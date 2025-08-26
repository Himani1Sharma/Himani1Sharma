#!/usr/bin/env python3
"""
Comprehensive test suite for the Weather Backend Service
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.services.weather_service import WeatherService
from src.models.weather import WeatherData, db

def test_database_operations():
    """Test database operations"""
    print("=== Testing Database Operations ===")
    
    try:
        with app.app_context():
            # Test database connection
            print("1. Testing database connection...")
            record_count = WeatherData.query.count()
            print(f"   ✓ Database connected, {record_count} existing records")
            
            # Test table structure
            print("2. Testing table structure...")
            columns = [column.name for column in WeatherData.__table__.columns]
            expected_columns = ['id', 'timestamp', 'latitude', 'longitude', 'temperature_2m', 'relative_humidity_2m', 'created_at']
            
            if all(col in columns for col in expected_columns):
                print(f"   ✓ All required columns present: {columns}")
            else:
                print(f"   ✗ Missing columns. Expected: {expected_columns}, Found: {columns}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {str(e)}")
        return False

def test_weather_service():
    """Test weather service functionality"""
    print("\n=== Testing Weather Service ===")
    
    try:
        with app.app_context():
            # Test API data fetching
            print("1. Testing API data fetch...")
            api_data = WeatherService.fetch_weather_data(47.37, 8.55, days=1)
            
            if 'hourly' in api_data and 'time' in api_data['hourly']:
                record_count = len(api_data['hourly']['time'])
                print(f"   ✓ Successfully fetched {record_count} hourly records")
            else:
                print("   ✗ Invalid API response structure")
                return False
            
            # Test data processing and storage
            print("2. Testing data processing and storage...")
            weather_records = WeatherService.process_and_store_weather_data(api_data, 47.37, 8.55)
            print(f"   ✓ Successfully processed and stored {len(weather_records)} records")
            
            # Test data retrieval
            print("3. Testing data retrieval...")
            recent_data = WeatherService.get_recent_weather_data(24)
            location_data = WeatherService.get_weather_data_by_location(47.37, 8.55, 24)
            
            print(f"   ✓ Retrieved {len(recent_data)} recent records")
            print(f"   ✓ Retrieved {len(location_data)} location-specific records")
        
        return True
        
    except Exception as e:
        print(f"✗ Weather service test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n=== Testing API Endpoints ===")
    
    try:
        with app.test_client() as client:
            # Test health endpoint
            print("1. Testing health endpoint...")
            response = client.get('/api/health')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✓ Health endpoint working - Status: {data.get('status')}")
            else:
                print(f"   ✗ Health endpoint failed: {response.status_code}")
                return False
            
            # Test weather-report endpoint with valid coordinates
            print("2. Testing weather-report endpoint...")
            response = client.get('/api/weather-report?lat=47.37&lon=8.55')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✓ Weather report successful - {data.get('records_count', 0)} records")
            else:
                print(f"   ✗ Weather report failed: {response.status_code}")
                return False
            
            # Test weather-report endpoint with invalid coordinates
            print("3. Testing weather-report endpoint with invalid coordinates...")
            response = client.get('/api/weather-report?lat=91&lon=181')
            if response.status_code == 400:
                print("   ✓ Correctly rejected invalid coordinates")
            else:
                print(f"   ✗ Should have rejected invalid coordinates: {response.status_code}")
                return False
            
            # Test weather-report endpoint with missing parameters
            print("4. Testing weather-report endpoint with missing parameters...")
            response = client.get('/api/weather-report')
            if response.status_code == 400:
                print("   ✓ Correctly rejected missing parameters")
            else:
                print(f"   ✗ Should have rejected missing parameters: {response.status_code}")
                return False
            
            # Test weather-data endpoint
            print("5. Testing weather-data endpoint...")
            response = client.get('/api/weather-data?lat=47.37&lon=8.55&hours=72')  # Use 72 hours to capture historical data
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✓ Weather data retrieval successful - {data.get('records_count', 0)} records")
            else:
                print(f"   ✗ Weather data retrieval failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {str(e)}")
        return False

def test_export_endpoints():
    """Test export endpoints"""
    print("\n=== Testing Export Endpoints ===")
    
    try:
        with app.test_client() as client:
            # Ensure we have data first
            response = client.get('/api/weather-report?lat=47.37&lon=8.55')
            if response.status_code != 200:
                print("   ✗ Failed to fetch data for export tests")
                return False
            
            # Test Excel export
            print("1. Testing Excel export...")
            response = client.get('/api/export/excel?lat=47.37&lon=8.55&hours=72')  # Use 72 hours
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'spreadsheet' in content_type or 'excel' in content_type:
                    print(f"   ✓ Excel export successful - {len(response.data)} bytes")
                else:
                    print(f"   ✗ Unexpected Excel content type: {content_type}")
                    return False
            else:
                print(f"   ✗ Excel export failed: {response.status_code}")
                return False
            
            # Test PDF export
            print("2. Testing PDF export...")
            response = client.get('/api/export/pdf?lat=47.37&lon=8.55&hours=72')  # Use 72 hours
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'pdf' in content_type:
                    print(f"   ✓ PDF export successful - {len(response.data)} bytes")
                else:
                    print(f"   ✗ Unexpected PDF content type: {content_type}")
                    return False
            else:
                print(f"   ✗ PDF export failed: {response.status_code}")
                return False
            
            # Test export with no data
            print("3. Testing export with no data...")
            response = client.get('/api/export/excel?lat=0&lon=0&hours=1')
            if response.status_code == 404:
                print("   ✓ Correctly handled no data scenario")
            else:
                print(f"   ✗ Should have returned 404 for no data: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Export endpoints test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling scenarios"""
    print("\n=== Testing Error Handling ===")
    
    try:
        with app.test_client() as client:
            # Test invalid hours parameter
            print("1. Testing invalid hours parameter...")
            response = client.get('/api/weather-data?hours=200')
            if response.status_code == 400:
                print("   ✓ Correctly rejected invalid hours parameter")
            else:
                print(f"   ✗ Should have rejected invalid hours: {response.status_code}")
                return False
            
            # Test invalid coordinate ranges
            print("2. Testing invalid coordinate ranges...")
            response = client.get('/api/export/excel?lat=100&lon=200')
            if response.status_code == 400:
                print("   ✓ Correctly rejected invalid coordinates")
            else:
                print(f"   ✗ Should have rejected invalid coordinates: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {str(e)}")
        return False

def run_comprehensive_tests():
    """Run all tests"""
    print("🧪 Weather Backend Service - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database Operations", test_database_operations),
        ("Weather Service", test_weather_service),
        ("API Endpoints", test_api_endpoints),
        ("Export Endpoints", test_export_endpoints),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} tests...")
        start_time = time.time()
        
        try:
            result = test_func()
            results[test_name] = result
            duration = time.time() - start_time
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {status} ({duration:.2f}s)")
        except Exception as e:
            results[test_name] = False
            duration = time.time() - start_time
            print(f"   ❌ FAILED ({duration:.2f}s) - {str(e)}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The Weather Backend Service is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the implementation.")
        return False

if __name__ == '__main__':
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)

