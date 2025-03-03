import os
import tempfile
import pytest
from main import analyze_logs

def create_test_log(content):
    """Create a temporary log file with the given content for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as f:
        f.write(content)
    return temp_file.name

def compare_reports(actual, expected):
    """Compare actual and expected reports, ignoring whitespace"""
    actual_lines = [line.strip() for line in actual.split('\n') if line.strip()]
    expected_lines = [line.strip() for line in expected.split('\n') if line.strip()]
    return actual_lines == expected_lines

def test_basic_log_analysis():
    """Test basic log analysis functionality"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
"""
    log_path = create_test_log(log_content)
    
    report = analyze_logs(log_path)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_report = """Log Summary:
- INFO messages: 2
- ERROR messages: 1
- WARNING messages: 0"""
    
    assert compare_reports(report, expected_report), f"Expected:\n{expected_report}\n\nGot:\n{report}"

def test_response_extraction():
    """Test that AI responses are correctly extracted and counted"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
"""
    log_path = create_test_log(log_content)
    
    report = analyze_logs(log_path)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_responses = """Top 3 AI Responses:
1. "Hello! How can I help you today?" (3 times)
2. "I'm sorry, I didn't understand that." (1 times)"""
    
    assert expected_responses in report, f"Expected responses not found in report:\n{report}"

def test_error_extraction():
    """Test that errors are correctly extracted and counted"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] ERROR - API Connection Failure
[2025-02-20 14:35:20] ERROR - Model Timeout after 5000ms
[2025-02-20 14:36:45] ERROR - Invalid Response Format
"""
    log_path = create_test_log(log_content)
    
    report = analyze_logs(log_path)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_errors = """Most Common Errors:
1. Model Timeout after 5000ms (2 times)
2. API Connection Failure (1 times)
3. Invalid Response Format (1 times)"""
    
    assert expected_errors in report, f"Expected errors not found in report:\n{report}"

def test_full_report_format():
    """Test the complete format of the report"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] WARNING - Response latency high: 2500ms
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:37:30] ERROR - API Connection Failure
[2025-02-20 14:38:12] INFO - Agent Response: "Please provide more details."
[2025-02-20 14:39:55] WARNING - Memory usage high: 85%
[2025-02-20 14:40:33] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:41:22] ERROR - Model Timeout after 5000ms
"""
    log_path = create_test_log(log_content)
    
    report = analyze_logs(log_path)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_report = """Log Summary:
- INFO messages: 4
- ERROR messages: 3
- WARNING messages: 2

Top 3 AI Responses:
1. "Hello! How can I help you today?" (3 times)
2. "I'm sorry, I didn't understand that." (1 times)
3. "Please provide more details." (1 times)

Most Common Errors:
1. Model Timeout after 5000ms (2 times)
2. API Connection Failure (1 times)"""
    
    assert compare_reports(report, expected_report), f"Expected:\n{expected_report}\n\nGot:\n{report}"

def test_empty_log_file():
    """Test handling of empty log file"""
    log_path = create_test_log("")
    
    report = analyze_logs(log_path)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_report = """Log Summary:
- INFO messages: 0
- ERROR messages: 0
- WARNING messages: 0

Top 3 AI Responses:
No AI responses found

Most Common Errors:
No errors found"""
    
    assert compare_reports(report, expected_report), f"Expected:\n{expected_report}\n\nGot:\n{report}"

def test_custom_top_n():
    """Test customizing the number of top items to display"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] WARNING - Response latency high: 2500ms
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:37:30] ERROR - API Connection Failure
[2025-02-20 14:38:12] INFO - Agent Response: "Please provide more details."
[2025-02-20 14:39:55] WARNING - Memory usage high: 85%
[2025-02-20 14:40:33] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:41:22] ERROR - Model Timeout after 5000ms
[2025-02-20 14:42:15] ERROR - Invalid Response Format
[2025-02-20 14:43:40] INFO - Agent Response: "Thank you for your question."
"""
    log_path = create_test_log(log_content)
    
    report = analyze_logs(log_path, top_responses=4, top_errors=3)
    
    # Clean up the temporary file
    os.unlink(log_path)
    
    expected_report = """Log Summary:
- INFO messages: 5
- ERROR messages: 4
- WARNING messages: 2

Top 4 AI Responses:
1. "Hello! How can I help you today?" (3 times)
2. "I'm sorry, I didn't understand that." (1 times)
3. "Please provide more details." (1 times)
4. "Thank you for your question." (1 times)

Most Common Errors:
1. Model Timeout after 5000ms (2 times)
2. API Connection Failure (1 times)
3. Invalid Response Format (1 times)"""
    
    assert compare_reports(report, expected_report), f"Expected:\n{expected_report}\n\nGot:\n{report}"

