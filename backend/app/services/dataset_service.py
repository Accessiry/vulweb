import json
import csv

def analyze_dataset(file_path, file_format):
    """Analyze dataset and extract statistics"""
    try:
        if file_format == 'json':
            return analyze_json_dataset(file_path)
        elif file_format == 'csv':
            return analyze_csv_dataset(file_path)
        else:
            return None
    except Exception as e:
        raise Exception(f"Failed to analyze dataset: {str(e)}")

def analyze_json_dataset(file_path):
    """Analyze JSON dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if isinstance(data, list):
        num_samples = len(data)
        # Assuming dataset has 'label' or 'vulnerable' field
        num_vulnerable = sum(1 for item in data if item.get('label') == 1 or item.get('vulnerable') == True)
        num_safe = num_samples - num_vulnerable
        
        return {
            'num_samples': num_samples,
            'num_vulnerable': num_vulnerable,
            'num_safe': num_safe
        }
    
    return None

def analyze_csv_dataset(file_path):
    """Analyze CSV dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    num_samples = len(rows)
    # Assuming dataset has 'label' or 'vulnerable' column
    num_vulnerable = sum(1 for row in rows if row.get('label') == '1' or row.get('vulnerable') == 'True')
    num_safe = num_samples - num_vulnerable
    
    return {
        'num_samples': num_samples,
        'num_vulnerable': num_vulnerable,
        'num_safe': num_safe
    }
