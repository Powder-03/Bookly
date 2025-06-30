import requests
import json
from typing import Dict, Any

# Base URL for your FastAPI server
BASE_URL = "http://localhost:8000/api/v1"

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
    print("🚀 Starting Bookly API Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server is not responding correctly")
            return
    except:
        print("❌ Server is not running!")
        print("   Start it with: uvicorn main:app --reload")
        return
    
    print("\n📋 Testing Book API Endpoints:")
    print("-" * 30)
    
    # Test get all books
    test_endpoint("GET", "/books")
    
    # Test get specific book
    test_endpoint("GET", "/books/1")
    test_endpoint("GET", "/books/999", expected_status=404)  # Non-existent book
    
    # Test create book
    new_book = {
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "published_date": "2024-01-01",
        "pagecount": 100,
        "language": "English"
    }
    test_endpoint("POST", "/books", data=new_book, expected_status=201)
    
    # Test update book
    update_data = {
        "title": "Updated Test Book",
        "pagecount": 150
    }
    test_endpoint("PUT", "/books/1", data=update_data)
    
    # Test delete book
    test_endpoint("DELETE", "/books/6")  # Delete the newly created book
    
    print("\n" + "=" * 50)
    print("✨ Tests completed!")
    print(f"\n📖 API Documentation: http://localhost:8000/docs")
    print(f"📖 Alternative docs: http://localhost:8000/redoc")

if __name__ == "__main__":
    run_all_tests()