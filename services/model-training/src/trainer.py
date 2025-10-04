"""
Distributed Model Training Worker
Handles actual model training execution in Kubernetes Jobs
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

import torch
import torch.nn as nn
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
import mlflow
import mlflow.pytorch
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Distributed model trainer"""
    
    def __init__(self, config: Dict[str, Any], job_id: str, user_id: str):
        self.config = config
        self.job_id = job_id
        self.user_id = user_id
        self.device = None
        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.train_loader = None
        self.val_loader = None
        self.best_metric = 0.0
        self.early_stopping_counter = 0
        self.early_stopping_patience = config.get('early_stopping_patience', 10)
        
        # MLflow setup
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        self.experiment_name = f"training-{user_id}"
        
        # S3 client for model storage
        self.s3_client = boto3.client('s3')
        self.s3_bucket = os.getenv("S3_BUCKET", "aic-aipaas-models")
        
    def setup_distributed(self, rank: int, world_size: int):
        """Setup distributed training"""
        os.environ['MASTER_ADDR'] = 'localhost'
        os.environ['MASTER_PORT'] = '12355'
        
        # Initialize the process group
        dist.init_process_group("nccl", rank=rank, world_size=world_size)
        
        # Set device
        torch.cuda.set_device(rank)
        self.device = torch.device(f"cuda:{rank}")
        
    def cleanup_distributed(self):
        """Cleanup distributed training"""
        dist.destroy_process_group()
        
    def create_model(self) -> nn.Module:
        """Create model based on configuration"""
        model_type = self.config.get('model_type', 'resnet18')
        num_classes = self.config.get('num_classes', 10)
        
        if model_type == 'resnet18':
            from torchvision.models import resnet18
            model = resnet18(pretrained=True)
            model.fc = nn.Linear(model.fc.in_features, num_classes)
        elif model_type == 'resnet50':
            from torchvision.models import resnet50
            model = resnet50(pretrained=True)
            model.fc = nn.Linear(model.fc.in_features, num_classes)
        elif model_type == 'transformer':
            from transformers import AutoModel, AutoConfig
            config_name = self.config.get('model_name', 'bert-base-uncased')
            config = AutoConfig.from_pretrained(config_name)
            config.num_labels = num_classes
            model = AutoModel.from_pretrained(config_name, config=config)
        else:
            # Simple CNN for demonstration
            model = nn.Sequential(
                nn.Conv2d(3, 32, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(32, 64, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.AdaptiveAvgPool2d((1, 1)),
                nn.Flatten(),
                nn.Linear(64, num_classes)
            )
        
        return model
    
    def create_data_loaders(self):
        """Create training and validation data loaders"""
        from torchvision import datasets, transforms
        
        # Data transforms
        transform_train = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(32, padding=4),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])
        
        transform_val = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
        ])
        
        # Load dataset based on configuration
        dataset_path = self.config.get('dataset_path', '/data')
        
        if 'cifar' in dataset_path.lower():
            train_dataset = datasets.CIFAR10(
                root=dataset_path, train=True, download=True, transform=transform_train
            )
            val_dataset = datasets.CIFAR10(
                root=dataset_path, train=False, download=True, transform=transform_val
            )
        else:
            # Custom dataset
            train_dataset = datasets.ImageFolder(
                root=os.path.join(dataset_path, 'train'), transform=transform_train
            )
            val_dataset = datasets.ImageFolder(
                root=os.path.join(dataset_path, 'val'), transform=transform_val
            )
        
        # Distributed samplers
        if self.config.get('distributed', False):
            train_sampler = DistributedSampler(train_dataset)
            val_sampler = DistributedSampler(val_dataset, shuffle=False)
        else:
            train_sampler = None
            val_sampler = None
        
        # Data loaders
        self.train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.get('batch_size', 32),
            shuffle=(train_sampler is None),
            sampler=train_sampler,
            num_workers=4,
            pin_memory=True
        )
        
        self.val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.get('batch_size', 32),
            shuffle=False,
            sampler=val_sampler,
            num_workers=4,
            pin_memory=True
        )
    
    def create_optimizer_and_scheduler(self):
        """Create optimizer and learning rate scheduler"""
        lr = self.config.get('learning_rate', 0.001)
        weight_decay = self.config.get('weight_decay', 1e-4)
        
        # Optimizer
        optimizer_type = self.config.get('optimizer', 'adam')
        if optimizer_type.lower() == 'adam':
            self.optimizer = torch.optim.Adam(
                self.model.parameters(), lr=lr, weight_decay=weight_decay
            )
        elif optimizer_type.lower() == 'sgd':
            momentum = self.config.get('momentum', 0.9)
            self.optimizer = torch.optim.SGD(
                self.model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay
            )
        else:
            self.optimizer = torch.optim.AdamW(
                self.model.parameters(), lr=lr, weight_decay=weight_decay
            )
        
        # Scheduler
        scheduler_type = self.config.get('scheduler', 'cosine')
        epochs = self.config.get('epochs', 10)
        
        if scheduler_type == 'cosine':
            self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=epochs
            )
        elif scheduler_type == 'step':
            step_size = self.config.get('step_size', epochs // 3)
            gamma = self.config.get('gamma', 0.1)
            self.scheduler = torch.optim.lr_scheduler.StepLR(
                self.optimizer, step_size=step_size, gamma=gamma
            )
        else:
            self.scheduler = None
    
    def train_epoch(self, epoch: int) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = nn.CrossEntropyLoss()(output, target)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
            
            if batch_idx % 100 == 0:
                logger.info(
                    f'Epoch {epoch}, Batch {batch_idx}/{len(self.train_loader)}, '
                    f'Loss: {loss.item():.6f}, Acc: {100. * correct / total:.2f}%'
                )
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100. * correct / total
        
        return {'loss': avg_loss, 'accuracy': accuracy}
    
    def validate(self) -> Dict[str, float]:
        """Validate the model"""
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_targets = []
        
        with torch.no_grad():
            for data, target in self.val_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = nn.CrossEntropyLoss()(output, target)
                total_loss += loss.item()
                
                pred = output.argmax(dim=1)
                all_preds.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
        
        avg_loss = total_loss / len(self.val_loader)
        accuracy = accuracy_score(all_targets, all_preds)
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_targets, all_preds, average='weighted'
        )
        
        return {
            'loss': avg_loss,
            'accuracy': accuracy * 100,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def save_checkpoint(self, epoch: int, metrics: Dict[str, float], is_best: bool = False):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': metrics,
            'config': self.config
        }
        
        # Save locally first
        checkpoint_dir = Path(f"/models/{self.job_id}")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint_path = checkpoint_dir / f"checkpoint_epoch_{epoch}.pth"
        torch.save(checkpoint, checkpoint_path)
        
        if is_best:
            best_path = checkpoint_dir / "best_model.pth"
            torch.save(checkpoint, best_path)
            
            # Upload best model to S3
            try:
                s3_key = f"models/{self.user_id}/{self.job_id}/best_model.pth"
                self.s3_client.upload_file(str(best_path), self.s3_bucket, s3_key)
                logger.info(f"Uploaded best model to S3: {s3_key}")
            except ClientError as e:
                logger.error(f"Failed to upload model to S3: {e}")
        
        logger.info(f"Saved checkpoint: {checkpoint_path}")
    
    def train(self, rank: int = 0, world_size: int = 1):
        """Main training loop"""
        
        # Setup distributed training if needed
        if self.config.get('distributed', False) and world_size > 1:
            self.setup_distributed(rank, world_size)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Create model, data loaders, optimizer
        self.model = self.create_model().to(self.device)
        
        if self.config.get('distributed', False) and world_size > 1:
            self.model = DDP(self.model, device_ids=[rank])
        
        self.create_data_loaders()
        self.create_optimizer_and_scheduler()
        
        # MLflow experiment
        mlflow.set_experiment(self.experiment_name)
        
        with mlflow.start_run(run_name=f"job-{self.job_id}"):
            # Log hyperparameters
            mlflow.log_params(self.config)
            
            epochs = self.config.get('epochs', 10)
            checkpoint_interval = self.config.get('checkpoint_interval', 5)
            
            for epoch in range(1, epochs + 1):
                start_time = time.time()
                
                # Training
                train_metrics = self.train_epoch(epoch)
                
                # Validation
                val_metrics = self.validate()
                
                epoch_time = time.time() - start_time
                
                # Log metrics
                mlflow.log_metrics({
                    'train_loss': train_metrics['loss'],
                    'train_accuracy': train_metrics['accuracy'],
                    'val_loss': val_metrics['loss'],
                    'val_accuracy': val_metrics['accuracy'],
                    'val_precision': val_metrics['precision'],
                    'val_recall': val_metrics['recall'],
                    'val_f1': val_metrics['f1'],
                    'epoch_time': epoch_time,
                    'learning_rate': self.optimizer.param_groups[0]['lr']
                }, step=epoch)
                
                logger.info(
                    f'Epoch {epoch}/{epochs} - '
                    f'Train Loss: {train_metrics["loss"]:.4f}, '
                    f'Train Acc: {train_metrics["accuracy"]:.2f}%, '
                    f'Val Loss: {val_metrics["loss"]:.4f}, '
                    f'Val Acc: {val_metrics["accuracy"]:.2f}%, '
                    f'Time: {epoch_time:.2f}s'
                )
                
                # Check if this is the best model
                current_metric = val_metrics['accuracy']
                is_best = current_metric > self.best_metric
                if is_best:
                    self.best_metric = current_metric
                    self.early_stopping_counter = 0
                else:
                    self.early_stopping_counter += 1
                
                # Save checkpoint
                if epoch % checkpoint_interval == 0 or is_best:
                    self.save_checkpoint(epoch, val_metrics, is_best)
                
                # Learning rate scheduling
                if self.scheduler:
                    self.scheduler.step()
                
                # Early stopping
                if (self.config.get('early_stopping', True) and 
                    self.early_stopping_counter >= self.early_stopping_patience):
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Log final model
            if rank == 0:  # Only log from main process
                model_path = f"/models/{self.job_id}/best_model.pth"
                if os.path.exists(model_path):
                    mlflow.pytorch.log_model(
                        self.model.module if hasattr(self.model, 'module') else self.model,
                        "model",
                        registered_model_name=f"{self.user_id}-{self.job_id}"
                    )
        
        # Cleanup
        if self.config.get('distributed', False) and world_size > 1:
            self.cleanup_distributed()
        
        logger.info("Training completed successfully")

def main():
    """Main entry point for training worker"""
    
    # Get configuration from command line arguments
    if len(sys.argv) < 2:
        logger.error("Training configuration not provided")
        sys.exit(1)
    
    try:
        config = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        logger.error(f"Invalid configuration JSON: {e}")
        sys.exit(1)
    
    # Get job information from environment
    job_id = os.getenv("JOB_ID")
    user_id = os.getenv("USER_ID")
    
    if not job_id or not user_id:
        logger.error("JOB_ID and USER_ID environment variables are required")
        sys.exit(1)
    
    # Create trainer
    trainer = ModelTrainer(config, job_id, user_id)
    
    # Check if distributed training is enabled
    if config.get('distributed', False):
        world_size = int(os.getenv('WORLD_SIZE', 1))
        rank = int(os.getenv('RANK', 0))
        
        if world_size > 1:
            mp.spawn(trainer.train, args=(world_size,), nprocs=world_size, join=True)
        else:
            trainer.train()
    else:
        trainer.train()

if __name__ == "__main__":
    main()
