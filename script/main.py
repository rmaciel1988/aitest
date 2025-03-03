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
    #normalized_messages = [msg.strip().lower().replace('"', '') for msg in messages]
    phrases_count = Counter(messages)

    # most common errors:
    pattern = r"\] (\w+) - (.+)"

    matches = re.findall(pattern, logs)

    error_msg = []

    for msg_type, text in matches:
        #text = text.strip().lower().replace('"', '')
        if msg_type == 'ERROR':
            error_msg.append(text)

    error_counts = Counter(error_msg)
    error_counts = dict(sorted(error_counts.items(), key=lambda item: item[1], reverse=True))

    i = 0
    error_msgs = ""
    for k in error_counts:
        i = i + 1
        error_msgs += f"{i}. {k} ({error_counts[k]} times)\n"
    error_msgs = error_msgs.strip()


    info_count = type_count.get('INFO',0)
    error_count = type_count.get('ERROR',0)
    warning_count = type_count.get('WARNING',0)

    phrases_agent = {}
    phrases_count = dict(sorted(phrases_count.items(), key=lambda item: item[1], reverse=True))
    for k in phrases_count.keys():
        if 'Agent Response:' in k:
            phrases_agent[k.replace('Agent Response:','')] = f'({phrases_count[k]} times)'


    i = 0
    agent_responses = "Top {} AI Responses:\n".format(len(phrases_agent))
    for k in phrases_agent:
        i = i + 1
        agent_responses += f"{i}. {k} {phrases_agent[k]}\n"
    agent_responses = agent_responses.strip()


    report = f'''
    Log Summary:
    - INFO messages: {info_count} 
    - ERROR messages: {error_count}
    - WARNING messages: {warning_count}

    {agent_responses}

    Most Common Errors:
    {error_msgs}
    '''
    return report

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    report = analyze_logs("sample.log")
    print(report)

