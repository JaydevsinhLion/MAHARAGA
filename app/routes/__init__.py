"""
maharaga routes initializer
---------------------------
centralizes all route blueprints for api, admin, and auth.
"""

from app.routes import api_routes, admin_routes, auth_routes

__all__ = ["api_routes", "admin_routes", "auth_routes"]
