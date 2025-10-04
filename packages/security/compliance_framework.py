"""
Compliance Framework Module

This module provides comprehensive compliance management for major standards
including GDPR, HIPAA, SOC 2, ISO 27001, and other regulatory frameworks.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


class ComplianceStandard(Enum):
    """Supported compliance standards"""
    GDPR = "gdpr"                    # General Data Protection Regulation
    HIPAA = "hipaa"                  # Health Insurance Portability and Accountability Act
    SOC2 = "soc2"                   # Service Organization Control 2
    ISO27001 = "iso27001"           # ISO/IEC 27001 Information Security Management
    PCI_DSS = "pci_dss"             # Payment Card Industry Data Security Standard
    CCPA = "ccpa"                   # California Consumer Privacy Act
    NIST = "nist"                   # NIST Cybersecurity Framework
    FedRAMP = "fedramp"             # Federal Risk and Authorization Management Program


class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"
    NOT_APPLICABLE = "not_applicable"


class ControlType(Enum):
    """Types of compliance controls"""
    ADMINISTRATIVE = "administrative"
    TECHNICAL = "technical"
    PHYSICAL = "physical"
    OPERATIONAL = "operational"


@dataclass
class ComplianceControl:
    """Individual compliance control"""
    control_id: str
    name: str
    description: str
    standard: ComplianceStandard
    control_type: ControlType
    requirements: List[str] = field(default_factory=list)
    implementation_status: ComplianceStatus = ComplianceStatus.UNDER_REVIEW
    evidence: List[str] = field(default_factory=list)
    responsible_party: str = ""
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'control_id': self.control_id,
            'name': self.name,
            'description': self.description,
            'standard': self.standard.value,
            'control_type': self.control_type.value,
            'requirements': self.requirements,
            'implementation_status': self.implementation_status.value,
            'evidence': self.evidence,
            'responsible_party': self.responsible_party,
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'next_review': self.next_review.isoformat() if self.next_review else None
        }


@dataclass
class ComplianceReport:
    """Compliance assessment report"""
    report_id: str
    standard: ComplianceStandard
    assessment_date: datetime
    overall_status: ComplianceStatus
    compliance_score: float  # 0-100
    total_controls: int
    compliant_controls: int
    non_compliant_controls: int
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    next_assessment: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'report_id': self.report_id,
            'standard': self.standard.value,
            'assessment_date': self.assessment_date.isoformat(),
            'overall_status': self.overall_status.value,
            'compliance_score': self.compliance_score,
            'total_controls': self.total_controls,
            'compliant_controls': self.compliant_controls,
            'non_compliant_controls': self.non_compliant_controls,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'next_assessment': self.next_assessment.isoformat() if self.next_assessment else None
        }


@dataclass
class DataProcessingRecord:
    """GDPR Article 30 - Record of Processing Activities"""
    record_id: str
    controller_name: str
    contact_details: str
    purposes_of_processing: List[str]
    categories_of_data_subjects: List[str]
    categories_of_personal_data: List[str]
    recipients: List[str]
    third_country_transfers: List[str]
    retention_periods: Dict[str, str]
    security_measures: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class ComplianceFramework:
    """
    Comprehensive compliance management framework for multiple standards
    """
    
    def __init__(self):
        self.controls: Dict[str, ComplianceControl] = {}
        self.reports: List[ComplianceReport] = []
        self.data_processing_records: Dict[str, DataProcessingRecord] = {}
        self.compliance_policies: Dict[str, Dict[str, Any]] = {}
        self._initialize_compliance_controls()
        
    def _initialize_compliance_controls(self):
        """Initialize compliance controls for major standards"""
        
        # GDPR Controls
        self._initialize_gdpr_controls()
        
        # HIPAA Controls
        self._initialize_hipaa_controls()
        
        # SOC 2 Controls
        self._initialize_soc2_controls()
        
        # ISO 27001 Controls
        self._initialize_iso27001_controls()
        
    def _initialize_gdpr_controls(self):
        """Initialize GDPR compliance controls"""
        
        gdpr_controls = [
            {
                'control_id': 'GDPR-001',
                'name': 'Lawful Basis for Processing',
                'description': 'Establish and document lawful basis for processing personal data',
                'requirements': [
                    'Identify lawful basis under Article 6',
                    'Document basis for each processing activity',
                    'Inform data subjects of lawful basis'
                ]
            },
            {
                'control_id': 'GDPR-002',
                'name': 'Data Subject Rights',
                'description': 'Implement processes to handle data subject rights requests',
                'requirements': [
                    'Right to access (Article 15)',
                    'Right to rectification (Article 16)',
                    'Right to erasure (Article 17)',
                    'Right to data portability (Article 20)',
                    'Right to object (Article 21)'
                ]
            },
            {
                'control_id': 'GDPR-003',
                'name': 'Privacy by Design and Default',
                'description': 'Implement privacy by design and default principles',
                'requirements': [
                    'Data protection impact assessments',
                    'Privacy-enhancing technologies',
                    'Default privacy settings',
                    'Data minimization'
                ]
            },
            {
                'control_id': 'GDPR-004',
                'name': 'Data Breach Notification',
                'description': 'Implement data breach detection and notification procedures',
                'requirements': [
                    '72-hour notification to supervisory authority',
                    'Data subject notification when high risk',
                    'Breach register maintenance',
                    'Risk assessment procedures'
                ]
            },
            {
                'control_id': 'GDPR-005',
                'name': 'Records of Processing Activities',
                'description': 'Maintain comprehensive records of processing activities',
                'requirements': [
                    'Article 30 compliance',
                    'Controller and processor records',
                    'Regular updates and reviews',
                    'Documentation of data flows'
                ]
            }
        ]
        
        for control_data in gdpr_controls:
            control = ComplianceControl(
                control_id=control_data['control_id'],
                name=control_data['name'],
                description=control_data['description'],
                standard=ComplianceStandard.GDPR,
                control_type=ControlType.ADMINISTRATIVE,
                requirements=control_data['requirements']
            )
            self.controls[control.control_id] = control
            
    def _initialize_hipaa_controls(self):
        """Initialize HIPAA compliance controls"""
        
        hipaa_controls = [
            {
                'control_id': 'HIPAA-001',
                'name': 'Administrative Safeguards',
                'description': 'Implement administrative safeguards for PHI protection',
                'requirements': [
                    'Security officer designation',
                    'Workforce training',
                    'Access management procedures',
                    'Contingency planning'
                ]
            },
            {
                'control_id': 'HIPAA-002',
                'name': 'Physical Safeguards',
                'description': 'Implement physical safeguards for PHI protection',
                'requirements': [
                    'Facility access controls',
                    'Workstation security',
                    'Device and media controls',
                    'Physical access logging'
                ]
            },
            {
                'control_id': 'HIPAA-003',
                'name': 'Technical Safeguards',
                'description': 'Implement technical safeguards for PHI protection',
                'requirements': [
                    'Access control systems',
                    'Audit controls and logging',
                    'Integrity controls',
                    'Transmission security'
                ]
            },
            {
                'control_id': 'HIPAA-004',
                'name': 'Business Associate Agreements',
                'description': 'Manage business associate relationships and agreements',
                'requirements': [
                    'BAA execution and management',
                    'Vendor risk assessments',
                    'Subcontractor oversight',
                    'Contract compliance monitoring'
                ]
            }
        ]
        
        for control_data in hipaa_controls:
            control = ComplianceControl(
                control_id=control_data['control_id'],
                name=control_data['name'],
                description=control_data['description'],
                standard=ComplianceStandard.HIPAA,
                control_type=ControlType.ADMINISTRATIVE,
                requirements=control_data['requirements']
            )
            self.controls[control.control_id] = control
            
    def _initialize_soc2_controls(self):
        """Initialize SOC 2 compliance controls"""
        
        soc2_controls = [
            {
                'control_id': 'SOC2-001',
                'name': 'Security - Logical Access Controls',
                'description': 'Implement logical access controls to protect system resources',
                'requirements': [
                    'User access provisioning and deprovisioning',
                    'Privileged access management',
                    'Multi-factor authentication',
                    'Access reviews and certifications'
                ]
            },
            {
                'control_id': 'SOC2-002',
                'name': 'Availability - System Monitoring',
                'description': 'Monitor system availability and performance',
                'requirements': [
                    'System monitoring and alerting',
                    'Capacity planning and management',
                    'Incident response procedures',
                    'Business continuity planning'
                ]
            },
            {
                'control_id': 'SOC2-003',
                'name': 'Processing Integrity - Data Validation',
                'description': 'Ensure data processing integrity and accuracy',
                'requirements': [
                    'Data validation controls',
                    'Error detection and correction',
                    'Processing completeness checks',
                    'Data reconciliation procedures'
                ]
            },
            {
                'control_id': 'SOC2-004',
                'name': 'Confidentiality - Data Classification',
                'description': 'Classify and protect confidential information',
                'requirements': [
                    'Data classification scheme',
                    'Confidentiality agreements',
                    'Data handling procedures',
                    'Secure disposal methods'
                ]
            }
        ]
        
        for control_data in soc2_controls:
            control = ComplianceControl(
                control_id=control_data['control_id'],
                name=control_data['name'],
                description=control_data['description'],
                standard=ComplianceStandard.SOC2,
                control_type=ControlType.TECHNICAL,
                requirements=control_data['requirements']
            )
            self.controls[control.control_id] = control
            
    def _initialize_iso27001_controls(self):
        """Initialize ISO 27001 compliance controls"""
        
        iso27001_controls = [
            {
                'control_id': 'ISO27001-001',
                'name': 'Information Security Management System',
                'description': 'Establish and maintain ISMS',
                'requirements': [
                    'ISMS scope definition',
                    'Risk assessment methodology',
                    'Security policy framework',
                    'Management review processes'
                ]
            },
            {
                'control_id': 'ISO27001-002',
                'name': 'Asset Management',
                'description': 'Identify and manage information assets',
                'requirements': [
                    'Asset inventory maintenance',
                    'Asset classification and labeling',
                    'Acceptable use policies',
                    'Secure disposal procedures'
                ]
            },
            {
                'control_id': 'ISO27001-003',
                'name': 'Cryptography',
                'description': 'Implement cryptographic controls',
                'requirements': [
                    'Cryptographic policy',
                    'Key management procedures',
                    'Encryption implementation',
                    'Digital signature controls'
                ]
            },
            {
                'control_id': 'ISO27001-004',
                'name': 'Incident Management',
                'description': 'Manage information security incidents',
                'requirements': [
                    'Incident response procedures',
                    'Incident classification and escalation',
                    'Evidence collection and preservation',
                    'Lessons learned processes'
                ]
            }
        ]
        
        for control_data in iso27001_controls:
            control = ComplianceControl(
                control_id=control_data['control_id'],
                name=control_data['name'],
                description=control_data['description'],
                standard=ComplianceStandard.ISO27001,
                control_type=ControlType.OPERATIONAL,
                requirements=control_data['requirements']
            )
            self.controls[control.control_id] = control
            
    async def assess_compliance(self, standard: ComplianceStandard) -> ComplianceReport:
        """Perform compliance assessment for a specific standard"""
        
        # Get controls for the standard
        standard_controls = [
            control for control in self.controls.values()
            if control.standard == standard
        ]
        
        if not standard_controls:
            raise ValueError(f"No controls found for standard: {standard.value}")
            
        # Calculate compliance metrics
        total_controls = len(standard_controls)
        compliant_controls = len([
            c for c in standard_controls 
            if c.implementation_status == ComplianceStatus.COMPLIANT
        ])
        non_compliant_controls = len([
            c for c in standard_controls 
            if c.implementation_status == ComplianceStatus.NON_COMPLIANT
        ])
        
        # Calculate compliance score
        compliance_score = (compliant_controls / total_controls) * 100 if total_controls > 0 else 0
        
        # Determine overall status
        if compliance_score >= 95:
            overall_status = ComplianceStatus.COMPLIANT
        elif compliance_score >= 70:
            overall_status = ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            overall_status = ComplianceStatus.NON_COMPLIANT
            
        # Generate findings
        findings = []
        for control in standard_controls:
            if control.implementation_status != ComplianceStatus.COMPLIANT:
                findings.append({
                    'control_id': control.control_id,
                    'control_name': control.name,
                    'status': control.implementation_status.value,
                    'gap_description': f"Control {control.control_id} is not fully implemented",
                    'risk_level': 'HIGH' if control.implementation_status == ComplianceStatus.NON_COMPLIANT else 'MEDIUM'
                })
                
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(standard, findings)
        
        # Create report
        report = ComplianceReport(
            report_id=str(uuid4()),
            standard=standard,
            assessment_date=datetime.utcnow(),
            overall_status=overall_status,
            compliance_score=compliance_score,
            total_controls=total_controls,
            compliant_controls=compliant_controls,
            non_compliant_controls=non_compliant_controls,
            findings=findings,
            recommendations=recommendations,
            next_assessment=datetime.utcnow() + timedelta(days=365)  # Annual assessment
        )
        
        self.reports.append(report)
        logger.info(f"Compliance assessment completed for {standard.value}: {compliance_score:.1f}% compliant")
        
        return report
        
    def _generate_compliance_recommendations(self, standard: ComplianceStandard, 
                                          findings: List[Dict[str, Any]]) -> List[str]:
        """Generate compliance recommendations based on findings"""
        recommendations = []
        
        if standard == ComplianceStandard.GDPR:
            if any(f['control_id'] == 'GDPR-001' for f in findings):
                recommendations.append("Establish clear lawful basis for all data processing activities")
            if any(f['control_id'] == 'GDPR-002' for f in findings):
                recommendations.append("Implement automated data subject rights request handling")
            if any(f['control_id'] == 'GDPR-004' for f in findings):
                recommendations.append("Develop comprehensive data breach response procedures")
                
        elif standard == ComplianceStandard.HIPAA:
            if any(f['control_id'] == 'HIPAA-003' for f in findings):
                recommendations.append("Strengthen technical safeguards for PHI protection")
            if any(f['control_id'] == 'HIPAA-004' for f in findings):
                recommendations.append("Review and update business associate agreements")
                
        elif standard == ComplianceStandard.SOC2:
            if any(f['control_id'] == 'SOC2-001' for f in findings):
                recommendations.append("Implement comprehensive access control management")
            if any(f['control_id'] == 'SOC2-002' for f in findings):
                recommendations.append("Enhance system monitoring and availability controls")
                
        # General recommendations
        high_risk_findings = [f for f in findings if f.get('risk_level') == 'HIGH']
        if high_risk_findings:
            recommendations.append(f"Address {len(high_risk_findings)} high-risk compliance gaps immediately")
            
        if not recommendations:
            recommendations.append("Maintain current compliance posture and continue regular assessments")
            
        return recommendations
        
    async def update_control_status(self, control_id: str, 
                                  status: ComplianceStatus,
                                  evidence: Optional[List[str]] = None,
                                  responsible_party: Optional[str] = None) -> bool:
        """Update compliance control implementation status"""
        
        if control_id not in self.controls:
            return False
            
        control = self.controls[control_id]
        control.implementation_status = status
        control.last_reviewed = datetime.utcnow()
        control.next_review = datetime.utcnow() + timedelta(days=90)  # Quarterly review
        
        if evidence:
            control.evidence.extend(evidence)
            
        if responsible_party:
            control.responsible_party = responsible_party
            
        logger.info(f"Updated control {control_id} status to {status.value}")
        return True
        
    async def create_data_processing_record(self, record: DataProcessingRecord) -> str:
        """Create GDPR Article 30 record of processing activities"""
        
        record.record_id = record.record_id or str(uuid4())
        record.created_at = datetime.utcnow()
        record.updated_at = datetime.utcnow()
        
        self.data_processing_records[record.record_id] = record
        
        logger.info(f"Created data processing record: {record.record_id}")
        return record.record_id
        
    async def generate_compliance_dashboard(self) -> Dict[str, Any]:
        """Generate compliance dashboard data"""
        
        # Calculate overall compliance metrics
        total_controls = len(self.controls)
        compliant_controls = len([
            c for c in self.controls.values()
            if c.implementation_status == ComplianceStatus.COMPLIANT
        ])
        
        overall_compliance_score = (compliant_controls / total_controls) * 100 if total_controls > 0 else 0
        
        # Compliance by standard
        compliance_by_standard = {}
        for standard in ComplianceStandard:
            standard_controls = [c for c in self.controls.values() if c.standard == standard]
            if standard_controls:
                standard_compliant = len([
                    c for c in standard_controls
                    if c.implementation_status == ComplianceStatus.COMPLIANT
                ])
                compliance_by_standard[standard.value] = {
                    'total_controls': len(standard_controls),
                    'compliant_controls': standard_compliant,
                    'compliance_score': (standard_compliant / len(standard_controls)) * 100
                }
                
        # Recent assessments
        recent_reports = sorted(self.reports, key=lambda r: r.assessment_date, reverse=True)[:5]
        
        # Controls requiring attention
        attention_controls = [
            {
                'control_id': c.control_id,
                'name': c.name,
                'standard': c.standard.value,
                'status': c.implementation_status.value,
                'next_review': c.next_review.isoformat() if c.next_review else None
            }
            for c in self.controls.values()
            if c.implementation_status != ComplianceStatus.COMPLIANT
        ]
        
        dashboard = {
            'overall_compliance_score': overall_compliance_score,
            'total_controls': total_controls,
            'compliant_controls': compliant_controls,
            'compliance_by_standard': compliance_by_standard,
            'recent_assessments': [r.to_dict() for r in recent_reports],
            'controls_requiring_attention': attention_controls,
            'data_processing_records': len(self.data_processing_records),
            'last_updated': datetime.utcnow().isoformat()
        }
        
        return dashboard
        
    async def export_compliance_report(self, standard: ComplianceStandard, 
                                     format: str = 'json') -> Dict[str, Any]:
        """Export compliance report in specified format"""
        
        # Get latest report for the standard
        standard_reports = [r for r in self.reports if r.standard == standard]
        if not standard_reports:
            # Generate new assessment if none exists
            report = await self.assess_compliance(standard)
        else:
            report = max(standard_reports, key=lambda r: r.assessment_date)
            
        # Get controls for the standard
        standard_controls = [
            c.to_dict() for c in self.controls.values()
            if c.standard == standard
        ]
        
        export_data = {
            'report': report.to_dict(),
            'controls': standard_controls,
            'export_timestamp': datetime.utcnow().isoformat(),
            'format': format
        }
        
        return export_data
        
    async def schedule_compliance_review(self, control_id: str, 
                                       review_date: datetime) -> bool:
        """Schedule compliance control review"""
        
        if control_id not in self.controls:
            return False
            
        control = self.controls[control_id]
        control.next_review = review_date
        
        logger.info(f"Scheduled review for control {control_id} on {review_date}")
        return True
        
    async def get_compliance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive compliance metrics"""
        
        metrics = {
            'total_controls': len(self.controls),
            'compliant_controls': len([
                c for c in self.controls.values()
                if c.implementation_status == ComplianceStatus.COMPLIANT
            ]),
            'non_compliant_controls': len([
                c for c in self.controls.values()
                if c.implementation_status == ComplianceStatus.NON_COMPLIANT
            ]),
            'controls_under_review': len([
                c for c in self.controls.values()
                if c.implementation_status == ComplianceStatus.UNDER_REVIEW
            ]),
            'standards_covered': len(set(c.standard for c in self.controls.values())),
            'total_assessments': len(self.reports),
            'data_processing_records': len(self.data_processing_records),
            'overdue_reviews': len([
                c for c in self.controls.values()
                if c.next_review and c.next_review < datetime.utcnow()
            ])
        }
        
        return metrics


