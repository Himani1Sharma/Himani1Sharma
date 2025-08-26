import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.models.weather import WeatherData, db

class WeatherService:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    
    @staticmethod
    def fetch_weather_data(latitude: float, longitude: float, days: int = 2) -> Dict[str, Any]:
        """
        Fetch weather data from Open-Meteo API for the specified location and time period.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            days: Number of past days to fetch data for (default: 2)
            
        Returns:
            Dictionary containing the API response data
            
        Raises:
            requests.RequestException: If API request fails
            ValueError: If API returns invalid data
        """
        # Calculate date range for past N days (inclusive) using archive API
        # Example: days=2 -> start=yesterday-1, end=yesterday (2 days total)
        end_date = datetime.now().date() - timedelta(days=1)  # Archive requires past dates
        start_date = end_date - timedelta(days=days - 1)
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,relative_humidity_2m',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'timezone': 'auto'
        }
        
        try:
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if 'hourly' not in data:
                raise ValueError("Invalid API response: missing 'hourly' data")
                
            hourly_data = data['hourly']
            required_fields = ['time', 'temperature_2m', 'relative_humidity_2m']
            
            for field in required_fields:
                if field not in hourly_data:
                    raise ValueError(f"Invalid API response: missing '{field}' in hourly data")
            
            return data
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch weather data: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid weather data received: {str(e)}")
    
    @staticmethod
    def process_and_store_weather_data(api_data: Dict[str, Any], latitude: float, longitude: float) -> List[WeatherData]:
        """
        Process API response data and store it in the database.
        
        Args:
            api_data: Raw API response data
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            List of WeatherData objects that were created
        """
        hourly_data = api_data['hourly']
        timestamps = hourly_data['time']
        temperatures = hourly_data['temperature_2m']
        humidities = hourly_data['relative_humidity_2m']
        
        weather_records = []
        
        for i, timestamp_str in enumerate(timestamps):
            # Parse timestamp
            timestamp = datetime.fromisoformat(timestamp_str.replace('T', ' '))
            
            # Skip if temperature or humidity is None
            if temperatures[i] is None or humidities[i] is None:
                continue
            
            # Check if record already exists
            existing_record = WeatherData.query.filter_by(
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude
            ).first()
            
            if existing_record:
                # Update existing record
                existing_record.temperature_2m = temperatures[i]
                existing_record.relative_humidity_2m = humidities[i]
                weather_records.append(existing_record)
            else:
                # Create new record
                weather_record = WeatherData(
                    timestamp=timestamp,
                    latitude=latitude,
                    longitude=longitude,
                    temperature_2m=temperatures[i],
                    relative_humidity_2m=humidities[i]
                )
                db.session.add(weather_record)
                weather_records.append(weather_record)
        
        try:
            db.session.commit()
            return weather_records
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to store weather data: {str(e)}")
    
    @staticmethod
    def get_recent_weather_data(hours: int = 48) -> List[WeatherData]:
        """
        Retrieve recent weather data from the database.
        
        Args:
            hours: Number of hours to look back (default: 48)
            
        Returns:
            List of WeatherData objects ordered by timestamp
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return WeatherData.query.filter(
            WeatherData.timestamp >= cutoff_time
        ).order_by(WeatherData.timestamp.asc()).all()
    
    @staticmethod
    def get_weather_data_by_location(latitude: float, longitude: float, hours: int = 48) -> List[WeatherData]:
        """
        Retrieve weather data for a specific location from the database.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            hours: Number of hours to look back (default: 48)
            
        Returns:
            List of WeatherData objects for the specified location
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return WeatherData.query.filter(
            WeatherData.latitude == latitude,
            WeatherData.longitude == longitude,
            WeatherData.timestamp >= cutoff_time
        ).order_by(WeatherData.timestamp.asc()).all()



