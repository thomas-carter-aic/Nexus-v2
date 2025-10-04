"""
Enterprise Security Manager

This module provides centralized security policy management, security controls,
and comprehensive security governance for the AI-Native PaaS Platform.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
import hashlib
import secrets

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different environments and data types"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    TOP_SECRET = "top_secret"


class PolicyType(Enum):
    """Types of security policies"""
    ACCESS_CONTROL = "access_control"
    DATA_PROTECTION = "data_protection"
    NETWORK_SECURITY = "network_security"
    ENCRYPTION = "encryption"
    AUDIT_LOGGING = "audit_logging"
    INCIDENT_RESPONSE = "incident_response"
    COMPLIANCE = "compliance"
    THREAT_DETECTION = "threat_detection"


class SecurityAction(Enum):
    """Security actions that can be taken"""
    ALLOW = "allow"
    DENY = "deny"
    MONITOR = "monitor"
    ALERT = "alert"
    BLOCK = "block"
    QUARANTINE = "quarantine"


@dataclass
class SecurityPolicy:
    """Security policy definition"""
    policy_id: str
    name: str
    description: str
    policy_type: PolicyType
    security_level: SecurityLevel
    rules: List[Dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'policy_id': self.policy_id,
            'name': self.name,
            'description': self.description,
            'policy_type': self.policy_type.value,
            'security_level': self.security_level.value,
            'rules': self.rules,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version
        }


@dataclass
class SecurityEvent:
    """Security event for monitoring and alerting"""
    event_id: str
    event_type: str
    severity: str
    source: str
    target: str
    action: SecurityAction
    timestamp: datetime = field(default_factory=datetime.utcnow)
    details: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'severity': self.severity,
            'source': self.source,
            'target': self.target,
            'action': self.action.value,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details,
            'user_id': self.user_id,
            'session_id': self.session_id
        }


@dataclass
class SecurityMetrics:
    """Security metrics and KPIs"""
    total_policies: int
    active_policies: int
    security_events_24h: int
    threats_detected: int
    incidents_resolved: int
    compliance_score: float
    last_security_scan: datetime
    vulnerabilities_found: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_policies': self.total_policies,
            'active_policies': self.active_policies,
            'security_events_24h': self.security_events_24h,
            'threats_detected': self.threats_detected,
            'incidents_resolved': self.incidents_resolved,
            'compliance_score': self.compliance_score,
            'last_security_scan': self.last_security_scan.isoformat(),
            'vulnerabilities_found': self.vulnerabilities_found
        }


class SecurityManager:
    """
    Centralized security management system for enterprise-grade security controls
    """
    
    def __init__(self):
        self.policies: Dict[str, SecurityPolicy] = {}
        self.security_events: List[SecurityEvent] = []
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.security_rules: Dict[str, callable] = {}
        self.threat_indicators: Set[str] = set()
        self._initialize_default_policies()
        
    def _initialize_default_policies(self):
        """Initialize default security policies"""
        
        # Data Protection Policy
        data_protection_policy = SecurityPolicy(
            policy_id="dp-001",
            name="Data Protection Policy",
            description="Comprehensive data protection and privacy controls",
            policy_type=PolicyType.DATA_PROTECTION,
            security_level=SecurityLevel.CONFIDENTIAL,
            rules=[
                {
                    "rule_id": "dp-001-01",
                    "name": "PII Encryption",
                    "description": "All PII must be encrypted at rest and in transit",
                    "condition": "data_type == 'PII'",
                    "action": "encrypt",
                    "encryption_algorithm": "AES-256-GCM"
                },
                {
                    "rule_id": "dp-001-02",
                    "name": "Data Retention",
                    "description": "Automatic data deletion after retention period",
                    "condition": "age > retention_period",
                    "action": "delete",
                    "retention_days": 2555  # 7 years for compliance
                },
                {
                    "rule_id": "dp-001-03",
                    "name": "Data Access Logging",
                    "description": "Log all access to sensitive data",
                    "condition": "security_level >= 'confidential'",
                    "action": "log",
                    "log_level": "INFO"
                }
            ]
        )
        self.policies[data_protection_policy.policy_id] = data_protection_policy
        
        # Access Control Policy
        access_control_policy = SecurityPolicy(
            policy_id="ac-001",
            name="Access Control Policy",
            description="Role-based access control with principle of least privilege",
            policy_type=PolicyType.ACCESS_CONTROL,
            security_level=SecurityLevel.RESTRICTED,
            rules=[
                {
                    "rule_id": "ac-001-01",
                    "name": "Multi-Factor Authentication",
                    "description": "MFA required for admin access",
                    "condition": "role == 'admin' OR security_level >= 'restricted'",
                    "action": "require_mfa",
                    "mfa_methods": ["totp", "sms", "hardware_key"]
                },
                {
                    "rule_id": "ac-001-02",
                    "name": "Session Timeout",
                    "description": "Automatic session timeout for security",
                    "condition": "session_idle_time > timeout_threshold",
                    "action": "terminate_session",
                    "timeout_minutes": 30
                },
                {
                    "rule_id": "ac-001-03",
                    "name": "Failed Login Protection",
                    "description": "Account lockout after failed login attempts",
                    "condition": "failed_login_attempts >= max_attempts",
                    "action": "lock_account",
                    "max_attempts": 5,
                    "lockout_duration_minutes": 15
                }
            ]
        )
        self.policies[access_control_policy.policy_id] = access_control_policy
        
        # Network Security Policy
        network_security_policy = SecurityPolicy(
            policy_id="ns-001",
            name="Network Security Policy",
            description="Network-level security controls and monitoring",
            policy_type=PolicyType.NETWORK_SECURITY,
            security_level=SecurityLevel.CONFIDENTIAL,
            rules=[
                {
                    "rule_id": "ns-001-01",
                    "name": "TLS Enforcement",
                    "description": "Enforce TLS 1.3 for all communications",
                    "condition": "protocol == 'HTTP'",
                    "action": "upgrade_to_https",
                    "min_tls_version": "1.3"
                },
                {
                    "rule_id": "ns-001-02",
                    "name": "IP Allowlist",
                    "description": "Restrict access to approved IP ranges",
                    "condition": "source_ip NOT IN allowlist",
                    "action": "block",
                    "allowlist": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
                },
                {
                    "rule_id": "ns-001-03",
                    "name": "DDoS Protection",
                    "description": "Rate limiting and DDoS protection",
                    "condition": "request_rate > threshold",
                    "action": "rate_limit",
                    "max_requests_per_minute": 1000
                }
            ]
        )
        self.policies[network_security_policy.policy_id] = network_security_policy
        
    async def create_policy(self, policy: SecurityPolicy) -> str:
        """Create a new security policy"""
        policy.policy_id = policy.policy_id or str(uuid4())
        policy.created_at = datetime.utcnow()
        policy.updated_at = datetime.utcnow()
        
        self.policies[policy.policy_id] = policy
        
        # Log policy creation
        await self._log_security_event(
            event_type="policy_created",
            severity="INFO",
            source="security_manager",
            target=policy.policy_id,
            action=SecurityAction.ALLOW,
            details={
                'policy_name': policy.name,
                'policy_type': policy.policy_type.value,
                'security_level': policy.security_level.value
            }
        )
        
        logger.info(f"Created security policy: {policy.name} ({policy.policy_id})")
        return policy.policy_id
        
    async def update_policy(self, policy_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing security policy"""
        if policy_id not in self.policies:
            return False
            
        policy = self.policies[policy_id]
        
        for key, value in updates.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
                
        policy.updated_at = datetime.utcnow()
        
        # Log policy update
        await self._log_security_event(
            event_type="policy_updated",
            severity="INFO",
            source="security_manager",
            target=policy_id,
            action=SecurityAction.ALLOW,
            details={'updates': updates}
        )
        
        return True
        
    async def delete_policy(self, policy_id: str) -> bool:
        """Delete a security policy"""
        if policy_id not in self.policies:
            return False
            
        policy = self.policies.pop(policy_id)
        
        # Log policy deletion
        await self._log_security_event(
            event_type="policy_deleted",
            severity="WARNING",
            source="security_manager",
            target=policy_id,
            action=SecurityAction.ALLOW,
            details={'policy_name': policy.name}
        )
        
        return True
        
    async def evaluate_access(self, user_id: str, resource: str, 
                            action: str, context: Dict[str, Any]) -> bool:
        """Evaluate access request against security policies"""
        
        # Log access attempt
        await self._log_security_event(
            event_type="access_attempt",
            severity="INFO",
            source=user_id,
            target=resource,
            action=SecurityAction.MONITOR,
            details={
                'requested_action': action,
                'context': context
            },
            user_id=user_id
        )
        
        # Check access control policies
        for policy in self.policies.values():
            if policy.policy_type == PolicyType.ACCESS_CONTROL and policy.enabled:
                if not await self._evaluate_policy_rules(policy, user_id, resource, action, context):
                    # Log access denied
                    await self._log_security_event(
                        event_type="access_denied",
                        severity="WARNING",
                        source=user_id,
                        target=resource,
                        action=SecurityAction.DENY,
                        details={
                            'policy_id': policy.policy_id,
                            'requested_action': action
                        },
                        user_id=user_id
                    )
                    return False
                    
        # Log access granted
        await self._log_security_event(
            event_type="access_granted",
            severity="INFO",
            source=user_id,
            target=resource,
            action=SecurityAction.ALLOW,
            details={'requested_action': action},
            user_id=user_id
        )
        
        return True
        
    async def _evaluate_policy_rules(self, policy: SecurityPolicy, 
                                   user_id: str, resource: str, 
                                   action: str, context: Dict[str, Any]) -> bool:
        """Evaluate policy rules against access request"""
        
        for rule in policy.rules:
            condition = rule.get('condition', '')
            
            # Simple condition evaluation (in production, use a proper rule engine)
            if 'role == \'admin\'' in condition:
                user_role = context.get('user_role', '')
                if user_role == 'admin':
                    # Check if MFA is required
                    if rule.get('action') == 'require_mfa':
                        mfa_verified = context.get('mfa_verified', False)
                        if not mfa_verified:
                            return False
                            
            elif 'security_level >=' in condition:
                required_level = condition.split('>=')[1].strip().strip("'\"")
                resource_level = context.get('security_level', 'public')
                
                # Simple security level comparison
                levels = ['public', 'internal', 'confidential', 'restricted', 'top_secret']
                if levels.index(resource_level) < levels.index(required_level):
                    return False
                    
        return True
        
    async def detect_threats(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect security threats from events"""
        threats = []
        
        # Analyze events for threat patterns
        for event in events:
            # Check for brute force attacks
            if event.get('event_type') == 'login_failed':
                user_id = event.get('user_id')
                if user_id:
                    recent_failures = [
                        e for e in events 
                        if e.get('user_id') == user_id and 
                        e.get('event_type') == 'login_failed' and
                        datetime.fromisoformat(e.get('timestamp', '')) > 
                        datetime.utcnow() - timedelta(minutes=15)
                    ]
                    
                    if len(recent_failures) >= 5:
                        threats.append({
                            'threat_type': 'brute_force_attack',
                            'severity': 'HIGH',
                            'user_id': user_id,
                            'event_count': len(recent_failures),
                            'recommendation': 'Lock account and investigate'
                        })
                        
            # Check for unusual access patterns
            elif event.get('event_type') == 'access_granted':
                user_id = event.get('user_id')
                resource = event.get('target')
                
                # Check for access outside normal hours
                event_time = datetime.fromisoformat(event.get('timestamp', ''))
                if event_time.hour < 6 or event_time.hour > 22:
                    threats.append({
                        'threat_type': 'unusual_access_time',
                        'severity': 'MEDIUM',
                        'user_id': user_id,
                        'resource': resource,
                        'access_time': event_time.isoformat(),
                        'recommendation': 'Verify legitimate access'
                    })
                    
        return threats
        
    async def generate_security_report(self, start_date: datetime, 
                                     end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        
        # Filter events by date range
        filtered_events = [
            event for event in self.security_events
            if start_date <= event.timestamp <= end_date
        ]
        
        # Calculate metrics
        total_events = len(filtered_events)
        access_attempts = len([e for e in filtered_events if e.event_type == 'access_attempt'])
        access_denied = len([e for e in filtered_events if e.event_type == 'access_denied'])
        security_violations = len([e for e in filtered_events if e.severity in ['HIGH', 'CRITICAL']])
        
        # Detect threats
        threat_events = [event.to_dict() for event in filtered_events]
        threats = await self.detect_threats(threat_events)
        
        # Generate report
        report = {
            'report_id': str(uuid4()),
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'summary': {
                'total_events': total_events,
                'access_attempts': access_attempts,
                'access_denied': access_denied,
                'success_rate': (access_attempts - access_denied) / access_attempts * 100 if access_attempts > 0 else 100,
                'security_violations': security_violations,
                'threats_detected': len(threats)
            },
            'policy_status': {
                'total_policies': len(self.policies),
                'active_policies': len([p for p in self.policies.values() if p.enabled]),
                'policy_types': list(set(p.policy_type.value for p in self.policies.values()))
            },
            'threats': threats,
            'top_events': [
                {
                    'event_type': event.event_type,
                    'count': len([e for e in filtered_events if e.event_type == event.event_type])
                }
                for event in filtered_events[:10]
            ],
            'recommendations': self._generate_security_recommendations(filtered_events, threats)
        }
        
        return report
        
    def _generate_security_recommendations(self, events: List[SecurityEvent], 
                                         threats: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on events and threats"""
        recommendations = []
        
        # Check for high number of access denials
        access_denied_count = len([e for e in events if e.event_type == 'access_denied'])
        if access_denied_count > 100:
            recommendations.append(
                "High number of access denials detected. Review access control policies and user permissions."
            )
            
        # Check for threats
        if len(threats) > 0:
            recommendations.append(
                f"Security threats detected ({len(threats)}). Immediate investigation and response required."
            )
            
        # Check for policy coverage
        policy_types = set(p.policy_type for p in self.policies.values())
        required_types = {PolicyType.ACCESS_CONTROL, PolicyType.DATA_PROTECTION, PolicyType.NETWORK_SECURITY}
        
        missing_types = required_types - policy_types
        if missing_types:
            recommendations.append(
                f"Missing security policies: {', '.join(t.value for t in missing_types)}. "
                "Implement comprehensive security policy coverage."
            )
            
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Security posture is good. Continue monitoring and regular policy reviews.",
                "Consider implementing additional threat detection capabilities.",
                "Regular security training for users is recommended."
            ])
            
        return recommendations
        
    async def get_security_metrics(self) -> SecurityMetrics:
        """Get current security metrics"""
        
        # Calculate metrics from current state
        recent_events = [
            event for event in self.security_events
            if event.timestamp > datetime.utcnow() - timedelta(hours=24)
        ]
        
        threats = await self.detect_threats([event.to_dict() for event in recent_events])
        
        return SecurityMetrics(
            total_policies=len(self.policies),
            active_policies=len([p for p in self.policies.values() if p.enabled]),
            security_events_24h=len(recent_events),
            threats_detected=len(threats),
            incidents_resolved=0,  # Would be tracked separately
            compliance_score=95.5,  # Would be calculated from compliance framework
            last_security_scan=datetime.utcnow() - timedelta(hours=2),
            vulnerabilities_found=0  # Would come from security scanner
        )
        
    async def _log_security_event(self, event_type: str, severity: str, 
                                source: str, target: str, action: SecurityAction,
                                details: Dict[str, Any], user_id: Optional[str] = None,
                                session_id: Optional[str] = None):
        """Log security event"""
        
        event = SecurityEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            severity=severity,
            source=source,
            target=target,
            action=action,
            details=details,
            user_id=user_id,
            session_id=session_id
        )
        
        self.security_events.append(event)
        
        # Keep only recent events in memory (last 10,000)
        if len(self.security_events) > 10000:
            self.security_events = self.security_events[-10000:]
            
        # In production, this would also write to persistent storage
        logger.info(f"Security event logged: {event_type} - {severity}")
        
    async def create_session(self, user_id: str, context: Dict[str, Any]) -> str:
        """Create secure user session"""
        session_id = secrets.token_urlsafe(32)
        
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'context': context,
            'security_level': context.get('security_level', 'internal')
        }
        
        self.active_sessions[session_id] = session_data
        
        await self._log_security_event(
            event_type="session_created",
            severity="INFO",
            source=user_id,
            target="session_manager",
            action=SecurityAction.ALLOW,
            details={'session_id': session_id},
            user_id=user_id,
            session_id=session_id
        )
        
        return session_id
        
    async def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate and refresh user session"""
        if session_id not in self.active_sessions:
            return None
            
        session = self.active_sessions[session_id]
        
        # Check session timeout
        timeout_minutes = 30  # Default timeout
        if datetime.utcnow() - session['last_activity'] > timedelta(minutes=timeout_minutes):
            await self.terminate_session(session_id)
            return None
            
        # Update last activity
        session['last_activity'] = datetime.utcnow()
        
        return session
        
    async def terminate_session(self, session_id: str) -> bool:
        """Terminate user session"""
        if session_id not in self.active_sessions:
            return False
            
        session = self.active_sessions.pop(session_id)
        
        await self._log_security_event(
            event_type="session_terminated",
            severity="INFO",
            source=session['user_id'],
            target="session_manager",
            action=SecurityAction.ALLOW,
            details={'session_id': session_id},
            user_id=session['user_id'],
            session_id=session_id
        )
        
        return True


# Example usage
async def example_security_manager():
    """Example of using the security manager"""
    
    # Create security manager
    security_manager = SecurityManager()
    
    # Create a custom security policy
    custom_policy = SecurityPolicy(
        policy_id="custom-001",
        name="API Rate Limiting Policy",
        description="Rate limiting for API endpoints",
        policy_type=PolicyType.NETWORK_SECURITY,
        security_level=SecurityLevel.INTERNAL,
        rules=[
            {
                "rule_id": "custom-001-01",
                "name": "API Rate Limit",
                "description": "Limit API requests per user",
                "condition": "request_count > rate_limit",
                "action": "rate_limit",
                "rate_limit": 1000,
                "time_window_minutes": 60
            }
        ]
    )
    
    policy_id = await security_manager.create_policy(custom_policy)
    print(f"Created policy: {policy_id}")
    
    # Create user session
    session_id = await security_manager.create_session(
        user_id="user-123",
        context={
            'user_role': 'admin',
            'security_level': 'confidential',
            'mfa_verified': True
        }
    )
    print(f"Created session: {session_id}")
    
    # Evaluate access request
    access_granted = await security_manager.evaluate_access(
        user_id="user-123",
        resource="/api/admin/users",
        action="read",
        context={
            'user_role': 'admin',
            'security_level': 'confidential',
            'mfa_verified': True
        }
    )
    print(f"Access granted: {access_granted}")
    
    # Generate security report
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    report = await security_manager.generate_security_report(start_date, end_date)
    print(f"Security report generated with {report['summary']['total_events']} events")
    
    # Get security metrics
    metrics = await security_manager.get_security_metrics()
    print(f"Security metrics: {metrics.total_policies} policies, {metrics.security_events_24h} events in 24h")


if __name__ == "__main__":
    asyncio.run(example_security_manager())
