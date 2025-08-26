#!/usr/bin/env python3
"""
Test script for weather API endpoints
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.services.weather_service import WeatherService

def test_weather_service():
    """Test the weather service functionality"""
    print("Testing Weather Service...")
    
    try:
        # Test API data fetching
        print("1. Testing API data fetch...")
        api_data = WeatherService.fetch_weather_data(47.37, 8.55, days=2)
        print(f"   ✓ Successfully fetched data with {len(api_data['hourly']['time'])} hourly records")
        
        # Test data processing and storage
        print("2. Testing data processing and storage...")
        with app.app_context():
            weather_records = WeatherService.process_and_store_weather_data(api_data, 47.37, 8.55)
            print(f"   ✓ Successfully processed and stored {len(weather_records)} records")
            
            # Test data retrieval
            print("3. Testing data retrieval...")
            recent_data = WeatherService.get_recent_weather_data(48)
            print(f"   ✓ Successfully retrieved {len(recent_data)} recent records")
            
            location_data = WeatherService.get_weather_data_by_location(47.37, 8.55, 48)
            print(f"   ✓ Successfully retrieved {len(location_data)} location-specific records")
        
        print("✓ All weather service tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Weather service test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test the Flask API endpoints"""
    print("\nTesting API Endpoints...")
    
    try:
        with app.test_client() as client:
            # Test health endpoint
            print("1. Testing health endpoint...")
            response = client.get('/api/health')
            if response.status_code == 200:
                print("   ✓ Health endpoint working")
            else:
                print(f"   ✗ Health endpoint failed: {response.status_code}")
                return False
            
            # Test weather-report endpoint
            print("2. Testing weather-report endpoint...")
            response = client.get('/api/weather-report?lat=47.37&lon=8.55')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✓ Weather report endpoint working, stored {data.get('records_count', 0)} records")
            else:
                print(f"   ✗ Weather report endpoint failed: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
            
            # Test weather-data endpoint
            print("3. Testing weather-data endpoint...")
            response = client.get('/api/weather-data?lat=47.37&lon=8.55&hours=24')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✓ Weather data endpoint working, retrieved {data.get('records_count', 0)} records")
            else:
                print(f"   ✗ Weather data endpoint failed: {response.status_code}")
                return False
        
        print("✓ All API endpoint tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ API endpoint test failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("=== Weather Backend Service Test ===\n")
    
    # Test weather service
    service_test_passed = test_weather_service()
    
    # Test API endpoints
    api_test_passed = test_api_endpoints()
    
    print(f"\n=== Test Results ===")
    print(f"Weather Service: {'PASSED' if service_test_passed else 'FAILED'}")
    print(f"API Endpoints: {'PASSED' if api_test_passed else 'FAILED'}")
    
    if service_test_passed and api_test_passed:
        print("✓ All tests passed! The weather backend service is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the implementation.")
        sys.exit(1)

