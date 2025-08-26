# Weather Backend Service

A comprehensive backend service that fetches time-series weather data from the Open-Meteo API and provides REST endpoints for data retrieval, Excel export, and PDF report generation with charts.

## 🚀 Features

- **Weather Data Fetching**: Integrates with Open-Meteo Archive API to fetch historical weather data
- **Database Storage**: Stores weather data in SQLite database with proper indexing
- **REST API**: Provides clean REST endpoints for data access and manipulation
- **Excel Export**: Generates formatted Excel files (.xlsx) with weather data
- **PDF Reports**: Creates professional PDF reports with charts and statistics
- **Data Visualization**: Uses matplotlib to generate temperature and humidity charts
- **Error Handling**: Comprehensive error handling and input validation
- **CORS Support**: Enabled for cross-origin requests

## 📋 Requirements

All requirements are listed in `requirements.txt`. Key dependencies include:

- Flask 3.1.1 - Web framework
- Flask-SQLAlchemy 3.1.1 - Database ORM
- requests 2.32.5 - HTTP client for API calls
- openpyxl 3.1.5 - Excel file generation
- matplotlib 3.10.5 - Chart generation
- weasyprint 66.0 - PDF generation
- flask-cors 6.0.0 - CORS support

## 🛠️ Installation

1. **Clone or extract the project**:
   ```bash
   cd weather-backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   The database will be automatically created when you first run the application.

## 🚀 Running the Application

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Start the Flask server**:
   ```bash
   python src/main.py
   ```

3. **The server will start on**: `http://localhost:5000`

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "Weather Backend Service",
  "timestamp": "2025-08-25T14:30:00.000000",
  "database": {
    "status": "connected",
    "total_records": 27
  }
}
```

#### 2. Fetch Weather Data
```http
GET /api/weather-report?lat={latitude}&lon={longitude}
```

**Parameters**:
- `lat` (required): Latitude coordinate (-90 to 90)
- `lon` (required): Longitude coordinate (-180 to 180)

**Example**:
```http
GET /api/weather-report?lat=47.37&lon=8.55
```

**Response**:
```json
{
  "status": "success",
  "message": "Successfully fetched and stored 48 weather records",
  "location": {
    "latitude": 47.37,
    "longitude": 8.55
  },
  "records_count": 48,
  "data_range": {
    "start": "2025-08-23T00:00:00",
    "end": "2025-08-24T23:00:00"
  },
  "sample_data": [...]
}
```

#### 3. Retrieve Weather Data
```http
GET /api/weather-data?lat={latitude}&lon={longitude}&hours={hours}
```

**Parameters**:
- `lat` (optional): Latitude coordinate
- `lon` (optional): Longitude coordinate
- `hours` (optional): Number of hours to look back (default: 48, max: 168)

**Example**:
```http
GET /api/weather-data?lat=47.37&lon=8.55&hours=24
```

#### 4. Export to Excel
```http
GET /api/export/excel?lat={latitude}&lon={longitude}&hours={hours}
```

**Parameters**: Same as weather-data endpoint

**Response**: Downloads an Excel file (.xlsx) with formatted weather data

#### 5. Export to PDF
```http
GET /api/export/pdf?lat={latitude}&lon={longitude}&hours={hours}
```

**Parameters**: Same as weather-data endpoint

**Response**: Downloads a PDF report with charts and statistics

## 🗄️ Database Schema

### WeatherData Table
```sql
CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    temperature_2m FLOAT NOT NULL,
    relative_humidity_2m FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- `timestamp` - For efficient time-based queries
- Composite index on `(latitude, longitude, timestamp)` for location-based queries

## 🧪 Testing

The project includes comprehensive test suites:

### Run All Tests
```bash
python test_comprehensive.py
```

### Individual Test Files
- `test_api.py` - Basic API functionality tests
- `test_excel.py` - Excel export functionality tests
- `test_pdf.py` - PDF export functionality tests
- `test_comprehensive.py` - Complete test suite

