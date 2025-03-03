import re
from collections import Counter

def analyze_logs(log_file_path, top_responses=3, top_errors=2):
    """
    Analyze log file and generate a structured report.
    
    Args:
        log_file_path (str): Path to the log file
        top_responses (int): Number of top responses to include
        top_errors (int): Number of top errors to include
        
    Returns:
        str: Formatted report string with log summary,
             top AI responses, and most common errors
    """
    # TODO: Implement this function

    logs = read_file(log_file_path)
    
    # type count
    pattern = r"\] (\w+) -"
    message_types = re.findall(pattern, logs)
    type_count = Counter(message_types)

    # most used phrases
    pattern = r"- (.+)"
    messages = re.findall(pattern, logs)
    normalized_messages = [msg.strip().lower().replace('"', '') for msg in messages]
    phrases_count = Counter(normalized_messages)

    # most common errors:
    pattern = r"\] (\w+) - (.+)"

    matches = re.findall(pattern, logs)

    error_msg = []

    for msg_type, text in matches:
        text = text.strip().lower().replace('"', '')
        if msg_type == 'ERROR':
            error_msg.append(text)

    error_counts = Counter(error_msg)

    print(f'Total of errors {error_counts}')




    '''
    Log Summary:
    - INFO messages: 42
    - ERROR messages: 8
    - WARNING messages: 5

    Top 3 AI Responses:
    1. "Hello! How can I help you today?" (12 times)
    2. "I'm sorry, I didn't understand that." (7 times)
    3. "Please provide more details." (5 times)

    Most Common Errors:
    1. Model Timeout after 5000ms (3 times)
    2. API Connection Failure (2 times)
    '''







    return read_file(log_file_path)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    report = analyze_logs("sample.log")
    print(report)

