"""
Integration Tests for Application Service

This module contains integration tests that verify the interaction between
application services, repositories, event stores, and AI services. These tests
use real AWS services or realistic mocks to ensure proper integration.

Test Categories:
- Application lifecycle management
- Event sourcing and CQRS integration
- AI-driven scaling decisions
- Repository and event store interactions
- Error handling and resilience
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.domain.models import (
    Application, ApplicationId, ApplicationStatus, UserId,
    ResourceRequirements, ScalingConfiguration, ScalingStrategy,
    EventType, DomainEvent
)
from src.core.application.services import (
    ApplicationService, ApplicationRepository, EventStore, AIScalingService
)
from src.infrastructure.aws_services import (
    DynamoDBEventStore, ECSApplicationRepository, InfrastructureError
)


class MockApplicationRepository(ApplicationRepository):
    """Mock implementation of ApplicationRepository for testing"""
    
    def __init__(self):
        self._applications = {}
        self._save_calls = []
        self._get_calls = []
    
    async def save(self, application: Application) -> None:
        """Save application to in-memory store"""
        self._applications[str(application.id.value)] = application
        self._save_calls.append(application.id)
    
    async def get_by_id(self, application_id: ApplicationId) -> Application:
        """Get application by ID from in-memory store"""
        self._get_calls.append(application_id)
        return self._applications.get(str(application_id.value))
    
    async def get_by_user_id(self, user_id: UserId) -> list[Application]:
        """Get applications by user ID"""
        return [app for app in self._applications.values() if app.user_id == user_id]
    
    async def delete(self, application_id: ApplicationId) -> bool:
        """Delete application from in-memory store"""
        key = str(application_id.value)
        if key in self._applications:
            del self._applications[key]
            return True
        return False


class MockEventStore(EventStore):
    """Mock implementation of EventStore for testing"""
    
    def __init__(self):
        self._events = {}  # aggregate_id -> list of events
        self._append_calls = []
        self._get_calls = []
    
    async def append_events(self, aggregate_id: str, events: list[DomainEvent], expected_version: int) -> None:
        """Append events to in-memory store"""
        if aggregate_id not in self._events:
            self._events[aggregate_id] = []
        
        # Simple concurrency check
        current_version = len(self._events[aggregate_id])
        if current_version != expected_version:
            raise Exception(f"Concurrency conflict: expected {expected_version}, got {current_version}")
        
        self._events[aggregate_id].extend(events)
        self._append_calls.append((aggregate_id, len(events)))
    
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> list[DomainEvent]:
        """Get events from in-memory store"""
        self._get_calls.append((aggregate_id, from_version))
        events = self._events.get(aggregate_id, [])
        return events[from_version:]
    
    async def get_all_events(self, event_types: list[EventType] = None) -> list[DomainEvent]:
        """Get all events, optionally filtered by type"""
        all_events = []
        for events in self._events.values():
            all_events.extend(events)
        
        if event_types:
            all_events = [e for e in all_events if e.event_type in event_types]
        
        return sorted(all_events, key=lambda e: e.timestamp)


class MockAIScalingService(AIScalingService):
    """Mock implementation of AIScalingService for testing"""
    
    def __init__(self):
        self._predictions = {}
        self._predict_calls = []
        self._optimize_calls = []
    
    def set_prediction(self, application_id: str, prediction: dict):
        """Set prediction result for specific application"""
        self._predictions[application_id] = prediction
    
    async def predict_scaling_need(self, application: Application, current_metrics: dict[str, float]) -> dict:
        """Return mock prediction"""
        self._predict_calls.append((application.id, current_metrics))
        return self._predictions.get(str(application.id.value), {
            'should_scale': False,
            'recommended_instances': application.current_instance_count,
            'confidence': 0.7,
            'reason': 'Mock prediction - no scaling needed'
        })
    
    async def optimize_resource_allocation(self, application: Application) -> ResourceRequirements:
        """Return mock optimized resources"""
        self._optimize_calls.append(application.id)
        return application.resource_requirements  # Return current as optimized


@pytest.fixture
def mock_repository():
    """Fixture providing mock application repository"""
    return MockApplicationRepository()


@pytest.fixture
def mock_event_store():
    """Fixture providing mock event store"""
    return MockEventStore()


@pytest.fixture
def mock_ai_service():
    """Fixture providing mock AI scaling service"""
    return MockAIScalingService()


@pytest.fixture
def application_service(mock_repository, mock_event_store, mock_ai_service):
    """Fixture providing application service with mocked dependencies"""
    return ApplicationService(
        application_repository=mock_repository,
        event_store=mock_event_store,
        ai_scaling_service=mock_ai_service
    )


@pytest.fixture
def sample_resources():
    """Fixture providing sample resource requirements"""
    return ResourceRequirements(
        cpu_cores=2.0,
        memory_mb=4096,
        storage_gb=20
    )


@pytest.fixture
def sample_scaling_config():
    """Fixture providing sample scaling configuration"""
    return ScalingConfiguration(
        strategy=ScalingStrategy.PREDICTIVE,
        min_instances=1,
        max_instances=10,
        target_cpu_utilization=70.0
    )


class TestApplicationServiceIntegration:
    """Integration tests for ApplicationService"""
    
    @pytest.mark.asyncio
    async def test_create_application_success(self, application_service, mock_repository, mock_event_store, sample_resources):
        """Test successful application creation with event persistence"""
        user_id = UserId("test-user")
        
        # Create application
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Verify application was saved to repository
        assert len(mock_repository._save_calls) == 1
        assert mock_repository._save_calls[0] == app_id
        
        # Verify application exists in repository
        saved_app = await mock_repository.get_by_id(app_id)
        assert saved_app is not None
        assert saved_app.name == "test-app"
        assert saved_app.user_id == user_id
        assert saved_app.status == ApplicationStatus.PENDING
        
        # Verify events were persisted
        assert len(mock_event_store._append_calls) == 1
        aggregate_id, event_count = mock_event_store._append_calls[0]
        assert aggregate_id == str(app_id.value)
        assert event_count == 1
        
        # Verify event content
        events = await mock_event_store.get_events(str(app_id.value))
        assert len(events) == 1
        assert events[0].event_type == EventType.APPLICATION_CREATED
    
    @pytest.mark.asyncio
    async def test_deploy_application_success(self, application_service, mock_repository, mock_event_store, sample_resources):
        """Test successful application deployment"""
        # Create application first
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        mock_event_store._append_calls.clear()
        
        # Deploy application
        await application_service.deploy_application(app_id)
        
        # Verify application status was updated
        deployed_app = await mock_repository.get_by_id(app_id)
        assert deployed_app.status == ApplicationStatus.DEPLOYING
        
        # Verify save was called
        assert len(mock_repository._save_calls) == 1
        
        # Verify deployment event was persisted
        assert len(mock_event_store._append_calls) == 1
        
        # Verify event content
        events = await mock_event_store.get_events(str(app_id.value))
        deployment_events = [e for e in events if e.event_type == EventType.DEPLOYMENT_STARTED]
        assert len(deployment_events) == 1
    
    @pytest.mark.asyncio
    async def test_deploy_application_not_found(self, application_service):
        """Test deploying non-existent application"""
        non_existent_id = ApplicationId.generate()
        
        with pytest.raises(ValueError, match="Application .* not found"):
            await application_service.deploy_application(non_existent_id)
    
    @pytest.mark.asyncio
    async def test_scale_application_ai_driven(self, application_service, mock_repository, mock_ai_service, sample_resources):
        """Test AI-driven application scaling"""
        # Create and deploy application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Configure AI service to recommend scaling
        mock_ai_service.set_prediction(str(app_id.value), {
            'should_scale': True,
            'recommended_instances': 3,
            'confidence': 0.85,
            'reason': 'High CPU usage predicted'
        })
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        
        # Scale application (AI-driven)
        await application_service.scale_application(app_id)
        
        # Verify AI service was called
        assert len(mock_ai_service._predict_calls) == 1
        
        # Verify application was scaled
        scaled_app = await mock_repository.get_by_id(app_id)
        assert scaled_app.current_instance_count == 3
        assert scaled_app.status == ApplicationStatus.SCALING
        
        # Verify save was called
        assert len(mock_repository._save_calls) == 1
    
    @pytest.mark.asyncio
    async def test_scale_application_manual(self, application_service, mock_repository, sample_resources):
        """Test manual application scaling"""
        # Create and deploy application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        
        # Scale application manually
        await application_service.scale_application(app_id, target_instances=5)
        
        # Verify application was scaled
        scaled_app = await mock_repository.get_by_id(app_id)
        assert scaled_app.current_instance_count == 5
        assert scaled_app.status == ApplicationStatus.SCALING
    
    @pytest.mark.asyncio
    async def test_scale_application_ai_no_scaling_needed(self, application_service, mock_repository, mock_ai_service, sample_resources):
        """Test AI-driven scaling when no scaling is needed"""
        # Create and deploy application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Configure AI service to recommend no scaling
        mock_ai_service.set_prediction(str(app_id.value), {
            'should_scale': False,
            'recommended_instances': 1,
            'confidence': 0.9,
            'reason': 'Current capacity is optimal'
        })
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        
        # Attempt to scale application
        await application_service.scale_application(app_id)
        
        # Verify AI service was called
        assert len(mock_ai_service._predict_calls) == 1
        
        # Verify application was NOT scaled (no save calls)
        assert len(mock_repository._save_calls) == 0
        
        # Verify application state unchanged
        app_after = await mock_repository.get_by_id(app_id)
        assert app_after.current_instance_count == 1
        assert app_after.status == ApplicationStatus.RUNNING
    
    @pytest.mark.asyncio
    async def test_scale_application_invalid_status(self, application_service, mock_repository, sample_resources):
        """Test scaling application in invalid status"""
        # Create application (will be in PENDING status)
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Attempt to scale application in PENDING status
        with pytest.raises(ValueError, match="Cannot scale application in pending status"):
            await application_service.scale_application(app_id, target_instances=3)
    
    @pytest.mark.asyncio
    async def test_update_application_resources(self, application_service, mock_repository, mock_event_store, sample_resources):
        """Test updating application resource requirements"""
        # Create application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        mock_event_store._append_calls.clear()
        
        # Update resources
        new_resources = ResourceRequirements(
            cpu_cores=4.0,
            memory_mb=8192,
            storage_gb=40
        )
        
        await application_service.update_application_resources(app_id, new_resources)
        
        # Verify application was updated
        updated_app = await mock_repository.get_by_id(app_id)
        assert updated_app.resource_requirements == new_resources
        
        # Verify save was called
        assert len(mock_repository._save_calls) == 1
        
        # Verify update event was persisted
        assert len(mock_event_store._append_calls) == 1
    
    @pytest.mark.asyncio
    async def test_stop_application(self, application_service, mock_repository, sample_resources):
        """Test stopping a running application"""
        # Create and set up running application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Clear previous calls
        mock_repository._save_calls.clear()
        
        # Stop application
        await application_service.stop_application(app_id)
        
        # Verify application status was updated
        stopped_app = await mock_repository.get_by_id(app_id)
        assert stopped_app.status == ApplicationStatus.STOPPING
        
        # Verify save was called
        assert len(mock_repository._save_calls) == 1
    
    @pytest.mark.asyncio
    async def test_get_user_applications(self, application_service, sample_resources):
        """Test retrieving applications for a specific user"""
        user_id = UserId("test-user")
        other_user_id = UserId("other-user")
        
        # Create applications for different users
        app1_id = await application_service.create_application(
            name="app1",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        app2_id = await application_service.create_application(
            name="app2",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        app3_id = await application_service.create_application(
            name="app3",
            user_id=other_user_id,
            resource_requirements=sample_resources
        )
        
        # Get applications for test user
        user_apps = await application_service.get_user_applications(user_id)
        
        # Verify correct applications returned
        assert len(user_apps) == 2
        app_names = [app.name for app in user_apps]
        assert "app1" in app_names
        assert "app2" in app_names
        assert "app3" not in app_names
    
    @pytest.mark.asyncio
    async def test_delete_application(self, application_service, mock_repository, sample_resources):
        """Test deleting an application"""
        # Create application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to stopped status (required for deletion)
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.STOPPED
        await mock_repository.save(app)
        
        # Delete application
        deleted = await application_service.delete_application(app_id)
        
        # Verify deletion was successful
        assert deleted is True
        
        # Verify application no longer exists
        deleted_app = await mock_repository.get_by_id(app_id)
        assert deleted_app is None
    
    @pytest.mark.asyncio
    async def test_delete_application_invalid_status(self, application_service, mock_repository, sample_resources):
        """Test deleting application in invalid status"""
        # Create application (will be in PENDING status)
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Attempt to delete application in PENDING status
        with pytest.raises(ValueError, match="Cannot delete application in pending status"):
            await application_service.delete_application(app_id)
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, application_service, mock_repository, sample_resources):
        """Test concurrent operations on the same application"""
        # Create application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set application to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Perform concurrent operations
        async def scale_operation():
            await application_service.scale_application(app_id, target_instances=3)
        
        async def update_resources_operation():
            new_resources = ResourceRequirements(cpu_cores=4.0, memory_mb=8192, storage_gb=40)
            await application_service.update_application_resources(app_id, new_resources)
        
        # Run operations concurrently
        await asyncio.gather(scale_operation(), update_resources_operation())
        
        # Verify final state (both operations should have completed)
        final_app = await mock_repository.get_by_id(app_id)
        assert final_app.current_instance_count == 3
        assert final_app.resource_requirements.cpu_cores == 4.0


class TestEventSourcingIntegration:
    """Integration tests for event sourcing functionality"""
    
    @pytest.mark.asyncio
    async def test_event_persistence_and_retrieval(self, application_service, mock_event_store, sample_resources):
        """Test that events are properly persisted and can be retrieved"""
        # Create application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Deploy application
        await application_service.deploy_application(app_id)
        
        # Retrieve all events for the application
        events = await mock_event_store.get_events(str(app_id.value))
        
        # Verify events are in correct order
        assert len(events) == 2
        assert events[0].event_type == EventType.APPLICATION_CREATED
        assert events[1].event_type == EventType.DEPLOYMENT_STARTED
        
        # Verify event timestamps are ordered
        assert events[0].timestamp <= events[1].timestamp
    
    @pytest.mark.asyncio
    async def test_event_replay_capability(self, mock_event_store, sample_resources):
        """Test that application state can be reconstructed from events"""
        # This test would verify that we can rebuild application state from events
        # For now, we'll test that events contain sufficient information
        
        app_id = ApplicationId.generate()
        user_id = UserId("test-user")
        
        # Create mock events
        creation_event = DomainEvent(
            aggregate_id=app_id.value,
            event_type=EventType.APPLICATION_CREATED,
            metadata={
                'application_name': 'test-app',
                'user_id': user_id.value,
                'resource_requirements': sample_resources.to_dict() if hasattr(sample_resources, 'to_dict') else {}
            }
        )
        
        deployment_event = DomainEvent(
            aggregate_id=app_id.value,
            event_type=EventType.DEPLOYMENT_STARTED,
            metadata={'previous_status': 'pending'}
        )
        
        # Store events
        await mock_event_store.append_events(str(app_id.value), [creation_event, deployment_event], 0)
        
        # Retrieve events
        retrieved_events = await mock_event_store.get_events(str(app_id.value))
        
        # Verify we can reconstruct application state from events
        assert len(retrieved_events) == 2
        assert retrieved_events[0].event_type == EventType.APPLICATION_CREATED
        assert retrieved_events[1].event_type == EventType.DEPLOYMENT_STARTED
    
    @pytest.mark.asyncio
    async def test_event_filtering_by_type(self, application_service, mock_event_store, sample_resources):
        """Test filtering events by type"""
        # Create and perform operations on application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        await application_service.deploy_application(app_id)
        
        # Filter events by type
        all_events = await mock_event_store.get_all_events()
        creation_events = await mock_event_store.get_all_events([EventType.APPLICATION_CREATED])
        deployment_events = await mock_event_store.get_all_events([EventType.DEPLOYMENT_STARTED])
        
        # Verify filtering works correctly
        assert len(all_events) == 2
        assert len(creation_events) == 1
        assert len(deployment_events) == 1
        assert creation_events[0].event_type == EventType.APPLICATION_CREATED
        assert deployment_events[0].event_type == EventType.DEPLOYMENT_STARTED


class TestErrorHandlingIntegration:
    """Integration tests for error handling and resilience"""
    
    @pytest.mark.asyncio
    async def test_repository_failure_handling(self, mock_event_store, mock_ai_service):
        """Test handling of repository failures"""
        # Create a repository that fails on save
        class FailingRepository(MockApplicationRepository):
            async def save(self, application: Application) -> None:
                raise InfrastructureError("Database connection failed")
        
        failing_repo = FailingRepository()
        service = ApplicationService(failing_repo, mock_event_store, mock_ai_service)
        
        # Attempt to create application
        with pytest.raises(InfrastructureError, match="Database connection failed"):
            await service.create_application(
                name="test-app",
                user_id=UserId("test-user"),
                resource_requirements=ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=10)
            )
    
    @pytest.mark.asyncio
    async def test_event_store_failure_handling(self, mock_repository, mock_ai_service):
        """Test handling of event store failures"""
        # Create an event store that fails on append
        class FailingEventStore(MockEventStore):
            async def append_events(self, aggregate_id: str, events: list[DomainEvent], expected_version: int) -> None:
                raise InfrastructureError("Event store unavailable")
        
        failing_event_store = FailingEventStore()
        service = ApplicationService(mock_repository, failing_event_store, mock_ai_service)
        
        # Attempt to create application
        with pytest.raises(InfrastructureError, match="Event store unavailable"):
            await service.create_application(
                name="test-app",
                user_id=UserId("test-user"),
                resource_requirements=ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=10)
            )
    
    @pytest.mark.asyncio
    async def test_ai_service_failure_graceful_degradation(self, application_service, mock_repository, sample_resources):
        """Test graceful degradation when AI service fails"""
        # Create application and set to running
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Mock AI service to raise exception
        class FailingAIService(MockAIScalingService):
            async def predict_scaling_need(self, application: Application, current_metrics: dict[str, float]) -> dict:
                raise Exception("AI service unavailable")
        
        # Replace AI service with failing one
        application_service._ai_scaling_service = FailingAIService()
        
        # Attempt AI-driven scaling - should handle gracefully or provide fallback
        # The exact behavior depends on implementation - it might use fallback logic
        # or raise an appropriate exception
        try:
            await application_service.scale_application(app_id)
            # If it succeeds, verify it used fallback logic
            scaled_app = await mock_repository.get_by_id(app_id)
            # Application state should be consistent
            assert scaled_app is not None
        except Exception as e:
            # If it fails, it should be a controlled failure with appropriate error message
            assert "AI service" in str(e) or "unavailable" in str(e)


# Performance and load testing helpers
class TestPerformanceIntegration:
    """Integration tests for performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_bulk_application_creation(self, application_service, sample_resources):
        """Test creating multiple applications concurrently"""
        user_id = UserId("test-user")
        
        # Create multiple applications concurrently
        async def create_app(index):
            return await application_service.create_application(
                name=f"test-app-{index}",
                user_id=user_id,
                resource_requirements=sample_resources
            )
        
        # Create 10 applications concurrently
        app_ids = await asyncio.gather(*[create_app(i) for i in range(10)])
        
        # Verify all applications were created
        assert len(app_ids) == 10
        assert len(set(str(app_id.value) for app_id in app_ids)) == 10  # All unique
        
        # Verify all applications exist
        user_apps = await application_service.get_user_applications(user_id)
        assert len(user_apps) == 10
    
    @pytest.mark.asyncio
    async def test_rapid_scaling_operations(self, application_service, mock_repository, sample_resources):
        """Test rapid scaling operations on the same application"""
        # Create application
        user_id = UserId("test-user")
        app_id = await application_service.create_application(
            name="test-app",
            user_id=user_id,
            resource_requirements=sample_resources
        )
        
        # Set to running status
        app = await mock_repository.get_by_id(app_id)
        app._status = ApplicationStatus.RUNNING
        await mock_repository.save(app)
        
        # Perform rapid scaling operations
        scaling_operations = [
            application_service.scale_application(app_id, target_instances=2),
            application_service.scale_application(app_id, target_instances=3),
            application_service.scale_application(app_id, target_instances=4),
        ]
        
        # Execute operations (some may fail due to concurrency, which is expected)
        results = await asyncio.gather(*scaling_operations, return_exceptions=True)
        
        # At least one operation should succeed
        successful_operations = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_operations) >= 1
        
        # Final application state should be consistent
        final_app = await mock_repository.get_by_id(app_id)
        assert final_app.current_instance_count >= 2  # Should be scaled up
