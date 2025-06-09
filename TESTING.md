# Testing Documentation for Mood Checker Application

## Overview
This document describes the testing procedures and test suite for the Mood Checker application. The test suite uses Python's `unittest` framework and includes tests for all major functionality of the application.

## Test Environment Setup

### Prerequisites
- Python 3.10 or higher
- Required packages (install using pip):
  ```bash
  pip install -r requirements-dev.txt
  ```

### Test Files
- `test_mood_checker_tkinter.py`: Main test suite
- `requirements-dev.txt`: Development dependencies including testing tools

## Running the Tests

### Running All Tests
To run all tests with verbose output:
```bash
python3 -m pytest test_mood_checker_tkinter.py -v
```

### Running Specific Tests
To run a specific test:
```bash
python3 -m pytest test_mood_checker_tkinter.py -v -k "test_name"
```
Replace `test_name` with one of:
- `test_initialization`
- `test_emoji_buttons`
- `test_mood_selection`
- `test_notification_eligibility`
- `test_mood_saving`
- `test_animation_setup`

## Test Suite Description

### Test Cases

#### 1. Initialization Test (`test_initialization`)
- **Purpose**: Verifies proper initialization of application files and data structures
- **Checks**:
  - Test files are created correctly
  - CSV header is properly formatted
  - File permissions are correct

#### 2. Emoji Buttons Test (`test_emoji_buttons`)
- **Purpose**: Ensures emoji buttons are created and configured correctly
- **Checks**:
  - Correct number of emoji buttons
  - Button layout and styling
  - Emoji-state mapping

#### 3. Mood Selection Test (`test_mood_selection`)
- **Purpose**: Validates mood selection functionality
- **Checks**:
  - Button click handling
  - Mood state updates
  - Visual feedback on selection

#### 4. Notification Eligibility Test (`test_notification_eligibility`)
- **Purpose**: Tests notification timing and eligibility logic
- **Checks**:
  - Initial notification state
  - Date-based eligibility
  - User-specific notifications

#### 5. Mood Saving Test (`test_mood_saving`)
- **Purpose**: Verifies mood data persistence
- **Checks**:
  - CSV file writing
  - Data format correctness
  - File handling errors

#### 6. Animation Setup Test (`test_animation_setup`)
- **Purpose**: Tests animation components and behavior
- **Checks**:
  - Animation canvas creation
  - Spinner label setup
  - Animation timing

## Test File Structure

### Setup and Teardown
- `setUpClass`: Initializes test environment and files
- `setUp`: Prepares each test case
- `tearDown`: Cleans up after each test
- `tearDownClass`: Restores original state

### Helper Functions
- `create_test_files()`: Creates necessary test files
- Debug logging for troubleshooting

## Test Data

### Test Files
- `test_employee_mood_data.csv`: Temporary mood data file for testing
- `test_last_notification.txt`: Temporary notification data file for testing

### Test Constants
- Emoji mappings
- State definitions
- Color schemes

## Error Handling

The test suite includes error handling for:
- File operations
- GUI component creation
- Animation states
- Data validation

## Debugging

### Debug Output
The test suite includes detailed debug output for:
- File operations
- Current working directory
- File paths and contents
- Mood selection states

### Common Issues
1. **File Permission Issues**
   - Ensure write permissions in test directory
   - Check file ownership

2. **GUI Testing Issues**
   - Logo loading errors (expected in test environment)
   - Window creation timing

3. **Animation Testing**
   - Timing-dependent tests
   - State verification

## Contributing

When adding new tests:
1. Follow existing test patterns
2. Include proper setup/teardown
3. Add debug logging
4. Update this documentation

## Future Improvements

Planned test suite enhancements:
1. Add coverage reporting
2. Implement integration tests
3. Add performance testing
4. Expand edge case testing 