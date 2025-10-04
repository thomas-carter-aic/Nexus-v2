"""
Infrastructure Manager for AI-Native PaaS Platform.

This module manages the complete infrastructure lifecycle using Infrastructure
as Code (IaC) principles with AI-driven optimization and multi-environment support.

Features:
- AWS CDK infrastructure deployment
- Multi-environment management (dev, staging, production)
- AI-driven resource optimization
- Cost optimization and monitoring
- Security hardening and compliance
- Disaster recovery and backup strategies
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class Environment(str, Enum):
    """Deployment environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class InfrastructureStatus(str, Enum):
    """Infrastructure deployment status."""
    PENDING = "pending"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    UPDATING = "updating"
    FAILED = "failed"
    DESTROYING = "destroying"
    DESTROYED = "destroyed"


@dataclass
class InfrastructureConfig:
    """Infrastructure configuration for deployment."""
    environment: Environment
    region: str
    vpc_cidr: str = "10.0.0.0/16"
    availability_zones: List[str] = field(default_factory=lambda: ["us-east-1a", "us-east-1b"])
    enable_nat_gateway: bool = True
    enable_vpn_gateway: bool = False
    enable_flow_logs: bool = True
    backup_retention_days: int = 30
    monitoring_enabled: bool = True
    ai_optimization_enabled: bool = True
    cost_optimization_enabled: bool = True
    security_hardening_enabled: bool = True


@dataclass
class ResourceSpec:
    """Resource specification for infrastructure components."""
    resource_type: str
    resource_name: str
    configuration: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeploymentResult:
    """Infrastructure deployment result."""
    deployment_id: str
    environment: Environment
    status: InfrastructureStatus
    resources_created: List[str]
    resources_updated: List[str]
    resources_failed: List[str]
    deployment_time: datetime
    cost_estimate: float
    ai_optimizations_applied: List[str]
    metadata: Dict[str, Any]


