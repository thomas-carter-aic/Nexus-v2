"""
Domain Layer for AI-Native PaaS Platform

This module contains the core domain models and business logic.
"""

# Import simplified models for build testing
try:
    from .simple_models import *
except ImportError:
    pass

# Import full models when available
try:
    from .models import *
except ImportError:
    pass
