# PDF Data Extraction with Error Handling and Edge-Case Management

## Introduction

This Python script is designed to extract structured data from invoice PDFs using regular expressions (`regex`) and `pdfplumber`. It aims to tackle common challenges in document processing, such as multi-page PDFs, table rows that span multiple lines, and complex data extraction scenarios. Additionally, advanced error handling is implemented to manage unexpected situations, like missing or inconsistent data.

## Features

- **Text extraction from PDFs:** Extracts all the text from a given PDF file using `pdfplumber`.
- **Regex-based extraction:** Patterns are defined to extract key information such as Invoice Number, Customer Name, VAT Number, and more.
- **Multi-format Invoice Amount extraction:** Handles numeric values, including amounts written in words.
- **Generalized data extraction patterns:** Uses regex to identify specific fields like dates, customer numbers, and total amounts.
- **Error handling and validation:** Provides fallback values and error handling when data is inconsistent or missing.
- **Test cases for validation:** Ensures that the extraction functions work correctly with different input formats.
- **Customizable extraction template:** Generates a JSON template based on the fields and patterns used in extraction.
  
## Setup Instructions

### Prerequisites

Make sure you have Python 3.x installed, along with the following required libraries:

```bash
pip install pdfplumber word2number re
```

### Running the Script

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/pdf-data-extraction.git
    cd pdf-data-extraction
    ```

2. Place your PDF invoice file in the project directory. Update the `pdf_path` variable in the script to the path of your PDF file. By default, the script looks for:

    ```python
    pdf_path = "C:/Users/Project/annotation/sample-invoice.pdf"
    ```

3. Run the script:

    ```bash
    python extract_data.py
    ```

4. The script will extract the relevant information from the invoice and generate two output files:
   - `extracted_data.json`: Contains the extracted data (e.g., invoice number, VAT, customer information).
   - `extraction_template.json`: Contains the extraction template showing the regex rules used for extracting data.

### Example Output

Here is an example of how the extracted data may look:

```json
{
    "VAT Number": ["GB123456789"],
    "Invoice No": ["123456"],
    "Customer Name": ["John Doe"],
    "Customer Number": ["987654"],
    "Invoice Period": ["01.01.2024 - 31.01.2024"],
    "Date": ["15 Jan 2024"],
    "Total Amount": ["1,500.00"],
    "VAT": ["20"],
    "Gross Amount": ["1,800.00"],
    "Service Fees": ["Basic Fee Package 200.00 €"]
}
```

## Code Overview

### `textExtraction(pdf_path)`

This function opens the PDF file and extracts the text from all pages. It uses the `pdfplumber` library to read the content of each page, appending them into a single string.

```python
def textExtraction(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text
```

### Regex Patterns for Data Extraction

A dictionary of regex patterns is defined to identify and extract fields such as VAT number, invoice number, customer name, total amount, etc.

```python
patterns = {
    "VAT Number": r"VAT No\.\s+([A-Z]{2}\d+)",
    "Invoice No": r"Invoice No\s+(\d+)",
    "Customer Name": r"Name:\s+([\w\s]+)",
    ...
}
```

The `for` loop iterates over each field and applies the corresponding regex to the extracted text.

### Error Handling

The script includes error handling to ensure the program does not crash if expected data is missing or inconsistent. For example, if no match is found for a particular field, it returns `None`.

```python
extracted_data[field] = match if match else None
```

### Extraction of Invoice Amounts

The `extract_invoice_amount` function is designed to extract the invoice amounts in different formats (e.g., numeric values or words). If an amount is found in words, it uses the `word2number` library to convert it to a numeric value.

```python
def extract_invoice_amount(value_content):
    patterns = [
        r"Total Amount:\s*\$?(\d+[,.]?\d*)",   
        r"Amount Due:\s*\$?(\d+[,.]?\d*)",     
        r"Amount:\s*\$?(\d+[,.]?\d*)",         
        r"(\w+\s+\w+)",                        
    ]
    
    ...
```

### Template and Data Export

- The extraction template is saved as `extraction_template.json` for future reference.
- The extracted data is saved as `extracted_data.json`.

### Test Cases

The script includes a set of test cases for the `extract_invoice_amount` function. Each case validates the correct extraction of amounts in different formats.

```python
def test_extract_invoice_amount():
    test_cases = [
        {"input": "Total Amount: $500", "expected": "500"},
        {"input": "Amount Due: 500.00", "expected": "500.00"},
        {"input": "Amount: 1000", "expected": "1000"},
        ...
    ]
    
    ...
```

## Handling Complex Scenarios

### Multi-page PDF and Table Row Spanning

To handle multi-page PDFs and table rows that span multiple lines, the script aggregates the text from all pages into a single string using `pdfplumber`. Then, regex is applied across the entire text to ensure data spanning multiple pages is captured.

### Error Handling for Missing or Inconsistent Data

The script implements error handling for scenarios where expected data is missing, incomplete, or formatted incorrectly. It uses `try-except` blocks and regex validation to provide meaningful error messages and fallback values.

For example, when extracting an amount written in words:

```python
def amount_in_words_to_number(amount_in_words):
    try:
        return str(w2n.word_to_num(amount_in_words))
    except ValueError:
        return "N/A"
```