### Test Coverage
- ✅ Database operations and connectivity
- ✅ Weather service API integration
- ✅ All REST API endpoints
- ✅ Excel export functionality
- ✅ PDF report generation
- ✅ Error handling and validation
- ✅ Input parameter validation
- ✅ Edge cases and error scenarios

## 📊 Data Flow

1. **Data Fetching**: Client calls `/api/weather-report` with coordinates
2. **API Integration**: Service fetches data from Open-Meteo Archive API
3. **Data Processing**: Raw API data is processed and validated
4. **Database Storage**: Processed data is stored in SQLite database
5. **Data Retrieval**: Clients can retrieve stored data via `/api/weather-data`
6. **Export Options**: Data can be exported as Excel or PDF reports

## 🔧 Configuration

### Environment Variables
The application uses the following configuration:
- Database: SQLite file at `src/database/app.db`
- Host: `0.0.0.0` (allows external access)
- Port: `5000`
- Debug: `True` (disable in production)

### API Configuration
- Open-Meteo API: `https://archive-api.open-meteo.com/v1/archive`
- Request timeout: 30 seconds
- Data retention: Past 2 days by default

## 🚨 Error Handling

The API provides comprehensive error handling:

### Common Error Responses
```json
{
  "error": "Invalid coordinates",
  "message": "Latitude must be between -90 and 90, longitude between -180 and 180"
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (no data available)
- `500` - Internal Server Error

## 📈 Performance Considerations

- **Database Indexing**: Optimized queries with proper indexes
- **Data Deduplication**: Prevents duplicate records for same timestamp/location
- **Memory Management**: Efficient handling of large datasets
- **File Cleanup**: Automatic cleanup of temporary export files
- **Connection Pooling**: SQLAlchemy handles database connections efficiently

## 🔒 Security Features

- **Input Validation**: All parameters are validated and sanitized
- **SQL Injection Prevention**: Uses SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Properly configured for cross-origin requests
- **Error Information**: Sensitive information is not exposed in error messages

## 📝 API Usage Examples

### Fetch Weather Data for Zurich
```bash
curl "http://localhost:5000/api/weather-report?lat=47.37&lon=8.55"
```

### Get Recent Weather Data
```bash
curl "http://localhost:5000/api/weather-data?hours=48"
```

### Download Excel Report
```bash
curl -O -J "http://localhost:5000/api/export/excel?lat=47.37&lon=8.55&hours=48"
```

### Download PDF Report
```bash
curl -O -J "http://localhost:5000/api/export/pdf?lat=47.37&lon=8.55&hours=48"
```

## 🏗️ Project Structure

```
weather-backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model (template)
│   │   └── weather.py       # Weather data model
│   ├── routes/
│   │   ├── user.py          # User routes (template)
│   │   └── weather.py       # Weather API routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py  # Weather service logic
│   ├── static/              # Static files
│   ├── database/
│   │   └── app.db          # SQLite database
│   └── main.py             # Flask application entry point
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── test_api.py            # API tests
├── test_excel.py          # Excel export tests
├── test_pdf.py            # PDF export tests
├── test_comprehensive.py  # Complete test suite
└── README.md              # This file
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting changes

## 📄 License

This project is created as a take-home assignment and is provided as-is for evaluation purposes.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure the `src/database/` directory exists
   - Check file permissions

2. **API Timeout**:
   - Check internet connection
   - Verify Open-Meteo API availability

3. **Export File Generation**:
   - Ensure sufficient disk space
   - Check write permissions in temp directory

4. **Missing Dependencies**:
   - Run `pip install -r requirements.txt`
   - Ensure virtual environment is activated

### Debug Mode
To enable detailed error logging, the application runs in debug mode by default. For production deployment, set `debug=False` in `main.py`.

---

**Created by**: Senior Backend Developer  
**Date**: August 2025  
**Version**: 1.0.0

