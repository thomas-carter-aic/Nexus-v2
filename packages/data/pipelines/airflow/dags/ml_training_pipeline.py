"""
AIC AI Platform ML Training Pipeline DAG
Orchestrates end-to-end machine learning training workflows
"""

from datetime import datetime, timedelta
from typing import Dict, Any

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Default arguments
default_args = {
    'owner': 'aic-aipaas',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=6),
}

# DAG definition
dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='End-to-end ML training pipeline',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    tags=['ml', 'training', 'pipeline'],
)

# Configuration
NAMESPACE = 'ai-services'
AUTH_SERVICE_URL = Variable.get("AUTH_SERVICE_URL", "http://auth-service:8000")
TRAINING_SERVICE_URL = Variable.get("TRAINING_SERVICE_URL", "http://model-training-service:8001")
FEATURE_STORE_URL = Variable.get("FEATURE_STORE_URL", "http://feature-store-service:8004")
MODEL_REGISTRY_URL = Variable.get("MODEL_REGISTRY_URL", "http://model-registry-service:8003")

def validate_data_quality(**context):
    """Validate data quality before training"""
    
    # Get data from feature store
    feature_store_response = requests.post(
        f"{FEATURE_STORE_URL}/features/offline",
        json={
            "feature_views": ["user_features", "transaction_features"],
            "entity_df": {
                "user_id": list(range(1, 1001)),  # Sample 1000 users
                "event_timestamp": ["2025-01-15T00:00:00"] * 1000
            }
        },
        headers={"Authorization": f"Bearer {context['params']['auth_token']}"}
    )
    
    if feature_store_response.status_code != 200:
        raise Exception(f"Failed to get features: {feature_store_response.text}")
    
    features_data = feature_store_response.json()
    df = pd.DataFrame(features_data['features'])
    
    # Data quality checks
    quality_checks = {
        'row_count': len(df),
        'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)),
        'duplicate_percentage': df.duplicated().sum() / len(df),
        'feature_count': len(df.columns)
    }
    
    # Quality thresholds
    if quality_checks['row_count'] < 100:
        raise Exception(f"Insufficient data: {quality_checks['row_count']} rows")
    
    if quality_checks['null_percentage'] > 0.3:
        raise Exception(f"Too many null values: {quality_checks['null_percentage']:.2%}")
    
    if quality_checks['duplicate_percentage'] > 0.1:
        raise Exception(f"Too many duplicates: {quality_checks['duplicate_percentage']:.2%}")
    
    logger.info(f"Data quality checks passed: {quality_checks}")
    
    # Store quality metrics in XCom
    context['task_instance'].xcom_push(key='data_quality', value=quality_checks)
    
    return quality_checks

def prepare_training_config(**context):
    """Prepare training configuration"""
    
    data_quality = context['task_instance'].xcom_pull(key='data_quality')
    
    # Dynamic configuration based on data quality
    config = {
        "framework": "pytorch",
        "model_type": "neural_network",
        "dataset_path": "/data/training_dataset.parquet",
        "hyperparameters": {
            "hidden_layers": [128, 64, 32],
            "dropout_rate": 0.2,
            "activation": "relu"
        },
        "epochs": 50 if data_quality['row_count'] > 10000 else 30,
        "batch_size": 64 if data_quality['row_count'] > 5000 else 32,
        "learning_rate": 0.001,
        "early_stopping": True,
        "checkpoint_interval": 5,
        "distributed": data_quality['row_count'] > 50000
    }
    
    # Store config in XCom
    context['task_instance'].xcom_push(key='training_config', value=config)
    
    return config

