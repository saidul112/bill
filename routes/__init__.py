"""
Routes package initialization
"""

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profiles import profiles_bp
from routes.bills import bills_bp
from routes.adjustments import adjustments_bp

__all__ = ['auth_bp', 'dashboard_bp', 'profiles_bp', 'bills_bp', 'adjustments_bp']