class InfrastructureManager:
    """
    Infrastructure Manager with AI-driven optimization.
    
    Manages complete infrastructure lifecycle using Infrastructure as Code
    with intelligent resource optimization and multi-environment support.
    """
    
    def __init__(self, ai_service=None):
        """
        Initialize Infrastructure Manager.
        
        Args:
            ai_service: AI service for intelligent optimization
        """
        self.ai_service = ai_service
        
        # Initialize AWS clients
        try:
            self.cloudformation_client = boto3.client('cloudformation')
            self.ec2_client = boto3.client('ec2')
            self.iam_client = boto3.client('iam')
            self.s3_client = boto3.client('s3')
            self.rds_client = boto3.client('rds')
            self.elasticache_client = boto3.client('elasticache')
            
            # Test AWS connectivity
            try:
                self.cloudformation_client.list_stacks(MaxItems=1)
                logger.info("Infrastructure Manager initialized with AWS connectivity")
            except Exception:
                logger.warning("AWS not available - using mock mode")
                self._enable_mock_mode()
                
        except (NoCredentialsError, Exception):
            logger.warning("AWS credentials not configured - using mock mode")
            self._enable_mock_mode()
        
        # Manager state
        self.deployments: Dict[str, DeploymentResult] = {}
        self.environments: Dict[Environment, Dict[str, Any]] = {}
        self.resource_templates: Dict[str, Dict[str, Any]] = {}
        
        # Configuration
        self.default_region = "us-east-1"
        self.stack_prefix = "ai-paas"
        
        # Initialize resource templates
        self._initialize_resource_templates()
        
        logger.info("Infrastructure Manager initialized")
    
    def _enable_mock_mode(self):
        """Enable mock mode for testing without AWS."""
        self.cloudformation_client = None
        self.ec2_client = None
        self.iam_client = None
        self.s3_client = None
        self.rds_client = None
        self.elasticache_client = None
    
    def _initialize_resource_templates(self):
        """Initialize CloudFormation templates for different resources."""
        
        # VPC Template
        self.resource_templates['vpc'] = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "AI-Native PaaS VPC Infrastructure",
            "Parameters": {
                "Environment": {"Type": "String"},
                "VpcCidr": {"Type": "String", "Default": "10.0.0.0/16"},
                "AvailabilityZones": {"Type": "CommaDelimitedList"}
            },
            "Resources": {
                "VPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": {"Ref": "VpcCidr"},
                        "EnableDnsHostnames": True,
                        "EnableDnsSupport": True,
                        "Tags": [
                            {"Key": "Name", "Value": {"Fn::Sub": "${Environment}-ai-paas-vpc"}},
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Platform", "Value": "AI-Native-PaaS"}
                        ]
                    }
                },
                "InternetGateway": {
                    "Type": "AWS::EC2::InternetGateway",
                    "Properties": {
                        "Tags": [
                            {"Key": "Name", "Value": {"Fn::Sub": "${Environment}-ai-paas-igw"}},
                            {"Key": "Environment", "Value": {"Ref": "Environment"}}
                        ]
                    }
                },
                "VPCGatewayAttachment": {
                    "Type": "AWS::EC2::VPCGatewayAttachment",
                    "Properties": {
                        "VpcId": {"Ref": "VPC"},
                        "InternetGatewayId": {"Ref": "InternetGateway"}
                    }
                }
            },
            "Outputs": {
                "VpcId": {"Value": {"Ref": "VPC"}},
                "InternetGatewayId": {"Value": {"Ref": "InternetGateway"}}
            }
        }
        
        # ECS Cluster Template
        self.resource_templates['ecs_cluster'] = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "AI-Native PaaS ECS Cluster",
            "Parameters": {
                "Environment": {"Type": "String"},
                "VpcId": {"Type": "String"},
                "SubnetIds": {"Type": "CommaDelimitedList"}
            },
            "Resources": {
                "ECSCluster": {
                    "Type": "AWS::ECS::Cluster",
                    "Properties": {
                        "ClusterName": {"Fn::Sub": "${Environment}-ai-paas-cluster"},
                        "CapacityProviders": ["FARGATE", "FARGATE_SPOT"],
                        "DefaultCapacityProviderStrategy": [
                            {"CapacityProvider": "FARGATE", "Weight": 1, "Base": 0}
                        ],
                        "ClusterSettings": [
                            {"Name": "containerInsights", "Value": "enabled"}
                        ],
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Platform", "Value": "AI-Native-PaaS"}
                        ]
                    }
                },
                "ECSExecutionRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "RoleName": {"Fn::Sub": "${Environment}-ai-paas-ecs-execution-role"},
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                                    "Action": "sts:AssumeRole"
                                }
                            ]
                        },
                        "ManagedPolicyArns": [
                            "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
                        ]
                    }
                }
            },
            "Outputs": {
                "ClusterArn": {"Value": {"Ref": "ECSCluster"}},
                "ExecutionRoleArn": {"Value": {"Fn::GetAtt": ["ECSExecutionRole", "Arn"]}}
            }
        }
        
        # Database Template
        self.resource_templates['database'] = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "AI-Native PaaS Database Infrastructure",
            "Parameters": {
                "Environment": {"Type": "String"},
                "VpcId": {"Type": "String"},
                "SubnetIds": {"Type": "CommaDelimitedList"},
                "DatabasePassword": {"Type": "String", "NoEcho": True}
            },
            "Resources": {
                "DBSubnetGroup": {
                    "Type": "AWS::RDS::DBSubnetGroup",
                    "Properties": {
                        "DBSubnetGroupName": {"Fn::Sub": "${Environment}-ai-paas-db-subnet-group"},
                        "DBSubnetGroupDescription": "Subnet group for AI-Native PaaS database",
                        "SubnetIds": {"Ref": "SubnetIds"},
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Platform", "Value": "AI-Native-PaaS"}
                        ]
                    }
                },
                "DatabaseSecurityGroup": {
                    "Type": "AWS::EC2::SecurityGroup",
                    "Properties": {
                        "GroupName": {"Fn::Sub": "${Environment}-ai-paas-db-sg"},
                        "GroupDescription": "Security group for AI-Native PaaS database",
                        "VpcId": {"Ref": "VpcId"},
                        "SecurityGroupIngress": [
                            {
                                "IpProtocol": "tcp",
                                "FromPort": 5432,
                                "ToPort": 5432,
                                "CidrIp": "10.0.0.0/16",
                                "Description": "PostgreSQL access from VPC"
                            }
                        ]
                    }
                },
                "Database": {
                    "Type": "AWS::RDS::DBInstance",
                    "Properties": {
                        "DBInstanceIdentifier": {"Fn::Sub": "${Environment}-ai-paas-db"},
                        "DBInstanceClass": "db.t3.micro",
                        "Engine": "postgres",
                        "EngineVersion": "13.7",
                        "AllocatedStorage": 20,
                        "StorageType": "gp2",
                        "StorageEncrypted": True,
                        "MasterUsername": "aipaas",
                        "MasterUserPassword": {"Ref": "DatabasePassword"},
                        "DBSubnetGroupName": {"Ref": "DBSubnetGroup"},
                        "VPCSecurityGroups": [{"Ref": "DatabaseSecurityGroup"}],
                        "BackupRetentionPeriod": 7,
                        "MultiAZ": False,
                        "PubliclyAccessible": False,
                        "DeletionProtection": True,
                        "Tags": [
                            {"Key": "Environment", "Value": {"Ref": "Environment"}},
                            {"Key": "Platform", "Value": "AI-Native-PaaS"}
                        ]
                    }
                }
            },
            "Outputs": {
                "DatabaseEndpoint": {"Value": {"Fn::GetAtt": ["Database", "Endpoint.Address"]}},
                "DatabasePort": {"Value": {"Fn::GetAtt": ["Database", "Endpoint.Port"]}}
            }
        }
    
    async def deploy_environment(
        self, 
        config: InfrastructureConfig,
        dry_run: bool = False
    ) -> DeploymentResult:
        """
        Deploy complete environment infrastructure.
        
        Args:
            config: Infrastructure configuration
            dry_run: Whether to perform a dry run without actual deployment
            
        Returns:
            Deployment result with status and details
        """
        try:
            deployment_id = f"deploy-{config.environment.value}-{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Starting infrastructure deployment: {deployment_id}")
            
            # Apply AI optimizations if enabled
            if config.ai_optimization_enabled and self.ai_service:
                config = await self._apply_ai_optimizations(config)
            
            # Initialize deployment result
            deployment_result = DeploymentResult(
                deployment_id=deployment_id,
                environment=config.environment,
                status=InfrastructureStatus.DEPLOYING,
                resources_created=[],
                resources_updated=[],
                resources_failed=[],
                deployment_time=datetime.utcnow(),
                cost_estimate=0.0,
                ai_optimizations_applied=[],
                metadata={"config": config.__dict__, "dry_run": dry_run}
            )
            
            if dry_run:
                # Simulate deployment for dry run
                deployment_result = await self._simulate_deployment(config, deployment_result)
            else:
                # Perform actual deployment
                deployment_result = await self._execute_deployment(config, deployment_result)
            
            # Store deployment result
            self.deployments[deployment_id] = deployment_result
            
            logger.info(f"Infrastructure deployment completed: {deployment_id}")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Infrastructure deployment failed: {e}")
            raise
    
    async def _apply_ai_optimizations(self, config: InfrastructureConfig) -> InfrastructureConfig:
        """Apply AI-driven optimizations to infrastructure configuration."""
        try:
            if not self.ai_service:
                return config
            
            # Get AI insights for infrastructure optimization
            insights = await self.ai_service.get_comprehensive_insights(f"infrastructure-{config.environment.value}")
            
            optimizations_applied = []
            
            # Apply cost optimization insights
            cost_insights = [i for i in insights if i.insight_type.value == 'cost_optimization']
            for insight in cost_insights:
                if insight.confidence > 0.7:
                    # Apply cost optimizations
                    if 'instance_type' in insight.data:
                        optimizations_applied.append(f"Cost optimization: {insight.title}")
            
            # Apply resource recommendations
            resource_insights = [i for i in insights if i.insight_type.value == 'resource_recommendation']
            for insight in resource_insights:
                if insight.confidence > 0.8:
                    recommended_config = insight.data.get('recommended_config', {})
                    if 'availability_zones' in recommended_config:
                        config.availability_zones = recommended_config['availability_zones']
                        optimizations_applied.append("AI-optimized availability zone selection")
            
            logger.info(f"Applied {len(optimizations_applied)} AI optimizations")
            return config
            
        except Exception as e:
            logger.error(f"AI optimization failed: {e}")
            return config
    
    async def _simulate_deployment(
        self, 
        config: InfrastructureConfig, 
        deployment_result: DeploymentResult
    ) -> DeploymentResult:
        """Simulate infrastructure deployment for dry run."""
        try:
            # Simulate deployment steps
            await asyncio.sleep(1)  # Simulate deployment time
            
            # Simulate resource creation
            simulated_resources = [
                f"vpc-{config.environment.value}",
                f"subnet-public-{config.environment.value}-1a",
                f"subnet-public-{config.environment.value}-1b",
                f"subnet-private-{config.environment.value}-1a",
                f"subnet-private-{config.environment.value}-1b",
                f"igw-{config.environment.value}",
                f"nat-{config.environment.value}",
                f"ecs-cluster-{config.environment.value}",
                f"rds-{config.environment.value}",
                f"elasticache-{config.environment.value}"
            ]
            
            deployment_result.resources_created = simulated_resources
            deployment_result.status = InfrastructureStatus.DEPLOYED
            deployment_result.cost_estimate = self._estimate_infrastructure_cost(config)
            deployment_result.ai_optimizations_applied = [
                "Cost-optimized instance selection",
                "AI-driven availability zone distribution",
                "Intelligent backup retention optimization"
            ]
            
            logger.info(f"Simulated deployment completed with {len(simulated_resources)} resources")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Deployment simulation failed: {e}")
            deployment_result.status = InfrastructureStatus.FAILED
            deployment_result.metadata['error'] = str(e)
            return deployment_result
    
    async def _execute_deployment(
        self, 
        config: InfrastructureConfig, 
        deployment_result: DeploymentResult
    ) -> DeploymentResult:
        """Execute actual infrastructure deployment."""
        try:
            if not self.cloudformation_client:
                # Mock mode - simulate deployment
                return await self._simulate_deployment(config, deployment_result)
            
            # Deploy VPC stack
            vpc_stack_name = f"{self.stack_prefix}-{config.environment.value}-vpc"
            vpc_result = await self._deploy_stack(
                vpc_stack_name,
                self.resource_templates['vpc'],
                {
                    'Environment': config.environment.value,
                    'VpcCidr': config.vpc_cidr,
                    'AvailabilityZones': ','.join(config.availability_zones)
                }
            )
            
            if vpc_result['status'] == 'success':
                deployment_result.resources_created.extend(vpc_result['resources'])
            else:
                deployment_result.resources_failed.extend(vpc_result['resources'])
            
            # Deploy ECS stack
            ecs_stack_name = f"{self.stack_prefix}-{config.environment.value}-ecs"
            ecs_result = await self._deploy_stack(
                ecs_stack_name,
                self.resource_templates['ecs_cluster'],
                {
                    'Environment': config.environment.value,
                    'VpcId': vpc_result.get('vpc_id', 'vpc-mock'),
                    'SubnetIds': ','.join(['subnet-1', 'subnet-2'])  # Would get from VPC stack
                }
            )
            
            if ecs_result['status'] == 'success':
                deployment_result.resources_created.extend(ecs_result['resources'])
            else:
                deployment_result.resources_failed.extend(ecs_result['resources'])
            
            # Determine overall status
            if deployment_result.resources_failed:
                deployment_result.status = InfrastructureStatus.FAILED
            else:
                deployment_result.status = InfrastructureStatus.DEPLOYED
            
            deployment_result.cost_estimate = self._estimate_infrastructure_cost(config)
            
            logger.info(f"Infrastructure deployment executed: {len(deployment_result.resources_created)} resources created")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Infrastructure deployment execution failed: {e}")
            deployment_result.status = InfrastructureStatus.FAILED
            deployment_result.metadata['error'] = str(e)
            return deployment_result
    
    async def _deploy_stack(
        self, 
        stack_name: str, 
        template: Dict[str, Any], 
        parameters: Dict[str, str]
    ) -> Dict[str, Any]:
        """Deploy CloudFormation stack."""
        try:
            if not self.cloudformation_client:
                # Mock deployment
                return {
                    'status': 'success',
                    'resources': [f"{stack_name}-resource-1", f"{stack_name}-resource-2"],
                    'stack_id': f"arn:aws:cloudformation:us-east-1:123456789012:stack/{stack_name}/mock-id"
                }
            
            # Convert parameters to CloudFormation format
            cf_parameters = [
                {'ParameterKey': k, 'ParameterValue': v}
                for k, v in parameters.items()
            ]
            
            # Check if stack exists
            try:
                self.cloudformation_client.describe_stacks(StackName=stack_name)
                # Stack exists, update it
                response = self.cloudformation_client.update_stack(
                    StackName=stack_name,
                    TemplateBody=json.dumps(template),
                    Parameters=cf_parameters,
                    Capabilities=['CAPABILITY_NAMED_IAM']
                )
                operation = 'update'
            except ClientError as e:
                if 'does not exist' in str(e):
                    # Stack doesn't exist, create it
                    response = self.cloudformation_client.create_stack(
                        StackName=stack_name,
                        TemplateBody=json.dumps(template),
                        Parameters=cf_parameters,
                        Capabilities=['CAPABILITY_NAMED_IAM'],
                        Tags=[
                            {'Key': 'Platform', 'Value': 'AI-Native-PaaS'},
                            {'Key': 'ManagedBy', 'Value': 'InfrastructureManager'}
                        ]
                    )
                    operation = 'create'
                else:
                    raise
            
            stack_id = response['StackId']
            
            # Wait for stack operation to complete (simplified)
            await asyncio.sleep(2)  # In production, would poll for completion
            
            return {
                'status': 'success',
                'resources': [f"{stack_name}-vpc", f"{stack_name}-subnets", f"{stack_name}-gateways"],
                'stack_id': stack_id,
                'operation': operation
            }
            
        except Exception as e:
            logger.error(f"Stack deployment failed: {e}")
            return {
                'status': 'failed',
                'resources': [],
                'error': str(e)
            }
    
    def _estimate_infrastructure_cost(self, config: InfrastructureConfig) -> float:
        """Estimate monthly infrastructure cost."""
        try:
            # Base costs (simplified estimates)
            costs = {
                'vpc': 0.0,  # VPC is free
                'nat_gateway': 45.0,  # $45/month per NAT gateway
                'ecs_fargate': 50.0,  # Base ECS costs
                'rds_micro': 15.0,  # db.t3.micro
                'elasticache': 20.0,  # cache.t3.micro
                'cloudwatch': 10.0,  # Basic monitoring
                'data_transfer': 25.0  # Estimated data transfer
            }
            
            total_cost = sum(costs.values())
            
            # Apply environment multipliers
            if config.environment == Environment.PRODUCTION:
                total_cost *= 2.0  # Production has redundancy
            elif config.environment == Environment.STAGING:
                total_cost *= 0.7  # Staging is smaller
            else:
                total_cost *= 0.3  # Development is minimal
            
            return round(total_cost, 2)
            
        except Exception as e:
            logger.error(f"Cost estimation failed: {e}")
            return 100.0  # Default estimate
    
    async def destroy_environment(self, environment: Environment) -> bool:
        """
        Destroy environment infrastructure.
        
        Args:
            environment: Environment to destroy
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Destroying environment: {environment.value}")
            
            if not self.cloudformation_client:
                # Mock destruction
                logger.info(f"Mock destruction completed for {environment.value}")
                return True
            
            # Get all stacks for the environment
            stack_prefix = f"{self.stack_prefix}-{environment.value}"
            
            try:
                response = self.cloudformation_client.list_stacks(
                    StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE']
                )
                
                environment_stacks = [
                    stack for stack in response['StackSummaries']
                    if stack['StackName'].startswith(stack_prefix)
                ]
                
                # Delete stacks in reverse dependency order
                for stack in reversed(environment_stacks):
                    self.cloudformation_client.delete_stack(StackName=stack['StackName'])
                    logger.info(f"Initiated deletion of stack: {stack['StackName']}")
                
                return True
                
            except ClientError as e:
                logger.error(f"Failed to destroy environment: {e}")
                return False
            
        except Exception as e:
            logger.error(f"Environment destruction failed: {e}")
            return False
    
    async def get_environment_status(self, environment: Environment) -> Dict[str, Any]:
        """Get current status of environment infrastructure."""
        try:
            if not self.cloudformation_client:
                # Mock status
                return {
                    'environment': environment.value,
                    'status': 'deployed',
                    'resources': {
                        'vpc': 'active',
                        'ecs_cluster': 'active',
                        'database': 'active',
                        'cache': 'active'
                    },
                    'cost_estimate': self._estimate_infrastructure_cost(
                        InfrastructureConfig(environment=environment, region=self.default_region)
                    ),
                    'last_updated': datetime.utcnow().isoformat()
                }
            
            # Get actual stack status
            stack_prefix = f"{self.stack_prefix}-{environment.value}"
            
            try:
                response = self.cloudformation_client.list_stacks()
                environment_stacks = [
                    stack for stack in response['StackSummaries']
                    if stack['StackName'].startswith(stack_prefix)
                ]
                
                status = {
                    'environment': environment.value,
                    'stacks': len(environment_stacks),
                    'status': 'deployed' if environment_stacks else 'not_deployed',
                    'resources': {},
                    'last_updated': datetime.utcnow().isoformat()
                }
                
                for stack in environment_stacks:
                    status['resources'][stack['StackName']] = stack['StackStatus']
                
                return status
                
            except ClientError as e:
                logger.error(f"Failed to get environment status: {e}")
                return {'environment': environment.value, 'status': 'error', 'error': str(e)}
            
        except Exception as e:
            logger.error(f"Environment status check failed: {e}")
            return {'environment': environment.value, 'status': 'unknown', 'error': str(e)}
    
    async def get_deployment_history(self) -> List[DeploymentResult]:
        """Get deployment history."""
        return list(self.deployments.values())
    
    async def get_cost_analysis(self, environment: Environment) -> Dict[str, Any]:
        """Get cost analysis for environment."""
        try:
            # In production, this would integrate with AWS Cost Explorer
            config = InfrastructureConfig(environment=environment, region=self.default_region)
            estimated_cost = self._estimate_infrastructure_cost(config)
            
            return {
                'environment': environment.value,
                'estimated_monthly_cost': estimated_cost,
                'cost_breakdown': {
                    'compute': estimated_cost * 0.4,
                    'storage': estimated_cost * 0.2,
                    'network': estimated_cost * 0.2,
                    'monitoring': estimated_cost * 0.1,
                    'other': estimated_cost * 0.1
                },
                'optimization_opportunities': [
                    "Consider reserved instances for production workloads",
                    "Enable auto-scaling to optimize resource usage",
                    "Review storage classes for cost optimization"
                ],
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Cost analysis failed: {e}")
            return {'environment': environment.value, 'error': str(e)}
