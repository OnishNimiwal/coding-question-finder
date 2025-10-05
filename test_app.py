#!/usr/bin/env python3
"""
Test Script for Coding Questions Finder
"""

import requests
import time
import sys
import pytest

def test_application(for_script: bool = False):
    """Test the application endpoints.

    If called by pytest (default) this function will use assertions/pytest.fail and return None.
    If called from the script runner (for_script=True) it will return True/False to preserve
    the previous behavior.
    """
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Coding Questions Finder Application")
    print("=" * 50)
    
    try:
        # Test if app is running
        print("1. Testing if application is running...")
        response = requests.get(base_url, timeout=5)
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print("✅ Application is running!")
        else:
            msg = f"Application returned status code: {response.status_code}"
            print(f"❌ {msg}")
            if for_script:
                return False
            pytest.fail(msg)
            
    except requests.exceptions.ConnectionError:
        msg = "Application is not running! Start the application with: python app.py"
        print(f"❌ {msg}")
        if for_script:
            return False
        pytest.fail(msg)
    except Exception as e:
        msg = f"Error testing application: {e}"
        print(f"❌ {msg}")
        if for_script:
            return False
        pytest.fail(msg)
    
    # Test login page
    try:
        print("\n2. Testing login page...")
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Login page is accessible!")
        else:
            msg = f"Login page returned status code: {response.status_code}"
            print(f"❌ {msg}")
            if for_script:
                return False
            pytest.fail(msg)
    except Exception as e:
        print(f"❌ Error testing login page: {e}")
    
    # Test register page
    try:
        print("\n3. Testing register page...")
        response = requests.get(f"{base_url}/register", timeout=5)
        if response.status_code == 200:
            print("✅ Register page is accessible!")
        else:
            msg = f"Register page returned status code: {response.status_code}"
            print(f"❌ {msg}")
            if for_script:
                return False
            pytest.fail(msg)
    except Exception as e:
        print(f"❌ Error testing register page: {e}")
    
    print("\n🎉 Application test completed!")
    print("📝 You can now:")
    print("   • Open http://localhost:5000 in your browser")
    print("   • Register as a Mentor or Student")
    print("   • Start using the application!")
    
    # Succeed for script runner
    if for_script:
        return True


if __name__ == "__main__":
    print("🚀 Starting application test...")
    print("⏳ Waiting 3 seconds for application to start...")
    time.sleep(3)
    
    success = test_application()
    
    if success:
        print("\n✅ All tests passed! Your application is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the application.")
        sys.exit(1)
