"""
Infrastructure Layer for AI-Native PaaS Platform

This module contains infrastructure implementations for external integrations
and technical concerns, following the clean architecture pattern.
"""

# Import infrastructure implementations when they're available
try:
    from .aws_services import *
except ImportError:
    # AWS services module not available, skip import
    pass
