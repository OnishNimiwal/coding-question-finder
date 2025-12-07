#!/usr/bin/env python3
"""
Comprehensive Test Script for Coding Questions Finder
Tests all major functionality including search endpoint
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def test_app_running():
    """Test if the application is running"""
    print("=" * 60)
    print("TEST 1: Application Status")
    print("=" * 60)
    try:
        response = requests.get(BASE_URL, timeout=5, allow_redirects=True)
        print(f"✅ Application is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Application is not running!")
        print("   Please start the application with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n" + "=" * 60)
    print("TEST 2: Health Check Endpoints")
    print("=" * 60)
    
    # Test GenAI health
    try:
        response = requests.get(f"{BASE_URL}/health/genai", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GenAI Health Check: {data.get('message', 'OK')}")
            print(f"   AI Available: {data.get('ai_available', False)}")
            print(f"   API Key Present: {data.get('api_key_present', False)}")
            if data.get('model_candidates'):
                print(f"   Models: {', '.join(data.get('model_candidates', [])[:3])}")
            return data.get('ai_available', False)
        else:
            print(f"⚠️  GenAI Health Check returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking GenAI health: {e}")
        return False

def test_authentication():
    """Test registration and login"""
    print("\n" + "=" * 60)
    print("TEST 3: Authentication")
    print("=" * 60)
    
    test_username = f"test_user_{int(time.time())}"
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "testpass123"
    
    # Test registration
    try:
        print(f"   Registering test user: {test_username}")
        response = requests.post(
            f"{BASE_URL}/register",
            json={
                "username": test_username,
                "email": test_email,
                "password": test_password,
                "user_type": "mentor"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Registration successful")
            else:
                print(f"⚠️  Registration returned: {data.get('message')}")
        else:
            print(f"⚠️  Registration returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None
    
    # Test login
    try:
        print(f"   Logging in as: {test_username}")
        response = requests.post(
            f"{BASE_URL}/login",
            json={
                "username": test_username,
                "password": test_password
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Login successful")
                # Return session cookie for further tests
                return response.cookies
            else:
                print(f"❌ Login failed: {data.get('message')}")
                return None
        else:
            print(f"❌ Login returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_search_endpoint(cookies):
    """Test the search endpoint"""
    print("\n" + "=" * 60)
    print("TEST 4: Search Endpoint")
    print("=" * 60)
    
    if not cookies:
        print("⚠️  Skipping search test - no authenticated session")
        return False
    
    test_query = "binary tree traversal"
    
    try:
        print(f"   Searching for: '{test_query}'")
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": test_query},
            cookies=cookies,
            timeout=30  # Longer timeout for AI calls
        )
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Search request successful")
                print(f"   Summary: {data.get('summary', 'N/A')[:100]}...")
                
                questions = data.get('questions', [])
                print(f"   Questions returned: {len(questions)}")
                
                if questions:
                    print("\n   Sample question structure:")
                    first_q = questions[0]
                    required_fields = ['url', 'platform', 'topic', 'difficulty_level', 'company', 'category']
                    for field in required_fields:
                        value = first_q.get(field, 'MISSING')
                        print(f"      {field}: {value}")
                    
                    # Check if all required fields are present
                    missing_fields = [f for f in required_fields if f not in first_q]
                    if missing_fields:
                        print(f"\n   ⚠️  Missing fields in response: {missing_fields}")
                        return False
                    else:
                        print("\n   ✅ All required fields present")
                        return True
                else:
                    print("   ⚠️  No questions returned")
                    return False
            else:
                print(f"   ❌ Search failed: {data.get('error', 'Unknown error')}")
                return False
        elif response.status_code == 503:
            data = response.json()
            print(f"   ⚠️  AI not available: {data.get('error', 'Unknown error')}")
            return False
        else:
            print(f"   ❌ Search returned status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("   ❌ Search request timed out (AI may be slow)")
        return False
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n🧪 COMPREHENSIVE APPLICATION TEST")
    print("=" * 60)
    print("Make sure the application is running on http://localhost:5000")
    print("=" * 60)
    
    results = {}
    
    # Test 1: App running
    results['app_running'] = test_app_running()
    if not results['app_running']:
        print("\n❌ Application is not running. Please start it first.")
        sys.exit(1)
    
    # Test 2: Health checks
    results['ai_available'] = test_health_endpoints()
    
    # Test 3: Authentication
    cookies = test_authentication()
    results['auth'] = cookies is not None
    
    # Test 4: Search (only if authenticated)
    if cookies:
        results['search'] = test_search_endpoint(cookies)
    else:
        results['search'] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Application Running: {'✅' if results['app_running'] else '❌'}")
    print(f"AI Available: {'✅' if results.get('ai_available') else '❌'}")
    print(f"Authentication: {'✅' if results['auth'] else '❌'}")
    print(f"Search Endpoint: {'✅' if results.get('search') else '❌'}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