# Example usage
async def example_compliance_framework():
    """Example of using the compliance framework"""
    
    # Create compliance framework
    compliance = ComplianceFramework()
    
    # Update control status
    await compliance.update_control_status(
        'GDPR-001',
        ComplianceStatus.COMPLIANT,
        evidence=['Privacy policy updated', 'Legal basis documented'],
        responsible_party='Data Protection Officer'
    )
    
    # Perform GDPR assessment
    gdpr_report = await compliance.assess_compliance(ComplianceStandard.GDPR)
    print(f"GDPR Compliance Score: {gdpr_report.compliance_score:.1f}%")
    print(f"Status: {gdpr_report.overall_status.value}")
    
    # Create data processing record
    processing_record = DataProcessingRecord(
        record_id="dpr-001",
        controller_name="AI-Native PaaS Platform",
        contact_details="dpo@platform.com",
        purposes_of_processing=["Service provision", "Analytics", "Support"],
        categories_of_data_subjects=["Customers", "Employees"],
        categories_of_personal_data=["Contact information", "Usage data"],
        recipients=["Cloud service providers"],
        third_country_transfers=["US (adequacy decision)"],
        retention_periods={"Customer data": "7 years", "Analytics data": "2 years"},
        security_measures=["Encryption", "Access controls", "Audit logging"]
    )
    
    record_id = await compliance.create_data_processing_record(processing_record)
    print(f"Created data processing record: {record_id}")
    
    # Generate compliance dashboard
    dashboard = await compliance.generate_compliance_dashboard()
    print(f"Overall compliance score: {dashboard['overall_compliance_score']:.1f}%")
    
    # Get compliance metrics
    metrics = await compliance.get_compliance_metrics()
    print(f"Compliance metrics: {metrics['compliant_controls']}/{metrics['total_controls']} controls compliant")


if __name__ == "__main__":
    asyncio.run(example_compliance_framework())
