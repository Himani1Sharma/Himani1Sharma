#!/usr/bin/env python3
"""
Test script for PDF export functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

def test_pdf_export():
    """Test the PDF export endpoint"""
    print("Testing PDF Export...")
    
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
            
            # Test PDF export
            print("2. Testing PDF export...")
            response = client.get('/api/export/pdf?lat=47.37&lon=8.55&hours=48')
            
            if response.status_code == 200:
                # Check if response is a PDF file
                content_type = response.headers.get('Content-Type')
                if 'pdf' in content_type:
                    print("   ✓ PDF export successful")
                    print(f"   Content-Type: {content_type}")
                    print(f"   Content-Length: {len(response.data)} bytes")
                    
                    # Save the file for verification
                    import tempfile as _tmp
                    temp_path = _tmp.gettempdir().rstrip('\\/')
                    out_file = os.path.join(temp_path, 'test_weather_report.pdf')
                    with open(out_file, 'wb') as f:
                        f.write(response.data)
                    print(f"   ✓ PDF file saved to {out_file}")
                    
                    return True
                else:
                    print(f"   ✗ Unexpected content type: {content_type}")
                    return False
            else:
                print(f"   ✗ PDF export failed: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
        
    except Exception as e:
        print(f"✗ PDF export test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== PDF Export Test ===\n")
    
    success = test_pdf_export()
    
    print(f"\n=== Test Results ===")
    print(f"PDF Export: {'PASSED' if success else 'FAILED'}")
    
    if success:
        print("✓ PDF export test passed!")
        sys.exit(0)
    else:
        print("✗ PDF export test failed!")
        sys.exit(1)

