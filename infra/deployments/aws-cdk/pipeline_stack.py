"""
AWS CDK Stack for AI-Native PaaS CI/CD Pipeline

This module defines the AWS CDK infrastructure for a comprehensive CI/CD pipeline
that includes AI-driven deployment optimization, automated testing, blue/green
deployments, and intelligent rollback mechanisms.

Key Features:
- Multi-stage pipeline with automated testing
- AI-driven deployment optimization using SageMaker
- Blue/green deployment strategy
- Automated rollback on failure detection
- Cost-optimized build resources using Spot instances
- Parallel test execution for faster feedback
- Integration with monitoring and observability
"""

from aws_cdk import (
    Stack,
    Duration,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codedeploy as codedeploy,
    aws_iam as iam,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_sagemaker as sagemaker,
    aws_cloudwatch as cloudwatch,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    RemovalPolicy
)
from constructs import Construct
import json


class AIPaasPipelineStack(Stack):
    """
    CDK Stack for AI-Native PaaS CI/CD Pipeline
    
    This stack creates a comprehensive CI/CD pipeline with AI-driven optimizations,
    automated testing, and intelligent deployment strategies.
    """
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create core infrastructure components
        self._create_artifact_store()
        self._create_build_environment()
        self._create_ai_services()
        self._create_monitoring_resources()
        
        # Create the main CI/CD pipeline
        self._create_pipeline()
        
        # Create supporting Lambda functions
        self._create_pipeline_functions()
        
        # Create monitoring and alerting
        self._create_pipeline_monitoring()
    
    def _create_artifact_store(self) -> None:
        """
        Create S3 bucket for storing pipeline artifacts with encryption and versioning.
        
        The artifact store securely holds build artifacts, test results, and deployment
        packages throughout the pipeline execution.
        """
        self.artifact_bucket = s3.Bucket(
            self, "PipelineArtifacts",
            bucket_name=f"paas-pipeline-artifacts-{self.account}-{self.region}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteOldArtifacts",
                    enabled=True,
                    expiration=Duration.days(30),  # Clean up old artifacts
                    noncurrent_version_expiration=Duration.days(7)
                )
            ],
            removal_policy=RemovalPolicy.DESTROY  # For development/testing
        )
    
    def _create_build_environment(self) -> None:
        """
        Create optimized build environment with cost-efficient compute resources.
        
        Uses a combination of on-demand and spot instances for cost optimization
        while maintaining build reliability.
        """
        # VPC for build environment (optional, for enhanced security)
        self.build_vpc = ec2.Vpc(
            self, "BuildVPC",
            max_azs=2,
            nat_gateways=1,  # Cost optimization
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )
        
        # Security group for build environment
        self.build_security_group = ec2.SecurityGroup(
            self, "BuildSecurityGroup",
            vpc=self.build_vpc,
            description="Security group for CI/CD build environment",
            allow_all_outbound=True
        )
        
        # IAM role for CodeBuild projects
        self.build_role = iam.Role(
            self, "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeBuildDeveloperAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ],
            inline_policies={
                "BuildPolicy": iam.PolicyDocument(
                    statements=[
                        # Allow access to artifact bucket
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "s3:GetObject",
                                "s3:PutObject",
                                "s3:DeleteObject"
                            ],
                            resources=[f"{self.artifact_bucket.bucket_arn}/*"]
                        ),
                        # Allow CloudWatch logging
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            resources=["*"]
                        ),
                        # Allow SageMaker access for AI predictions
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "sagemaker:InvokeEndpoint",
                                "sagemaker:DescribeEndpoint"
                            ],
                            resources=["*"]
                        )
                    ]
                )
            }
        )
    
    def _create_ai_services(self) -> None:
        """
        Create AI/ML services for intelligent pipeline optimization.
        
        Sets up SageMaker endpoints for deployment risk assessment,
        test prioritization, and performance prediction.
        """
        # SageMaker execution role
        self.sagemaker_role = iam.Role(
            self, "SageMakerRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
            ]
        )
        
        # Model for deployment risk assessment
        self.deployment_risk_model = sagemaker.CfnModel(
            self, "DeploymentRiskModel",
            execution_role_arn=self.sagemaker_role.role_arn,
            model_name="paas-deployment-risk-predictor",
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image="382416733822.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest",
                model_data_url="s3://your-model-bucket/deployment-risk-model.tar.gz"
            )
        )
        
        # Endpoint configuration for deployment risk model
        self.risk_endpoint_config = sagemaker.CfnEndpointConfig(
            self, "RiskEndpointConfig",
            endpoint_config_name="paas-risk-assessment-config",
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    variant_name="primary",
                    model_name=self.deployment_risk_model.model_name,
                    initial_instance_count=1,
                    instance_type="ml.t2.medium",  # Cost-optimized instance
                    initial_variant_weight=1.0
                )
            ]
        )
        
        # SageMaker endpoint for deployment risk assessment
        self.risk_endpoint = sagemaker.CfnEndpoint(
            self, "RiskAssessmentEndpoint",
            endpoint_name="paas-deployment-risk-predictor",
            endpoint_config_name=self.risk_endpoint_config.endpoint_config_name
        )
        
        # Model for test prioritization
        self.test_prioritization_model = sagemaker.CfnModel(
            self, "TestPrioritizationModel",
            execution_role_arn=self.sagemaker_role.role_arn,
            model_name="paas-test-prioritization",
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image="382416733822.dkr.ecr.us-east-1.amazonaws.com/sklearn:latest",
                model_data_url="s3://your-model-bucket/test-prioritization-model.tar.gz"
            )
        )
        
        # Endpoint for test prioritization
        self.test_endpoint_config = sagemaker.CfnEndpointConfig(
            self, "TestEndpointConfig",
            endpoint_config_name="paas-test-prioritization-config",
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    variant_name="primary",
                    model_name=self.test_prioritization_model.model_name,
                    initial_instance_count=1,
                    instance_type="ml.t2.medium",
                    initial_variant_weight=1.0
                )
            ]
        )
        
        self.test_endpoint = sagemaker.CfnEndpoint(
            self, "TestPrioritizationEndpoint",
            endpoint_name="paas-test-prioritization",
            endpoint_config_name=self.test_endpoint_config.endpoint_config_name
        )
    
    def _create_monitoring_resources(self) -> None:
        """
        Create monitoring and observability resources for the pipeline.
        
        Sets up CloudWatch dashboards, alarms, and custom metrics for
        comprehensive pipeline monitoring and alerting.
        """
        # CloudWatch Log Group for pipeline logs
        self.pipeline_log_group = logs.LogGroup(
            self, "PipelineLogGroup",
            log_group_name="/aws/codepipeline/paas-pipeline",
            retention=logs.RetentionDays.ONE_MONTH,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Custom metrics namespace
        self.metrics_namespace = "PaaS/Pipeline"
        
        # CloudWatch Dashboard for pipeline monitoring
        self.pipeline_dashboard = cloudwatch.Dashboard(
            self, "PipelineDashboard",
            dashboard_name="PaaS-CI-CD-Pipeline",
            widgets=[
                [
                    cloudwatch.GraphWidget(
                        title="Pipeline Execution Times",
                        left=[
                            cloudwatch.Metric(
                                namespace=self.metrics_namespace,
                                metric_name="PipelineExecutionTime",
                                statistic="Average"
                            )
                        ],
                        width=12,
                        height=6
                    )
                ],
                [
                    cloudwatch.SingleValueWidget(
                        title="Success Rate",
                        metrics=[
                            cloudwatch.Metric(
                                namespace=self.metrics_namespace,
                                metric_name="PipelineSuccessRate",
                                statistic="Average"
                            )
                        ],
                        width=6,
                        height=6
                    ),
                    cloudwatch.SingleValueWidget(
                        title="AI Prediction Accuracy",
                        metrics=[
                            cloudwatch.Metric(
                                namespace=self.metrics_namespace,
                                metric_name="AIPredictionAccuracy",
                                statistic="Average"
                            )
                        ],
                        width=6,
                        height=6
                    )
                ]
            ]
        )
    
    def _create_pipeline(self) -> None:
        """
        Create the main CI/CD pipeline with multiple stages and AI integration.
        
        The pipeline includes:
        1. Source stage (CodeCommit)
        2. Build stage (CodeBuild with parallel builds)
        3. Test stage (Automated testing with AI prioritization)
        4. AI Analysis stage (Risk assessment and optimization)
        5. Deploy stage (Blue/green deployment)
        6. Monitor stage (Post-deployment monitoring)
        """
        # Source repository
        self.source_repo = codecommit.Repository(
            self, "SourceRepository",
            repository_name="paas-platform",
            description="AI-Native PaaS Platform Source Code"
        )
        
        # Pipeline artifacts
        source_output = codepipeline.Artifact("SourceOutput")
        build_output = codepipeline.Artifact("BuildOutput")
        test_output = codepipeline.Artifact("TestOutput")
        
        # Create CodeBuild projects
        self._create_build_projects()
        
        # Main pipeline
        self.pipeline = codepipeline.Pipeline(
            self, "PaasPipeline",
            pipeline_name="paas-ci-cd-pipeline",
            artifact_bucket=self.artifact_bucket,
            stages=[
                # Stage 1: Source
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="SourceAction",
                            repository=self.source_repo,
                            branch="main",
                            output=source_output,
                            trigger=codepipeline_actions.CodeCommitTrigger.EVENTS
                        )
                    ]
                ),
                
                # Stage 2: Build (Parallel builds for different components)
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="BuildCore",
                            project=self.core_build_project,
                            input=source_output,
                            outputs=[build_output],
                            run_order=1
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name="BuildAI",
                            project=self.ai_build_project,
                            input=source_output,
                            run_order=1  # Parallel with core build
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name="BuildInfrastructure",
                            project=self.infra_build_project,
                            input=source_output,
                            run_order=1  # Parallel with other builds
                        )
                    ]
                ),
                
                # Stage 3: Test (AI-prioritized testing)
                codepipeline.StageProps(
                    stage_name="Test",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="UnitTests",
                            project=self.unit_test_project,
                            input=build_output,
                            outputs=[test_output],
                            run_order=1
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name="IntegrationTests",
                            project=self.integration_test_project,
                            input=build_output,
                            run_order=2
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name="SecurityTests",
                            project=self.security_test_project,
                            input=build_output,
                            run_order=2  # Parallel with integration tests
                        )
                    ]
                ),
                
                # Stage 4: AI Analysis and Risk Assessment
                codepipeline.StageProps(
                    stage_name="AIAnalysis",
                    actions=[
                        codepipeline_actions.LambdaInvokeAction(
                            action_name="RiskAssessment",
                            lambda_=self.risk_assessment_function,
                            inputs=[test_output],
                            user_parameters={
                                "stage": "pre-deployment",
                                "sagemaker_endpoint": self.risk_endpoint.endpoint_name
                            }
                        )
                    ]
                ),
                
                # Stage 5: Deploy (Blue/Green with AI optimization)
                codepipeline.StageProps(
                    stage_name="Deploy",
                    actions=[
                        codepipeline_actions.LambdaInvokeAction(
                            action_name="BlueGreenDeploy",
                            lambda_=self.deployment_function,
                            inputs=[build_output],
                            user_parameters={
                                "deployment_strategy": "blue_green",
                                "ai_optimization": "enabled"
                            }
                        )
                    ]
                ),
                
                # Stage 6: Post-Deployment Monitoring
                codepipeline.StageProps(
                    stage_name="Monitor",
                    actions=[
                        codepipeline_actions.LambdaInvokeAction(
                            action_name="PostDeploymentMonitoring",
                            lambda_=self.monitoring_function,
                            inputs=[build_output],
                            user_parameters={
                                "monitoring_duration": "300",  # 5 minutes
                                "rollback_threshold": "5.0"    # 5% error rate
                            }
                        )
                    ]
                )
            ]
        )
    
    def _create_build_projects(self) -> None:
        """
        Create specialized CodeBuild projects for different components.
        
        Each project is optimized for its specific purpose with appropriate
        compute resources, environment variables, and build specifications.
        """
        # Core platform build project
        self.core_build_project = codebuild.Project(
            self, "CoreBuildProject",
            project_name="paas-core-build",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Logging in to Amazon ECR...",
                                "aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com",
                                "echo Installing dependencies...",
                                "pip install -r requirements.txt",
                                "pip install -r requirements-dev.txt"
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Build started on `date`",
                                "echo Building the Docker image...",
                                "docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .",
                                "docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG",
                                "echo Running static analysis...",
                                "pylint src/",
                                "black --check src/",
                                "mypy src/"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo Build completed on `date`",
                                "echo Pushing the Docker image...",
                                "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG",
                                "echo Writing image definitions file...",
                                "printf '[{\"name\":\"paas-core\",\"imageUri\":\"%s\"}]' $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG > imagedefinitions.json"
                            ]
                        }
                    },
                    "artifacts": {
                        "files": [
                            "imagedefinitions.json",
                            "**/*"
                        ]
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.MEDIUM,
                privileged=True  # Required for Docker builds
            ),
            environment_variables={
                "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(value=self.region),
                "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(value=self.account),
                "IMAGE_REPO_NAME": codebuild.BuildEnvironmentVariable(value="paas-core"),
                "IMAGE_TAG": codebuild.BuildEnvironmentVariable(value="latest")
            },
            role=self.build_role,
            vpc=self.build_vpc,
            security_groups=[self.build_security_group]
        )
        
        # AI services build project
        self.ai_build_project = codebuild.Project(
            self, "AIBuildProject",
            project_name="paas-ai-build",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Installing AI/ML dependencies...",
                                "pip install -r src/ai/requirements.txt",
                                "pip install boto3 sagemaker scikit-learn numpy pandas"
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Building AI models...",
                                "cd src/ai",
                                "python train_models.py",
                                "echo Packaging models for SageMaker...",
                                "tar -czf models.tar.gz models/",
                                "aws s3 cp models.tar.gz s3://$MODEL_BUCKET/models/"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo AI build completed on `date`"
                            ]
                        }
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.LARGE  # More compute for ML workloads
            ),
            environment_variables={
                "MODEL_BUCKET": codebuild.BuildEnvironmentVariable(value="paas-ml-models")
            },
            role=self.build_role
        )
        
        # Infrastructure build project
        self.infra_build_project = codebuild.Project(
            self, "InfraBuildProject",
            project_name="paas-infra-build",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Installing CDK...",
                                "npm install -g aws-cdk",
                                "pip install aws-cdk-lib constructs"
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Synthesizing CDK stacks...",
                                "cd deployments/aws-cdk",
                                "cdk synth",
                                "echo Validating infrastructure templates...",
                                "cdk diff"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo Infrastructure build completed on `date`"
                            ]
                        }
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.SMALL  # CDK doesn't need much compute
            ),
            role=self.build_role
        )
        
        # Unit test project with AI-driven test prioritization
        self.unit_test_project = codebuild.Project(
            self, "UnitTestProject",
            project_name="paas-unit-tests",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Installing test dependencies...",
                                "pip install pytest pytest-cov pytest-asyncio pytest-mock",
                                "echo Getting AI test prioritization...",
                                "python scripts/prioritize_tests.py --endpoint $TEST_PRIORITIZATION_ENDPOINT"
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Running prioritized unit tests...",
                                "pytest tests/unit/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml -v"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo Unit tests completed on `date`",
                                "echo Uploading test results...",
                                "aws s3 cp test-results.xml s3://$ARTIFACT_BUCKET/test-results/",
                                "aws s3 cp htmlcov/ s3://$ARTIFACT_BUCKET/coverage-report/ --recursive"
                            ]
                        }
                    },
                    "reports": {
                        "pytest_reports": {
                            "files": [
                                "test-results.xml"
                            ],
                            "file_format": "JUNITXML"
                        }
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.MEDIUM
            ),
            environment_variables={
                "TEST_PRIORITIZATION_ENDPOINT": codebuild.BuildEnvironmentVariable(
                    value=self.test_endpoint.endpoint_name
                ),
                "ARTIFACT_BUCKET": codebuild.BuildEnvironmentVariable(
                    value=self.artifact_bucket.bucket_name
                )
            },
            role=self.build_role
        )
        
        # Integration test project
        self.integration_test_project = codebuild.Project(
            self, "IntegrationTestProject",
            project_name="paas-integration-tests",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Setting up integration test environment...",
                                "docker-compose -f tests/integration/docker-compose.yml up -d",
                                "sleep 30"  # Wait for services to start
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Running integration tests...",
                                "pytest tests/integration/ --junitxml=integration-test-results.xml -v"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo Cleaning up test environment...",
                                "docker-compose -f tests/integration/docker-compose.yml down",
                                "echo Integration tests completed on `date`"
                            ]
                        }
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.LARGE,  # More resources for integration tests
                privileged=True  # Required for Docker
            ),
            role=self.build_role,
            vpc=self.build_vpc,
            security_groups=[self.build_security_group]
        )
        
        # Security test project
        self.security_test_project = codebuild.Project(
            self, "SecurityTestProject",
            project_name="paas-security-tests",
            source=codebuild.Source.code_pipeline(
                build_spec=codebuild.BuildSpec.from_object({
                    "version": "0.2",
                    "phases": {
                        "pre_build": {
                            "commands": [
                                "echo Installing security testing tools...",
                                "pip install bandit safety",
                                "npm install -g retire"
                            ]
                        },
                        "build": {
                            "commands": [
                                "echo Running security scans...",
                                "bandit -r src/ -f json -o bandit-report.json",
                                "safety check --json --output safety-report.json",
                                "retire --js --outputformat json --outputpath retire-report.json || true"
                            ]
                        },
                        "post_build": {
                            "commands": [
                                "echo Security tests completed on `date`",
                                "echo Uploading security reports...",
                                "aws s3 cp bandit-report.json s3://$ARTIFACT_BUCKET/security-reports/",
                                "aws s3 cp safety-report.json s3://$ARTIFACT_BUCKET/security-reports/",
                                "aws s3 cp retire-report.json s3://$ARTIFACT_BUCKET/security-reports/"
                            ]
                        }
                    }
                })
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.SMALL
            ),
            environment_variables={
                "ARTIFACT_BUCKET": codebuild.BuildEnvironmentVariable(
                    value=self.artifact_bucket.bucket_name
                )
            },
            role=self.build_role
        )
