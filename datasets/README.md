# Datasets Directory

This directory stores training datasets.

## Structure

Datasets uploaded through the web interface are stored in:
```
backend/uploads/datasets/
```

This directory is for reference and documentation purposes.

## Supported Formats

### JSON Format
```json
[
  {
    "code": "function vulnerable_code() { eval(user_input); }",
    "label": 1,
    "vulnerability_type": "Code Injection"
  },
  {
    "code": "function safe_code() { return sanitized_input; }",
    "label": 0,
    "vulnerability_type": "None"
  }
]
```

### CSV Format
```csv
code,label,vulnerability_type
"eval(user_input)",1,"Code Injection"
"sanitized_input",0,"None"
```

## Dataset Requirements

- **code**: Code snippet or function
- **label**: 0 (safe) or 1 (vulnerable)
- **vulnerability_type**: Type of vulnerability (optional)

## Usage

Datasets are managed through the web interface:
1. Navigate to "Dataset Management"
2. Click "Upload Dataset"
3. Fill in dataset information
4. Select dataset file
5. Upload

System will automatically analyze:
- Number of samples
- Vulnerable vs safe samples
- Format validation
- Statistics

## Best Practices

- Balance vulnerable and safe samples
- Include diverse vulnerability types
- Use consistent data format
- Validate labels
- Document data sources
- Include sufficient samples (recommended: 1000+)

## Sample Data

A sample dataset is provided in the documentation for testing purposes.
