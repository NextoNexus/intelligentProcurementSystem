#!/usr/bin/env python3
"""
Test application imports
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing application imports...")

try:
    # Test core config import
    from app.core.config import settings
    print("[OK] Successfully imported config")

    # Test database model imports
    from app.models import Base, User, Role, Supplier, ProcurementRequest, PurchaseOrder
    print("[OK] Successfully imported database models")

    # Test API route imports
    from app.api import auth, suppliers, procurement, inventory, ai
    print("[OK] Successfully imported API modules")

    # Test main application import
    from app.main import app
    print("[OK] Successfully imported FastAPI application")

    print("\nAll import tests passed!")
    print(f"App name: {settings.app_name}")
    print(f"App version: {settings.app_version}")
    print(f"Debug mode: {settings.debug}")

except Exception as e:
    print(f"\n[FAIL] Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)