def submit_training_job(**context):
    """Submit training job to model training service"""
    
    training_config = context['task_instance'].xcom_pull(key='training_config')
    
    # Prepare training job request
    job_request = {
        "name": f"scheduled_training_{context['ds_nodash']}",
        "description": f"Scheduled training job for {context['ds']}",
        "config": training_config,
        "resource_requirements": {
            "cpu": "4",
            "memory": "8Gi",
            "gpu": 1 if training_config.get('distributed', False) else 0,
            "storage": "50Gi"
        },
        "priority": 2,
        "tags": ["scheduled", "production"]
    }
    
    # Submit job
    response = requests.post(
        f"{TRAINING_SERVICE_URL}/training/jobs",
        json=job_request,
        headers={"Authorization": f"Bearer {context['params']['auth_token']}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to submit training job: {response.text}")
    
    job_info = response.json()
    job_id = job_info['id']
    
    logger.info(f"Training job submitted: {job_id}")
    
    # Store job ID in XCom
    context['task_instance'].xcom_push(key='training_job_id', value=job_id)
    
    return job_id

def monitor_training_job(**context):
    """Monitor training job completion"""
    
    job_id = context['task_instance'].xcom_pull(key='training_job_id')
    
    # Poll job status
    import time
    max_wait_time = 3600  # 1 hour
    poll_interval = 30    # 30 seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        response = requests.get(
            f"{TRAINING_SERVICE_URL}/training/jobs/{job_id}",
            headers={"Authorization": f"Bearer {context['params']['auth_token']}"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get job status: {response.text}")
        
        job_status = response.json()
        status = job_status['status']
        
        if status == 'completed':
            logger.info(f"Training job {job_id} completed successfully")
            context['task_instance'].xcom_push(key='training_result', value=job_status)
            return job_status
        elif status == 'failed':
            raise Exception(f"Training job {job_id} failed: {job_status.get('error_message', 'Unknown error')}")
        elif status in ['cancelled']:
            raise Exception(f"Training job {job_id} was cancelled")
        
        logger.info(f"Training job {job_id} status: {status}")
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    
    raise Exception(f"Training job {job_id} timed out after {max_wait_time} seconds")

def evaluate_model(**context):
    """Evaluate trained model"""
    
    training_result = context['task_instance'].xcom_pull(key='training_result')
    
    # Extract model metrics
    metrics = training_result.get('metrics', {})
    
    if not metrics:
        raise Exception("No metrics available from training job")
    
    # Model evaluation thresholds
    min_accuracy = 0.8
    max_loss = 0.5
    
    accuracy = metrics.get('val_accuracy', 0)
    loss = metrics.get('val_loss', float('inf'))
    
    if accuracy < min_accuracy:
        raise Exception(f"Model accuracy {accuracy:.3f} below threshold {min_accuracy}")
    
    if loss > max_loss:
        raise Exception(f"Model loss {loss:.3f} above threshold {max_loss}")
    
    evaluation_result = {
        'accuracy': accuracy,
        'loss': loss,
        'passed_evaluation': True,
        'evaluation_timestamp': datetime.utcnow().isoformat()
    }
    
    logger.info(f"Model evaluation passed: {evaluation_result}")
    
    context['task_instance'].xcom_push(key='evaluation_result', value=evaluation_result)
    
    return evaluation_result

def register_model(**context):
    """Register model in model registry"""
    
    training_result = context['task_instance'].xcom_pull(key='training_result')
    evaluation_result = context['task_instance'].xcom_pull(key='evaluation_result')
    
    # Register model
    model_request = {
        "name": f"scheduled_model_{context['ds_nodash']}",
        "description": f"Model trained on {context['ds']} via scheduled pipeline",
        "tags": ["scheduled", "production", "validated"],
        "use_case": "classification",
        "framework": "pytorch",
        "algorithm": "neural_network"
    }
    
    response = requests.post(
        f"{MODEL_REGISTRY_URL}/models",
        json=model_request,
        headers={"Authorization": f"Bearer {context['params']['auth_token']}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to register model: {response.text}")
    
    model_info = response.json()
    model_name = model_info['name']
    
    # Create model version
    version_request = {
        "model_name": model_name,
        "mlflow_run_id": training_result.get('run_id', 'unknown'),
        "description": f"Version created by scheduled pipeline on {context['ds']}",
        "stage": "Development"
    }
    
    response = requests.post(
        f"{MODEL_REGISTRY_URL}/models/{model_name}/versions",
        json=version_request,
        headers={"Authorization": f"Bearer {context['params']['auth_token']}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to create model version: {response.text}")
    
    version_info = response.json()
    
    logger.info(f"Model registered: {model_name}, version: {version_info['version']}")
    
    return {
        'model_name': model_name,
        'version': version_info['version'],
        'model_id': model_info['id']
    }

def send_notification(**context):
    """Send pipeline completion notification"""
    
    # Get results from previous tasks
    data_quality = context['task_instance'].xcom_pull(key='data_quality')
    evaluation_result = context['task_instance'].xcom_pull(key='evaluation_result')
    
    # Prepare notification message
    message = {
        "pipeline": "ml_training_pipeline",
        "execution_date": context['ds'],
        "status": "completed",
        "data_quality": data_quality,
        "model_performance": {
            "accuracy": evaluation_result['accuracy'],
            "loss": evaluation_result['loss']
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(f"Pipeline completed successfully: {message}")
    
    # Here you would typically send to Slack, email, or other notification service
    # For now, we'll just log the completion
    
    return message

# Task definitions
validate_data_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag,
)

prepare_config_task = PythonOperator(
    task_id='prepare_training_config',
    python_callable=prepare_training_config,
    dag=dag,
)

submit_job_task = PythonOperator(
    task_id='submit_training_job',
    python_callable=submit_training_job,
    dag=dag,
)

monitor_job_task = PythonOperator(
    task_id='monitor_training_job',
    python_callable=monitor_training_job,
    dag=dag,
)

evaluate_model_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

register_model_task = PythonOperator(
    task_id='register_model',
    python_callable=register_model,
    dag=dag,
)

notify_completion_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_notification,
    dag=dag,
)

# Health check for services
health_check_task = HttpSensor(
    task_id='check_services_health',
    http_conn_id='aic_services',
    endpoint='/health',
    timeout=60,
    poke_interval=10,
    dag=dag,
)

# Task dependencies
health_check_task >> validate_data_task >> prepare_config_task >> submit_job_task
submit_job_task >> monitor_job_task >> evaluate_model_task >> register_model_task
register_model_task >> notify_completion_task
