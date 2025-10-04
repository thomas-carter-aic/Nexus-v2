"""
AI-Native Cloud-Native PaaS Core Module

This module contains the core domain logic and foundational components for the
AI-native PaaS platform. It implements clean/hexagonal architecture principles
with clear separation between domain, application, and infrastructure layers.

Key Components:
- Domain models and business logic
- Event sourcing and CQRS patterns
- Saga orchestration for distributed transactions
- AI-driven optimization engines
- Plugin system architecture
"""

# Import core modules with graceful error handling
try:
    from .domain import *
except ImportError as e:
    print(f"Warning: Could not import domain module: {e}")

try:
    from .application import *
except ImportError as e:
    print(f"Warning: Could not import application module: {e}")

try:
    from .infrastructure import *
except ImportError as e:
    print(f"Warning: Could not import infrastructure module: {e}")

__version__ = "1.0.0"
__author__ = "AI-Native PaaS Team"
__description__ = "Core components for AI-native cloud-native PaaS platform"
