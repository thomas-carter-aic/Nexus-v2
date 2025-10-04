"""
AWS Infrastructure Services Integration

This module provides concrete implementations of infrastructure services
using AWS services like ECS, Lambda, DynamoDB, EventBridge, and others.
It implements the infrastructure layer of the clean architecture pattern.

Key Components:
- ECS-based application deployment and management
- DynamoDB-based event store implementation
- EventBridge-based event publishing
- CloudWatch-based monitoring integration
- Cognito-based authentication services
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from ..core.domain.models import (
    Application, ApplicationId, ApplicationStatus, UserId,
    DomainEvent, EventType, Plugin, PluginId
)
from ..core.application.services import (
    ApplicationRepository, EventStore, PluginRepository
)


# Configure logging for infrastructure services
logger = logging.getLogger(__name__)


class DynamoDBEventStore(EventStore):
    """
    DynamoDB-based implementation of the event store for event sourcing.
    
    This implementation stores domain events in DynamoDB with optimized
    partition strategies for high throughput and efficient querying.
    
    Table Structure:
    - Partition Key: aggregate_id (UUID string)
    - Sort Key: version (integer)
    - Attributes: event_id, event_type, timestamp, data, metadata
    """
    
    def __init__(self, 
                 table_name: str = 'paas-event-store',
                 region_name: str = 'us-east-1',
                 dynamodb_client: Optional[boto3.client] = None):
        """
        Initialize the DynamoDB event store.
        
        Args:
            table_name: Name of the DynamoDB table for event storage
            region_name: AWS region name
            dynamodb_client: Optional pre-configured DynamoDB client
        """
        self._table_name = table_name
        self._region_name = region_name
        self._dynamodb = dynamodb_client or boto3.client('dynamodb', region_name=region_name)
        
        # Event store configuration
        self._max_batch_size = 25  # DynamoDB batch write limit
        self._retry_attempts = 3
        self._retry_delay_seconds = 1
    
    async def append_events(self, 
                          aggregate_id: str, 
                          events: List[DomainEvent], 
                          expected_version: int) -> None:
        """
        Append events to the event stream with optimistic concurrency control.
        
        Args:
            aggregate_id: Unique identifier of the aggregate
            events: List of domain events to append
            expected_version: Expected current version for concurrency control
            
        Raises:
            ConcurrencyError: If the expected version doesn't match current version
            InfrastructureError: If DynamoDB operations fail
        """
        if not events:
            return
        
        logger.debug(f"Appending {len(events)} events for aggregate {aggregate_id}")
        
        try:
            # Check current version for optimistic concurrency control
            current_version = await self._get_current_version(aggregate_id)
            if current_version != expected_version:
                raise ConcurrencyError(
                    f"Expected version {expected_version}, but current version is {current_version}"
                )
            
            # Prepare event items for DynamoDB
            event_items = []
            for i, event in enumerate(events):
                version = expected_version + i + 1
                event_item = {
                    'aggregate_id': {'S': aggregate_id},
                    'version': {'N': str(version)},
                    'event_id': {'S': str(event.event_id)},
                    'event_type': {'S': event.event_type.value},
                    'timestamp': {'S': event.timestamp.isoformat()},
                    'data': {'S': json.dumps(event.to_dict())},
                    'metadata': {'S': json.dumps(event.metadata)}
                }
                event_items.append(event_item)
            
            # Write events in batches to handle DynamoDB limits
            await self._batch_write_events(event_items)
            
            logger.info(f"Successfully appended {len(events)} events for aggregate {aggregate_id}")
            
        except ClientError as e:
            logger.error(f"DynamoDB error appending events: {str(e)}")
            raise InfrastructureError(f"Failed to append events: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error appending events: {str(e)}")
            raise InfrastructureError(f"Unexpected error: {str(e)}")
    
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[DomainEvent]:
        """
        Retrieve events for an aggregate starting from a specific version.
        
        Args:
            aggregate_id: Unique identifier of the aggregate
            from_version: Starting version number (inclusive)
            
        Returns:
            List of domain events ordered by version
        """
        logger.debug(f"Retrieving events for aggregate {aggregate_id} from version {from_version}")
        
        try:
            # Query DynamoDB for events
            response = self._dynamodb.query(
                TableName=self._table_name,
                KeyConditionExpression='aggregate_id = :aggregate_id AND version >= :from_version',
                ExpressionAttributeValues={
                    ':aggregate_id': {'S': aggregate_id},
                    ':from_version': {'N': str(from_version)}
                },
                ScanIndexForward=True  # Sort by version ascending
            )
            
            # Convert DynamoDB items to domain events
            events = []
            for item in response.get('Items', []):
                event_data = json.loads(item['data']['S'])
                event = self._deserialize_event(event_data)
                events.append(event)
            
            logger.debug(f"Retrieved {len(events)} events for aggregate {aggregate_id}")
            return events
            
        except ClientError as e:
            logger.error(f"DynamoDB error retrieving events: {str(e)}")
            raise InfrastructureError(f"Failed to retrieve events: {str(e)}")
    
    async def get_all_events(self, event_types: Optional[List[EventType]] = None) -> List[DomainEvent]:
        """
        Retrieve all events, optionally filtered by event types.
        
        Args:
            event_types: Optional list of event types to filter by
            
        Returns:
            List of domain events matching the criteria
        """
        logger.debug(f"Retrieving all events with filter: {event_types}")
        
        try:
            # Scan DynamoDB table (expensive operation, use with caution)
            scan_params = {
                'TableName': self._table_name
            }
            
            # Add filter expression if event types are specified
            if event_types:
                event_type_values = [event_type.value for event_type in event_types]
                filter_expression = 'event_type IN (' + ','.join([f':type{i}' for i in range(len(event_type_values))]) + ')'
                expression_values = {f':type{i}': {'S': event_type} for i, event_type in enumerate(event_type_values)}
                
                scan_params['FilterExpression'] = filter_expression
                scan_params['ExpressionAttributeValues'] = expression_values
            
            # Perform scan operation
            response = self._dynamodb.scan(**scan_params)
            
            # Convert DynamoDB items to domain events
            events = []
            for item in response.get('Items', []):
                event_data = json.loads(item['data']['S'])
                event = self._deserialize_event(event_data)
                events.append(event)
            
            # Sort events by timestamp
            events.sort(key=lambda e: e.timestamp)
            
            logger.debug(f"Retrieved {len(events)} events with filter")
            return events
            
        except ClientError as e:
            logger.error(f"DynamoDB error scanning events: {str(e)}")
            raise InfrastructureError(f"Failed to scan events: {str(e)}")
    
    async def _get_current_version(self, aggregate_id: str) -> int:
        """
        Get the current version of an aggregate by finding the highest version number.
        
        Args:
            aggregate_id: Unique identifier of the aggregate
            
        Returns:
            Current version number (0 if no events exist)
        """
        try:
            response = self._dynamodb.query(
                TableName=self._table_name,
                KeyConditionExpression='aggregate_id = :aggregate_id',
                ExpressionAttributeValues={
                    ':aggregate_id': {'S': aggregate_id}
                },
                ScanIndexForward=False,  # Sort by version descending
                Limit=1  # Only need the latest version
            )
            
            items = response.get('Items', [])
            if items:
                return int(items[0]['version']['N'])
            else:
                return 0  # No events exist for this aggregate
                
        except ClientError as e:
            logger.error(f"Error getting current version: {str(e)}")
            return 0  # Assume version 0 on error
    
    async def _batch_write_events(self, event_items: List[Dict[str, Any]]) -> None:
        """
        Write events to DynamoDB in batches to handle API limits.
        
        Args:
            event_items: List of DynamoDB items to write
        """
        # Split items into batches
        for i in range(0, len(event_items), self._max_batch_size):
            batch = event_items[i:i + self._max_batch_size]
            
            # Prepare batch write request
            request_items = {
                self._table_name: [
                    {'PutRequest': {'Item': item}} for item in batch
                ]
            }
            
            # Execute batch write with retries
            for attempt in range(self._retry_attempts):
                try:
                    response = self._dynamodb.batch_write_item(RequestItems=request_items)
                    
                    # Handle unprocessed items
                    unprocessed_items = response.get('UnprocessedItems', {})
                    if unprocessed_items:
                        logger.warning(f"Retrying {len(unprocessed_items)} unprocessed items")
                        request_items = unprocessed_items
                        await asyncio.sleep(self._retry_delay_seconds * (attempt + 1))
                        continue
                    else:
                        break  # All items processed successfully
                        
                except ClientError as e:
                    if attempt == self._retry_attempts - 1:
                        raise  # Re-raise on final attempt
                    logger.warning(f"Batch write attempt {attempt + 1} failed: {str(e)}")
                    await asyncio.sleep(self._retry_delay_seconds * (attempt + 1))
    
    def _deserialize_event(self, event_data: Dict[str, Any]) -> DomainEvent:
        """
        Deserialize event data from JSON to DomainEvent object.
        
        Args:
            event_data: Event data dictionary from JSON
            
        Returns:
            Deserialized domain event
        """
        # Create base domain event
        event = DomainEvent(
            aggregate_id=UUID(event_data['aggregate_id']),
            event_id=UUID(event_data['event_id']),
            timestamp=datetime.fromisoformat(event_data['timestamp']),
            version=event_data['version'],
            metadata=event_data['metadata']
        )
        
        # Set event type
        event.event_type = EventType(event_data['event_type'])
        
        return event


class ECSApplicationRepository(ApplicationRepository):
    """
    ECS-based implementation of the application repository.
    
    This implementation stores application metadata in DynamoDB and
    manages actual application deployments using AWS ECS Fargate.
    """
    
    def __init__(self,
                 table_name: str = 'paas-applications',
                 cluster_name: str = 'paas-cluster',
                 region_name: str = 'us-east-1',
                 dynamodb_client: Optional[boto3.client] = None,
                 ecs_client: Optional[boto3.client] = None):
        """
        Initialize the ECS application repository.
        
        Args:
            table_name: DynamoDB table name for application metadata
            cluster_name: ECS cluster name for application deployments
            region_name: AWS region name
            dynamodb_client: Optional pre-configured DynamoDB client
            ecs_client: Optional pre-configured ECS client
        """
        self._table_name = table_name
        self._cluster_name = cluster_name
        self._region_name = region_name
        self._dynamodb = dynamodb_client or boto3.client('dynamodb', region_name=region_name)
        self._ecs = ecs_client or boto3.client('ecs', region_name=region_name)
    
    async def save(self, application: Application) -> None:
        """
        Save application metadata to DynamoDB and update ECS service if needed.
        
        Args:
            application: The application aggregate to save
        """
        logger.debug(f"Saving application {application.id.value}")
        
        try:
            # Convert application to DynamoDB item
            app_dict = application.to_dict()
            item = {
                'id': {'S': app_dict['id']},
                'name': {'S': app_dict['name']},
                'user_id': {'S': app_dict['user_id']},
                'status': {'S': app_dict['status']},
                'current_instance_count': {'N': str(app_dict['current_instance_count'])},
                'resource_requirements': {'S': json.dumps(app_dict['resource_requirements'])},
                'scaling_config': {'S': json.dumps(app_dict['scaling_config'])},
                'created_at': {'S': app_dict['created_at']},
                'updated_at': {'S': app_dict['updated_at']},
                'version': {'N': str(app_dict['version'])}
            }
            
            # Save to DynamoDB
            self._dynamodb.put_item(
                TableName=self._table_name,
                Item=item
            )
            
            # Update ECS service if application is running
            if application.status == ApplicationStatus.RUNNING:
                await self._update_ecs_service(application)
            
            logger.info(f"Successfully saved application {application.id.value}")
            
        except ClientError as e:
            logger.error(f"Error saving application: {str(e)}")
            raise InfrastructureError(f"Failed to save application: {str(e)}")
    
    async def get_by_id(self, application_id: ApplicationId) -> Optional[Application]:
        """
        Retrieve application by ID from DynamoDB.
        
        Args:
            application_id: Unique identifier of the application
            
        Returns:
            Application aggregate if found, None otherwise
        """
        logger.debug(f"Retrieving application {application_id.value}")
        
        try:
            response = self._dynamodb.get_item(
                TableName=self._table_name,
                Key={'id': {'S': str(application_id.value)}}
            )
            
            item = response.get('Item')
            if not item:
                return None
            
            # Convert DynamoDB item to Application
            return self._deserialize_application(item)
            
        except ClientError as e:
            logger.error(f"Error retrieving application: {str(e)}")
            raise InfrastructureError(f"Failed to retrieve application: {str(e)}")
    
    async def get_by_user_id(self, user_id: UserId) -> List[Application]:
        """
        Retrieve all applications for a user using GSI.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of applications owned by the user
        """
        logger.debug(f"Retrieving applications for user {user_id.value}")
        
        try:
            # Query using Global Secondary Index on user_id
            response = self._dynamodb.query(
                TableName=self._table_name,
                IndexName='user-id-index',  # Assumes GSI exists
                KeyConditionExpression='user_id = :user_id',
                ExpressionAttributeValues={
                    ':user_id': {'S': user_id.value}
                }
            )
            
            applications = []
            for item in response.get('Items', []):
                app = self._deserialize_application(item)
                applications.append(app)
            
            logger.debug(f"Retrieved {len(applications)} applications for user {user_id.value}")
            return applications
            
        except ClientError as e:
            logger.error(f"Error retrieving user applications: {str(e)}")
            raise InfrastructureError(f"Failed to retrieve user applications: {str(e)}")
    
    async def delete(self, application_id: ApplicationId) -> bool:
        """
        Delete application from DynamoDB and clean up ECS resources.
        
        Args:
            application_id: Unique identifier of the application to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        logger.debug(f"Deleting application {application_id.value}")
        
        try:
            # First, clean up ECS service
            await self._cleanup_ecs_service(application_id)
            
            # Delete from DynamoDB
            response = self._dynamodb.delete_item(
                TableName=self._table_name,
                Key={'id': {'S': str(application_id.value)}},
                ReturnValues='ALL_OLD'
            )
            
            # Check if item was actually deleted
            deleted = 'Attributes' in response
            
            if deleted:
                logger.info(f"Successfully deleted application {application_id.value}")
            
            return deleted
            
        except ClientError as e:
            logger.error(f"Error deleting application: {str(e)}")
            raise InfrastructureError(f"Failed to delete application: {str(e)}")
    
    async def _update_ecs_service(self, application: Application) -> None:
        """
        Update ECS service configuration based on application state.
        
        Args:
            application: Application aggregate with updated configuration
        """
        service_name = f"app-{application.id.value}"
        
        try:
            # Update service desired count
            self._ecs.update_service(
                cluster=self._cluster_name,
                service=service_name,
                desiredCount=application.current_instance_count
            )
            
            logger.debug(f"Updated ECS service {service_name} to {application.current_instance_count} instances")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServiceNotFoundException':
                logger.warning(f"ECS service {service_name} not found, may need to be created")
            else:
                logger.error(f"Error updating ECS service: {str(e)}")
                raise InfrastructureError(f"Failed to update ECS service: {str(e)}")
    
    async def _cleanup_ecs_service(self, application_id: ApplicationId) -> None:
        """
        Clean up ECS service and related resources.
        
        Args:
            application_id: ID of the application to clean up
        """
        service_name = f"app-{application_id.value}"
        
        try:
            # Scale service to 0 first
            self._ecs.update_service(
                cluster=self._cluster_name,
                service=service_name,
                desiredCount=0
            )
            
            # Delete the service
            self._ecs.delete_service(
                cluster=self._cluster_name,
                service=service_name
            )
            
            logger.debug(f"Cleaned up ECS service {service_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServiceNotFoundException':
                logger.debug(f"ECS service {service_name} already deleted")
            else:
                logger.warning(f"Error cleaning up ECS service: {str(e)}")
    
    def _deserialize_application(self, item: Dict[str, Any]) -> Application:
        """
        Convert DynamoDB item to Application aggregate.
        
        Args:
            item: DynamoDB item dictionary
            
        Returns:
            Deserialized Application aggregate
        """
        # This is a simplified deserialization
        # In a real implementation, you would need to properly reconstruct
        # all value objects and handle the aggregate state correctly
        
        # For now, return a placeholder that would need proper implementation
        from ..core.domain.models import ResourceRequirements, ScalingConfiguration, ScalingStrategy
        
        resource_req_data = json.loads(item['resource_requirements']['S'])
        scaling_config_data = json.loads(item['scaling_config']['S'])
        
        # Create value objects
        resource_requirements = ResourceRequirements(
            cpu_cores=resource_req_data['cpu_cores'],
            memory_mb=resource_req_data['memory_mb'],
            storage_gb=resource_req_data['storage_gb'],
            network_bandwidth_mbps=resource_req_data.get('network_bandwidth_mbps'),
            gpu_count=resource_req_data.get('gpu_count')
        )
        
        scaling_config = ScalingConfiguration(
            strategy=ScalingStrategy(scaling_config_data['strategy']),
            min_instances=scaling_config_data['min_instances'],
            max_instances=scaling_config_data['max_instances'],
            target_cpu_utilization=scaling_config_data.get('target_cpu_utilization'),
            target_memory_utilization=scaling_config_data.get('target_memory_utilization'),
            scale_up_cooldown_seconds=scaling_config_data.get('scale_up_cooldown_seconds', 300),
            scale_down_cooldown_seconds=scaling_config_data.get('scale_down_cooldown_seconds', 300),
            custom_metrics=scaling_config_data.get('custom_metrics')
        )
        
        # Create application (this would need proper aggregate reconstruction)
        application = Application(
            application_id=ApplicationId(UUID(item['id']['S'])),
            name=item['name']['S'],
            user_id=UserId(item['user_id']['S']),
            resource_requirements=resource_requirements,
            scaling_config=scaling_config
        )
        
        # Set additional state (this is a simplified approach)
        application._status = ApplicationStatus(item['status']['S'])
        application._current_instance_count = int(item['current_instance_count']['N'])
        application._version = int(item['version']['N'])
        
        return application


class ConcurrencyError(Exception):
    """Exception raised when optimistic concurrency control fails"""
    pass


class InfrastructureError(Exception):
    """Exception raised when infrastructure operations fail"""
    pass
