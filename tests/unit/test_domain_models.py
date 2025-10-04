"""
Unit Tests for Domain Models

This module contains comprehensive unit tests for the core domain models
of the AI-native PaaS platform. Tests cover business logic, validation,
event generation, and aggregate behavior.

Test Categories:
- Value object validation and behavior
- Entity lifecycle and state transitions
- Aggregate root business logic
- Domain event generation and handling
- Error conditions and edge cases
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from unittest.mock import Mock, patch

from src.core.domain.models import (
    # Value Objects
    UserId, ApplicationId, ResourceRequirements, ScalingConfiguration,
    PluginId, PluginVersion,
    
    # Enums
    ApplicationStatus, ScalingStrategy, EventType, PluginStatus,
    
    # Entities and Aggregates
    Application, Plugin,
    
    # Events
    DomainEvent, ApplicationCreatedEvent, ApplicationScaledEvent
)


class TestValueObjects:
    """Test suite for value objects validation and behavior"""
    
    def test_user_id_creation_valid(self):
        """Test that UserId can be created with valid string"""
        user_id = UserId("user123")
        assert user_id.value == "user123"
    
    def test_user_id_creation_invalid_empty(self):
        """Test that UserId raises error for empty string"""
        with pytest.raises(ValueError, match="UserId must be a non-empty string"):
            UserId("")
    
    def test_user_id_creation_invalid_none(self):
        """Test that UserId raises error for None value"""
        with pytest.raises(ValueError, match="UserId must be a non-empty string"):
            UserId(None)
    
    def test_application_id_creation_valid(self):
        """Test that ApplicationId can be created with valid UUID"""
        uuid_val = uuid4()
        app_id = ApplicationId(uuid_val)
        assert app_id.value == uuid_val
    
    def test_application_id_creation_invalid(self):
        """Test that ApplicationId raises error for non-UUID value"""
        with pytest.raises(ValueError, match="ApplicationId must be a UUID"):
            ApplicationId("not-a-uuid")
    
    def test_application_id_generate(self):
        """Test that ApplicationId.generate() creates valid UUID"""
        app_id = ApplicationId.generate()
        assert isinstance(app_id.value, UUID)
    
    def test_resource_requirements_creation_valid(self):
        """Test ResourceRequirements creation with valid values"""
        resources = ResourceRequirements(
            cpu_cores=2.0,
            memory_mb=4096,
            storage_gb=20,
            network_bandwidth_mbps=100,
            gpu_count=1
        )
        
        assert resources.cpu_cores == 2.0
        assert resources.memory_mb == 4096
        assert resources.storage_gb == 20
        assert resources.network_bandwidth_mbps == 100
        assert resources.gpu_count == 1
    
    def test_resource_requirements_creation_minimal(self):
        """Test ResourceRequirements creation with minimal required values"""
        resources = ResourceRequirements(
            cpu_cores=0.5,
            memory_mb=512,
            storage_gb=10
        )
        
        assert resources.cpu_cores == 0.5
        assert resources.memory_mb == 512
        assert resources.storage_gb == 10
        assert resources.network_bandwidth_mbps is None
        assert resources.gpu_count is None
    
    def test_resource_requirements_validation_negative_cpu(self):
        """Test ResourceRequirements validation for negative CPU"""
        with pytest.raises(ValueError, match="CPU cores must be positive"):
            ResourceRequirements(cpu_cores=-1.0, memory_mb=512, storage_gb=10)
    
    def test_resource_requirements_validation_zero_memory(self):
        """Test ResourceRequirements validation for zero memory"""
        with pytest.raises(ValueError, match="Memory must be positive"):
            ResourceRequirements(cpu_cores=1.0, memory_mb=0, storage_gb=10)
    
    def test_resource_requirements_validation_negative_storage(self):
        """Test ResourceRequirements validation for negative storage"""
        with pytest.raises(ValueError, match="Storage must be positive"):
            ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=-5)
    
    def test_resource_requirements_scale(self):
        """Test ResourceRequirements scaling functionality"""
        original = ResourceRequirements(
            cpu_cores=2.0,
            memory_mb=4096,
            storage_gb=20,
            network_bandwidth_mbps=100,
            gpu_count=2
        )
        
        scaled = original.scale(2.0)
        
        assert scaled.cpu_cores == 4.0
        assert scaled.memory_mb == 8192
        assert scaled.storage_gb == 40
        assert scaled.network_bandwidth_mbps == 200
        assert scaled.gpu_count == 4
    
    def test_scaling_configuration_creation_valid(self):
        """Test ScalingConfiguration creation with valid values"""
        config = ScalingConfiguration(
            strategy=ScalingStrategy.PREDICTIVE,
            min_instances=1,
            max_instances=10,
            target_cpu_utilization=70.0,
            target_memory_utilization=80.0,
            scale_up_cooldown_seconds=300,
            scale_down_cooldown_seconds=600
        )
        
        assert config.strategy == ScalingStrategy.PREDICTIVE
        assert config.min_instances == 1
        assert config.max_instances == 10
        assert config.target_cpu_utilization == 70.0
        assert config.target_memory_utilization == 80.0
        assert config.scale_up_cooldown_seconds == 300
        assert config.scale_down_cooldown_seconds == 600
    
    def test_scaling_configuration_validation_min_instances(self):
        """Test ScalingConfiguration validation for minimum instances"""
        with pytest.raises(ValueError, match="Minimum instances must be at least 1"):
            ScalingConfiguration(
                strategy=ScalingStrategy.MANUAL,
                min_instances=0,
                max_instances=5
            )
    
    def test_scaling_configuration_validation_max_less_than_min(self):
        """Test ScalingConfiguration validation for max < min instances"""
        with pytest.raises(ValueError, match="Maximum instances must be >= minimum instances"):
            ScalingConfiguration(
                strategy=ScalingStrategy.MANUAL,
                min_instances=5,
                max_instances=3
            )
    
    def test_scaling_configuration_validation_cpu_utilization_bounds(self):
        """Test ScalingConfiguration validation for CPU utilization bounds"""
        with pytest.raises(ValueError, match="Target CPU utilization must be between 0 and 100"):
            ScalingConfiguration(
                strategy=ScalingStrategy.REACTIVE,
                min_instances=1,
                max_instances=5,
                target_cpu_utilization=150.0
            )
    
    def test_plugin_version_creation_valid(self):
        """Test PluginVersion creation with valid semantic version"""
        version = PluginVersion(1, 2, 3)
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert str(version) == "1.2.3"
    
    def test_plugin_version_from_string_valid(self):
        """Test PluginVersion.from_string() with valid version string"""
        version = PluginVersion.from_string("2.1.0")
        assert version.major == 2
        assert version.minor == 1
        assert version.patch == 0
    
    def test_plugin_version_from_string_invalid(self):
        """Test PluginVersion.from_string() with invalid version string"""
        with pytest.raises(ValueError, match="Invalid version string"):
            PluginVersion.from_string("1.2")
    
    def test_plugin_version_compatibility(self):
        """Test PluginVersion compatibility checking"""
        v1_2_3 = PluginVersion(1, 2, 3)
        v1_3_0 = PluginVersion(1, 3, 0)
        v2_0_0 = PluginVersion(2, 0, 0)
        
        assert v1_2_3.is_compatible_with(v1_3_0)  # Same major version
        assert not v1_2_3.is_compatible_with(v2_0_0)  # Different major version


class TestDomainEvents:
    """Test suite for domain events creation and serialization"""
    
    def test_domain_event_creation(self):
        """Test basic DomainEvent creation"""
        aggregate_id = uuid4()
        event = DomainEvent(aggregate_id=aggregate_id, event_type=EventType.APPLICATION_CREATED)
        
        assert event.aggregate_id == aggregate_id
        assert event.event_type == EventType.APPLICATION_CREATED
        assert isinstance(event.event_id, UUID)
        assert isinstance(event.timestamp, datetime)
        assert event.version == 1
        assert event.metadata == {}
    
    def test_domain_event_to_dict(self):
        """Test DomainEvent serialization to dictionary"""
        aggregate_id = uuid4()
        event = DomainEvent(
            aggregate_id=aggregate_id,
            event_type=EventType.APPLICATION_CREATED,
            metadata={'test': 'value'}
        )
        
        event_dict = event.to_dict()
        
        assert event_dict['aggregate_id'] == str(aggregate_id)
        assert event_dict['event_id'] == str(event.event_id)
        assert 'timestamp' in event_dict
        assert event_dict['version'] == 1
        assert event_dict['metadata'] == {'test': 'value'}
        assert 'data' in event_dict
    
    def test_application_created_event(self):
        """Test ApplicationCreatedEvent creation and data"""
        app_id = uuid4()
        user_id = UserId("user123")
        resources = ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=10)
        
        event = ApplicationCreatedEvent(
            aggregate_id=app_id,
            application_name="test-app",
            user_id=user_id,
            resource_requirements=resources
        )
        
        assert event.event_type == EventType.APPLICATION_CREATED
        assert event.application_name == "test-app"
        assert event.user_id == user_id
        assert event.resource_requirements == resources
        
        event_data = event._get_event_data()
        assert event_data['application_name'] == "test-app"
        assert event_data['user_id'] == "user123"
        assert 'resource_requirements' in event_data
    
    def test_application_scaled_event(self):
        """Test ApplicationScaledEvent creation and data"""
        app_id = uuid4()
        
        event = ApplicationScaledEvent(
            aggregate_id=app_id,
            previous_instance_count=2,
            new_instance_count=4,
            scaling_reason="High CPU usage",
            ai_prediction_confidence=0.85
        )
        
        assert event.event_type == EventType.APPLICATION_SCALED
        assert event.previous_instance_count == 2
        assert event.new_instance_count == 4
        assert event.scaling_reason == "High CPU usage"
        assert event.ai_prediction_confidence == 0.85
        
        event_data = event._get_event_data()
        assert event_data['previous_instance_count'] == 2
        assert event_data['new_instance_count'] == 4
        assert event_data['scaling_reason'] == "High CPU usage"
        assert event_data['ai_prediction_confidence'] == 0.85


class TestApplicationAggregate:
    """Test suite for Application aggregate root behavior"""
    
    def create_test_application(self) -> Application:
        """Helper method to create a test application"""
        return Application(
            application_id=ApplicationId.generate(),
            name="test-app",
            user_id=UserId("user123"),
            resource_requirements=ResourceRequirements(
                cpu_cores=2.0,
                memory_mb=4096,
                storage_gb=20
            ),
            scaling_config=ScalingConfiguration(
                strategy=ScalingStrategy.PREDICTIVE,
                min_instances=1,
                max_instances=10
            )
        )
    
    def test_application_creation(self):
        """Test Application aggregate creation"""
        app_id = ApplicationId.generate()
        user_id = UserId("user123")
        resources = ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=10)
        scaling_config = ScalingConfiguration(
            strategy=ScalingStrategy.MANUAL,
            min_instances=1,
            max_instances=5
        )
        
        app = Application(
            application_id=app_id,
            name="test-app",
            user_id=user_id,
            resource_requirements=resources,
            scaling_config=scaling_config
        )
        
        assert app.id == app_id
        assert app.name == "test-app"
        assert app.user_id == user_id
        assert app.status == ApplicationStatus.PENDING
        assert app.current_instance_count == 1  # Should be min_instances
        assert app.resource_requirements == resources
        assert app.scaling_config == scaling_config
        assert app.version == 1
        
        # Check that creation event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.APPLICATION_CREATED
    
    def test_application_creation_invalid_name(self):
        """Test Application creation with invalid name"""
        with pytest.raises(ValueError, match="Application name must be a non-empty string"):
            Application(
                application_id=ApplicationId.generate(),
                name="",
                user_id=UserId("user123"),
                resource_requirements=ResourceRequirements(cpu_cores=1.0, memory_mb=512, storage_gb=10),
                scaling_config=ScalingConfiguration(
                    strategy=ScalingStrategy.MANUAL,
                    min_instances=1,
                    max_instances=5
                )
            )
    
    def test_application_deploy(self):
        """Test Application deployment state transition"""
        app = self.create_test_application()
        
        # Clear creation events for clean test
        app.mark_events_as_committed()
        
        app.deploy()
        
        assert app.status == ApplicationStatus.DEPLOYING
        assert app.version == 2
        
        # Check deployment event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.DEPLOYMENT_STARTED
    
    def test_application_deploy_invalid_status(self):
        """Test Application deployment from invalid status"""
        app = self.create_test_application()
        app._status = ApplicationStatus.RUNNING  # Set to invalid status for deployment
        
        with pytest.raises(ValueError, match="Cannot deploy application in running status"):
            app.deploy()
    
    def test_application_mark_as_running(self):
        """Test marking application as running after deployment"""
        app = self.create_test_application()
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_events_as_committed()  # Clear previous events
        
        app.mark_as_running()
        
        assert app.status == ApplicationStatus.RUNNING
        assert app.version == 3
        
        # Check completion event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.DEPLOYMENT_COMPLETED
    
    def test_application_scale_up(self):
        """Test scaling application up"""
        app = self.create_test_application()
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_as_running()  # Then mark as running
        app.mark_events_as_committed()  # Clear previous events
        
        app.scale(new_instance_count=5, reason="High CPU usage", ai_confidence=0.9)
        
        assert app.current_instance_count == 5
        assert app.status == ApplicationStatus.SCALING
        assert app.version == 4
        
        # Check scaling event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        scaling_event = events[0]
        assert scaling_event.event_type == EventType.APPLICATION_SCALED
        assert scaling_event.previous_instance_count == 1
        assert scaling_event.new_instance_count == 5
        assert scaling_event.scaling_reason == "High CPU usage"
        assert scaling_event.ai_prediction_confidence == 0.9
    
    def test_application_scale_down(self):
        """Test scaling application down"""
        app = self.create_test_application()
        app._current_instance_count = 5  # Set current count to 5
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_as_running()
        app.mark_events_as_committed()
        
        app.scale(new_instance_count=2, reason="Low traffic")
        
        assert app.current_instance_count == 2
        assert app.status == ApplicationStatus.SCALING
    
    def test_application_scale_below_minimum(self):
        """Test scaling below minimum instances"""
        app = self.create_test_application()
        
        with pytest.raises(ValueError, match="Cannot scale below minimum instances"):
            app.scale(new_instance_count=0, reason="Test")
    
    def test_application_scale_above_maximum(self):
        """Test scaling above maximum instances"""
        app = self.create_test_application()
        
        with pytest.raises(ValueError, match="Cannot scale above maximum instances"):
            app.scale(new_instance_count=15, reason="Test")
    
    def test_application_scale_no_change(self):
        """Test scaling to same instance count (no-op)"""
        app = self.create_test_application()
        app.mark_events_as_committed()
        
        app.scale(new_instance_count=1, reason="No change")
        
        # Should not generate events or change version
        assert len(app.get_uncommitted_events()) == 0
        assert app.version == 1
    
    def test_application_update_resources(self):
        """Test updating application resource requirements"""
        app = self.create_test_application()
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_as_running()
        app.mark_events_as_committed()
        
        new_resources = ResourceRequirements(
            cpu_cores=4.0,
            memory_mb=8192,
            storage_gb=40
        )
        
        app.update_resource_requirements(new_resources)
        
        assert app.resource_requirements == new_resources
        assert app.version == 4
        
        # Check update event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.APPLICATION_UPDATED
    
    def test_application_update_resources_invalid_status(self):
        """Test updating resources from invalid status"""
        app = self.create_test_application()
        # Keep in PENDING status
        
        new_resources = ResourceRequirements(cpu_cores=4.0, memory_mb=8192, storage_gb=40)
        
        with pytest.raises(ValueError, match="Cannot update resources while application is pending"):
            app.update_resource_requirements(new_resources)
    
    def test_application_stop(self):
        """Test stopping a running application"""
        app = self.create_test_application()
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_as_running()
        app.mark_events_as_committed()
        
        app.stop()
        
        assert app.status == ApplicationStatus.STOPPING
        assert app.version == 4
        
        # Check stop event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.APPLICATION_UPDATED
    
    def test_application_mark_as_stopped(self):
        """Test marking application as stopped"""
        app = self.create_test_application()
        app.deploy()  # First deploy to set to DEPLOYING status
        app.mark_as_running()
        app.stop()
        
        app.mark_as_stopped()
        
        assert app.status == ApplicationStatus.STOPPED
        assert app.current_instance_count == 0
    
    def test_application_mark_as_failed(self):
        """Test marking application as failed"""
        app = self.create_test_application()
        app.mark_events_as_committed()
        
        app.mark_as_failed("Deployment timeout")
        
        assert app.status == ApplicationStatus.FAILED
        
        # Check error event was raised
        events = app.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.ERROR_OCCURRED
        assert events[0].metadata['error_details'] == "Deployment timeout"
    
    def test_application_to_dict(self):
        """Test Application serialization to dictionary"""
        app = self.create_test_application()
        app_dict = app.to_dict()
        
        assert app_dict['id'] == str(app.id.value)
        assert app_dict['name'] == app.name
        assert app_dict['user_id'] == app.user_id.value
        assert app_dict['status'] == app.status.value
        assert app_dict['current_instance_count'] == app.current_instance_count
        assert 'resource_requirements' in app_dict
        assert 'scaling_config' in app_dict
        assert 'created_at' in app_dict
        assert 'updated_at' in app_dict
        assert app_dict['version'] == app.version
    
    def test_application_event_management(self):
        """Test application event management (commit/uncommitted)"""
        app = self.create_test_application()
        
        # Should have creation event
        events = app.get_uncommitted_events()
        assert len(events) == 1
        
        # Mark events as committed
        app.mark_events_as_committed()
        assert len(app.get_uncommitted_events()) == 0
        
        # Perform operation that generates event
        app.deploy()
        assert len(app.get_uncommitted_events()) == 1
        
        # Mark as committed again
        app.mark_events_as_committed()
        assert len(app.get_uncommitted_events()) == 0


class TestPluginEntity:
    """Test suite for Plugin entity behavior"""
    
    def create_test_plugin(self) -> Plugin:
        """Helper method to create a test plugin"""
        return Plugin(
            plugin_id=PluginId("test-plugin"),
            name="Test Plugin",
            version=PluginVersion(1, 0, 0),
            description="A test plugin for unit testing",
            author="Test Author",
            application_id=ApplicationId.generate()
        )
    
    def test_plugin_creation(self):
        """Test Plugin entity creation"""
        plugin_id = PluginId("test-plugin")
        version = PluginVersion(1, 2, 3)
        app_id = ApplicationId.generate()
        
        plugin = Plugin(
            plugin_id=plugin_id,
            name="Test Plugin",
            version=version,
            description="Test description",
            author="Test Author",
            application_id=app_id
        )
        
        assert plugin.id == plugin_id
        assert plugin.name == "Test Plugin"
        assert plugin.version == version
        assert plugin.status == PluginStatus.PENDING
        assert plugin.application_id == app_id
        assert isinstance(plugin.configuration, dict)
        assert len(plugin.configuration) == 0
        
        # Check installation event was raised
        events = plugin.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].event_type == EventType.PLUGIN_INSTALLED
    
    def test_plugin_creation_invalid_name(self):
        """Test Plugin creation with invalid name"""
        with pytest.raises(ValueError, match="Plugin name must be a non-empty string"):
            Plugin(
                plugin_id=PluginId("test"),
                name="",
                version=PluginVersion(1, 0, 0),
                description="Test",
                author="Author",
                application_id=ApplicationId.generate()
            )
    
    def test_plugin_activate(self):
        """Test plugin activation"""
        plugin = self.create_test_plugin()
        plugin._status = PluginStatus.INACTIVE  # Set to inactive first
        
        plugin.activate()
        
        assert plugin.status == PluginStatus.ACTIVE
    
    def test_plugin_activate_invalid_status(self):
        """Test plugin activation from invalid status"""
        plugin = self.create_test_plugin()
        # Keep in PENDING status
        
        with pytest.raises(ValueError, match="Cannot activate plugin in pending status"):
            plugin.activate()
    
    def test_plugin_deactivate(self):
        """Test plugin deactivation"""
        plugin = self.create_test_plugin()
        plugin._status = PluginStatus.ACTIVE  # Set to active first
        
        plugin.deactivate()
        
        assert plugin.status == PluginStatus.INACTIVE
    
    def test_plugin_deactivate_invalid_status(self):
        """Test plugin deactivation from invalid status"""
        plugin = self.create_test_plugin()
        # Keep in PENDING status
        
        with pytest.raises(ValueError, match="Cannot deactivate plugin in pending status"):
            plugin.deactivate()
    
    def test_plugin_update_configuration(self):
        """Test plugin configuration update"""
        plugin = self.create_test_plugin()
        
        new_config = {
            'setting1': 'value1',
            'setting2': 42,
            'setting3': True
        }
        
        plugin.update_configuration(new_config)
        
        assert plugin.configuration == new_config
    
    def test_plugin_update_resource_usage(self):
        """Test plugin resource usage update"""
        plugin = self.create_test_plugin()
        
        usage_metrics = {
            'cpu_usage': 25.5,
            'memory_usage': 128.0,
            'network_io': 1024.0
        }
        
        plugin.update_resource_usage(usage_metrics)
        
        assert plugin.resource_usage == usage_metrics
    
    def test_plugin_to_dict(self):
        """Test Plugin serialization to dictionary"""
        plugin = self.create_test_plugin()
        plugin_dict = plugin.to_dict()
        
        assert plugin_dict['id'] == plugin.id.value
        assert plugin_dict['name'] == plugin.name
        assert plugin_dict['version'] == str(plugin.version)
        assert plugin_dict['description'] == "A test plugin for unit testing"
        assert plugin_dict['author'] == "Test Author"
        assert plugin_dict['application_id'] == str(plugin.application_id.value)
        assert plugin_dict['status'] == plugin.status.value
        assert 'configuration' in plugin_dict
        assert 'resource_usage' in plugin_dict
        assert 'installed_at' in plugin_dict
        assert 'updated_at' in plugin_dict


# Test fixtures and utilities
@pytest.fixture
def sample_application():
    """Fixture providing a sample application for tests"""
    return Application(
        application_id=ApplicationId.generate(),
        name="sample-app",
        user_id=UserId("sample-user"),
        resource_requirements=ResourceRequirements(
            cpu_cores=1.0,
            memory_mb=1024,
            storage_gb=10
        ),
        scaling_config=ScalingConfiguration(
            strategy=ScalingStrategy.PREDICTIVE,
            min_instances=1,
            max_instances=5
        )
    )


@pytest.fixture
def sample_plugin():
    """Fixture providing a sample plugin for tests"""
    return Plugin(
        plugin_id=PluginId("sample-plugin"),
        name="Sample Plugin",
        version=PluginVersion(1, 0, 0),
        description="A sample plugin for testing",
        author="Sample Author",
        application_id=ApplicationId.generate()
    )


# Integration test helpers
class TestDomainModelIntegration:
    """Integration tests for domain model interactions"""
    
    def test_application_plugin_relationship(self, sample_application, sample_plugin):
        """Test relationship between application and plugin"""
        # Plugin should reference the application
        plugin = Plugin(
            plugin_id=PluginId("app-plugin"),
            name="Application Plugin",
            version=PluginVersion(1, 0, 0),
            description="Plugin for the application",
            author="Plugin Author",
            application_id=sample_application.id
        )
        
        assert plugin.application_id == sample_application.id
        
        # Plugin events should reference the application aggregate
        events = plugin.get_uncommitted_events()
        assert len(events) == 1
        assert events[0].aggregate_id == sample_application.id.value
    
    def test_event_ordering_and_versioning(self, sample_application):
        """Test that events are properly ordered and versioned"""
        app = sample_application
        app.mark_events_as_committed()  # Clear creation event
        
        # Perform multiple operations
        app.deploy()
        app.mark_as_running()
        app.scale(new_instance_count=3, reason="Load increase")
        
        events = app.get_uncommitted_events()
        assert len(events) == 3
        
        # Events should be in chronological order
        timestamps = [event.timestamp for event in events]
        assert timestamps == sorted(timestamps)
        
        # Application version should be incremented
        assert app.version == 4  # 1 (creation) + 3 (operations)
    
    def test_aggregate_consistency(self, sample_application):
        """Test aggregate consistency during state changes"""
        app = sample_application
        initial_version = app.version
        
        # Perform operation
        app.deploy()
        
        # Version should be incremented
        assert app.version == initial_version + 1
        
        # Status should be updated
        assert app.status == ApplicationStatus.DEPLOYING
        
        # Event should be generated
        events = app.get_uncommitted_events()
        deployment_events = [e for e in events if e.event_type == EventType.DEPLOYMENT_STARTED]
        assert len(deployment_events) == 1
