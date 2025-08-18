"""
Configuration file for SOP API Generator
Update these settings according to your API requirements
"""

# API Configuration
API_CONFIG = {
    # Replace with your actual API base URL
    "BASE_URL": "https://your-api-endpoint.com",
    
    # API Key for authentication (set to None if not required)
    "API_KEY": "your-api-key-here",
    
    # Request timeout in seconds
    "TIMEOUT": 30,
    
    # API endpoints for different operations
    "ENDPOINTS": {
        "create_sop": "/api/sops",
        "update_sop": "/api/sops",
        "get_sop": "/api/sops",
        "delete_sop": "/api/sops",
        "list_sops": "/api/sops/list"
    }
}

# Processing Configuration
PROCESSING_CONFIG = {
    # Maximum number of concurrent threads for parallel processing
    "MAX_WORKERS": 5,
    
    # Delay between sequential API calls (in seconds)
    "DELAY_BETWEEN_CALLS": 0.5,
    
    # Retry configuration
    "MAX_RETRIES": 3,
    "RETRY_DELAY": 1,
    
    # Default HTTP method for API calls
    "DEFAULT_METHOD": "POST"
}

# Output Configuration
OUTPUT_CONFIG = {
    # Default output directory for results
    "OUTPUT_DIR": "./results",
    
    # Default filename for results
    "DEFAULT_FILENAME": "sop_api_results.json",
    
    # Log file configuration
    "LOG_FILE": "sop_api_calls.log",
    "LOG_LEVEL": "INFO"
}

# SOP Categories (for reference and validation)
SOP_CATEGORIES = [
    "Quality Assurance",
    "Materials Management", 
    "Quality Control",
    "Production",
    "Packaging",
    "Engineering",
    "Health Safety Environment"
]

# Additional payload data that can be included with each SOP
DEFAULT_ADDITIONAL_DATA = {
    "company": "Your Company Name",
    "facility": "Manufacturing Facility",
    "version": "1.0",
    "effective_date": "2024-01-01",
    "review_date": "2025-01-01",
    "approved_by": "Quality Manager"
}