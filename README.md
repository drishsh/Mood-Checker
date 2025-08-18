# SOP API Generator for Aspirin Tablet Manufacturing

A comprehensive Python script for generating API calls for all Standard Operating Procedures (SOPs) in aspirin tablet manufacturing with one-button execution.

## 🏭 Features

- **Complete SOP Coverage**: All 58 SOPs across 7 categories
- **One-Button Execution**: Process all SOPs with a single command
- **Parallel & Sequential Processing**: Choose your preferred execution method
- **Category-Specific Processing**: Process SOPs by category
- **Error Handling**: Comprehensive error handling and logging
- **Results Export**: Save results to JSON files
- **Flexible Configuration**: Easy to configure for different APIs

## 📋 SOP Categories Covered

1. **Quality Assurance (14 SOPs)** - System-level procedures
2. **Materials Management (9 SOPs)** - Warehouse operations
3. **Quality Control (13 SOPs)** - Laboratory testing procedures
4. **Production (9 SOPs)** - Manufacturing processes
5. **Packaging (4 SOPs)** - Packaging operations
6. **Engineering (5 SOPs)** - Equipment maintenance
7. **Health Safety Environment (2 SOPs)** - Safety procedures

**Total: 58 SOPs**

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your API
Edit the configuration in `config.py` or directly in the script:

```python
BASE_URL = "https://your-api-endpoint.com"
API_KEY = "your-api-key-here"  # Or None if not needed
```

### 3. One-Button Execution
```bash
python quick_run_example.py
```

## 💻 Usage Examples

### Process All SOPs (Parallel)
```python
from sop_api_generator import SOPAPIGenerator

generator = SOPAPIGenerator(
    base_url="https://your-api.com",
    api_key="your-key"
)

# Process all 58 SOPs in parallel
results = generator.process_all_sops_parallel(
    endpoint="/api/sops",
    method="POST",
    max_workers=5
)

# Save results
generator.save_results_to_file(results)
```

### Process Specific Category
```python
# Process only Quality Assurance SOPs
results = generator.process_sops_by_category(
    category="Quality Assurance",
    parallel=True
)
```

### Sequential Processing with Delay
```python
# Process one by one with delay
results = generator.process_all_sops_sequential(
    delay_between_calls=0.5
)
```

## 🔧 Configuration Options

### Processing Methods
- **Parallel**: Fast execution using ThreadPoolExecutor
- **Sequential**: One-by-one processing with optional delays
- **Category-specific**: Process only selected categories

### API Methods Supported
- POST (default)
- PUT
- GET

### Customizable Parameters
- Request timeout
- Number of parallel workers
- Delay between requests
- Additional payload data
- Custom endpoints

## 📊 Output

The script generates detailed results including:
- Success/failure status for each SOP
- HTTP status codes
- Response data
- Error messages
- Summary statistics
- Processing timestamps

Example output structure:
```json
{
  "summary": {
    "total_sops": 58,
    "successful": 56,
    "failed": 2,
    "success_rate": "96.6%",
    "timestamp": "2024-01-15 10:30:45"
  },
  "results": [
    {
      "sop_code": "SOP-QA-001",
      "status": "success",
      "status_code": 201,
      "response": {...}
    }
  ]
}
```

## 🏗️ SOP Data Structure

Each SOP includes:
- **Code**: Unique identifier (e.g., SOP-QA-001)
- **Title**: Descriptive name
- **Category**: Functional category
- **Description**: Brief description
- **Metadata**: Timestamps, status, etc.

## 🛠️ Advanced Usage

### Custom Payload Data
```python
additional_data = {
    "company": "Your Company",
    "version": "1.0",
    "effective_date": "2024-01-01"
}

results = generator.process_all_sops_parallel(
    additional_data=additional_data
)
```

### Error Handling
The script includes comprehensive error handling:
- Network timeouts
- HTTP errors
- Authentication failures
- Thread execution errors
- File I/O errors

### Logging
All operations are logged to:
- Console output
- `sop_api_calls.log` file

## 📁 File Structure

```
/workspace/
├── sop_api_generator.py      # Main script
├── quick_run_example.py      # One-button execution
├── config.py                 # Configuration settings
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── results/                  # Output directory
    ├── sop_api_results.json
    └── sop_api_calls.log
```

## 🔒 Security Notes

- Store API keys securely (environment variables recommended)
- Use HTTPS endpoints
- Implement rate limiting if needed
- Validate SSL certificates

## 🤝 Contributing

Feel free to modify the script for your specific requirements:
- Add new SOP categories
- Modify payload structure
- Add custom validation
- Implement additional HTTP methods

## 📞 Support

For issues or questions:
1. Check the logs in `sop_api_calls.log`
2. Verify API endpoint configuration
3. Test with a single SOP first
4. Check network connectivity

---

**Ready to process all 58 SOPs with one button click!** 🚀