#!/usr/bin/env python3
"""
Test script for Excel export functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

def test_excel_export():
    """Test the Excel export endpoint"""
    print("Testing Excel Export...")
    
    try:
        with app.test_client() as client:
            # First, ensure we have some data
            print("1. Fetching weather data...")
            response = client.get('/api/weather-report?lat=47.37&lon=8.55')
            if response.status_code != 200:
                print(f"   ✗ Failed to fetch weather data: {response.status_code}")
                return False
            
            data = response.get_json()
            print(f"   ✓ Successfully fetched {data.get('records_count', 0)} records")
            
            # Test Excel export
            print("2. Testing Excel export...")
            response = client.get('/api/export/excel?lat=47.37&lon=8.55&hours=48')
            
            if response.status_code == 200:
                # Check if response is an Excel file
                content_type = response.headers.get('Content-Type')
                if 'spreadsheet' in content_type or 'excel' in content_type:
                    print("   ✓ Excel export successful")
                    print(f"   Content-Type: {content_type}")
                    print(f"   Content-Length: {len(response.data)} bytes")
                    
                    # Save the file for verification
                    import tempfile as _tmp
                    temp_path = _tmp.gettempdir().rstrip('\\/')
                    out_file = os.path.join(temp_path, 'test_weather_export.xlsx')
                    with open(out_file, 'wb') as f:
                        f.write(response.data)
                    print(f"   ✓ Excel file saved to {out_file}")
                    
                    return True
                else:
                    print(f"   ✗ Unexpected content type: {content_type}")
                    return False
            else:
                print(f"   ✗ Excel export failed: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
        
    except Exception as e:
        print(f"✗ Excel export test failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("=== Excel Export Test ===\n")
    
    success = test_excel_export()
    
    print(f"\n=== Test Results ===")
    print(f"Excel Export: {'PASSED' if success else 'FAILED'}")
    
    if success:
        print("✓ Excel export test passed!")
        sys.exit(0)
    else:
        print("✗ Excel export test failed!")
        sys.exit(1)

