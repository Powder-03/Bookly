import requests
import json
from typing import Dict, Any

# Base URL for your FastAPI server
BASE_URL = "http://localhost:8000"

def test_endpoint(method: str, endpoint: str, expected_status: int = 200, data: Dict = None) -> Dict[Any, Any]:
    """
    Test a specific endpoint and return the response
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url)
        else:
            print(f"❌ Unsupported method: {method}")
            return {}
        
        # Check status code
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
        
        # Print response
        try:
            response_json = response.json()
            print(f"   Response: {json.dumps(response_json, indent=2)}")
            return response_json
        except:
            print(f"   Response: {response.text}")
            return {"text": response.text}
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed to {url}")
        print("   Make sure your FastAPI server is running with: uvicorn main:app --reload")
        return {}
    except Exception as e:
        print(f"❌ Error testing {endpoint}: {str(e)}")
        return {}

def test_server_health():
    """
    Check if the server is running
    """
    print("🔍 Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except:
        print("❌ Server is not running!")
        print("   Start it with: uvicorn main:app --reload")
        return False

def run_all_tests():
    """
    Run all tests for the FastAPI application
    """
    print("🚀 Starting FastAPI Tests")
    print("=" * 50)
    
    # Check if server is running
    if not test_server_health():
        return
    
    print("\n📋 Testing Endpoints:")
    print("-" * 30)
    
    # Test root endpoint
    test_endpoint("GET", "/")
    
    # Test greet endpoint with different names and ages (query parameter)
    test_endpoint("GET", "/greet/Alice?age=25")
    test_endpoint("GET", "/greet/Bob?age=30")
    test_endpoint("GET", "/greet/FastAPI?age=5")
    
    # Test with special characters
    test_endpoint("GET", "/greet/John%20Doe?age=35")  # URL encoded space
    
    # Test missing age parameter (should return 422)
    test_endpoint("GET", "/greet/Alice", expected_status=422)
    
    # Test invalid endpoint (should return 404)
    test_endpoint("GET", "/invalid", expected_status=404)
    
    print("\n" + "=" * 50)
    print("✨ Tests completed!")
    print("\n📖 To view API documentation:")
    print(f"   Interactive docs: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    run_all_tests()