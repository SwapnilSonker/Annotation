import pdfplumber
import json
import re
from word2number import w2n

pdf_path = "C:/Users/Project/annotation/sample-invoice.pdf"

# Function to extract text from multiple pages and handle multi-page PDFs
def textExtraction(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Add text from all pages
        return text

extracted_text = textExtraction(pdf_path)

# Updated extraction patterns for complex scenarios (multi-line, etc.)
patterns = {
    "VAT Number": r"VAT No\.\s+([A-Z]{2}\d+)",
    "Invoice No": r"Invoice No\s+(\d+)",
    "Customer Name": r"Name:\s+([\w\s]+)",
    "Customer Number": r"Invoice No Customer No Invoice Period Date\n\d+\s+(\d+)",
    "Invoice Period": r"Invoice No Customer No Invoice Period Date\n\d+\s+\d+\s+(\d{1,2}\.\d{1,2}\.\d{4}\s+-\s+\d{1,2}\.\d{1,2}\.\d{4})",
    "Date": r"Invoice No Customer No Invoice Period Date\n\d+\s+\d+\s+\d{1,2}\.\d{1,2}\.\d{4}\s+-\s+\d{1,2}\.\d{1,2}\.\d{4}\s+(\d{1,2}\.\s\w+\s\d{4})",
    "Total Amount": r"Total\s+([\d,.]+) €",
    "VAT": r"VAT\s+(\d{1,2}) %",
    "Gross Amount": r"Gross Amount incl. VAT\s+([\d,.]+) €",
    "Service Fees": r"(Basic Fee [\w\s]+[\d,.]+ €)"
}

# Extract the data using the patterns
extracted_data = {}
for field, pattern in patterns.items():
    match = re.findall(pattern, extracted_text, re.DOTALL)  # Use re.DOTALL for multi-line handling
    extracted_data[field] = match if match else None

# Advanced error handling: if a field is missing, provide a fallback message
def safe_extract(field, pattern, text):
    try:
        match = re.findall(pattern, text, re.DOTALL)
        return match if match else f"Data for {field} not found"
    except re.error as e:
        return f"Error in extracting {field}: {str(e)}"

# Applying safe extraction with error handling for each field
for field, pattern in patterns.items():
    extracted_data[field] = safe_extract(field, pattern, extracted_text)

# Function to extract invoice amounts with advanced error handling
def extract_invoice_amount(value_content):
    patterns = [
        r"Total Amount:\s*\$?(\d+[,.]?\d*)",   # Total Amount: $500 or Total Amount: 500
        r"Amount Due:\s*\$?(\d+[,.]?\d*)",     # Amount Due: 500.00
        r"Amount:\s*\$?(\d+[,.]?\d*)",         # Amount: 500
        r"(\w+\s+\w+)",                        # Amount in words, e.g., "Five Hundred"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, value_content)
        if match:
            # Handle the case where the amount is in words
            amount = match.group(1)
            if re.match(r"\d+", amount):  # If the match is numeric
                return amount
            else:
                return amount_in_words_to_number(amount)  # Convert words to numbers
    
    # Return "N/A" if no amount is found
    return "N/A"

# Function to convert amount in words to numbers using word2number
def amount_in_words_to_number(amount_in_words):
    try:
        return str(w2n.word_to_num(amount_in_words))  # Ensure the return value is a string
    except ValueError:
        return "N/A"

# Error handling and tests for extract_invoice_amount
def test_extract_invoice_amount():
    test_cases = [
        {"input": "Total Amount: $500", "expected": "500"},
        {"input": "Amount Due: 500.00", "expected": "500.00"},
        {"input": "Amount: 1000", "expected": "1000"},
        {"input": "Amount: Five Hundred", "expected": "500"},  # Handles amount in words
        {"input": "Amount:", "expected": "N/A"},               # Handles missing amount
    ]
    
    for idx, case in enumerate(test_cases):
        try:
            result = extract_invoice_amount(case["input"])
            assert result.strip() == case["expected"].strip(), f"Test case {idx+1} failed: expected {case['expected']}, got {result}"
            print(f"Test case {idx+1} passed!")
        except Exception as e:
            print(f"Test case {idx+1} encountered an error: {str(e)}")

# Run the test cases
test_extract_invoice_amount()

# Optionally, you can also return or display the extracted data for verification
print("Extracted Data:", extracted_data)

# Save the extraction template
extraction_template = {
    field: {"rule": f"Extract using pattern: '{pattern}'"} for field, pattern in patterns.items()
}
with open('extraction_template.json', 'w') as json_file:
    json.dump(extraction_template, json_file, indent=4)

# Save extracted data to a separate JSON file
with open('extracted_data.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

if __name__ == "__main__":
    extracted_text = textExtraction(pdf_path)
    test_extract_invoice_amount()
