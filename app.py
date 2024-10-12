
import pdfplumber
import json
import re
from word2number import w2n  

pdf_path = "C:/Users/Project/annotation/sample-invoice.pdf"

def textExtraction(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text

extracted_text = textExtraction(pdf_path)

# Define patterns for extracting various fields
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

extracted_data = {}
for field, pattern in patterns.items():
    match = re.findall(pattern, extracted_text)
    extracted_data[field] = match if match else None

# Create the extraction template
extraction_template = {
    field: {"rule": f"Extract using pattern: '{pattern}'"} for field, pattern in patterns.items()
}

# Save the extraction template to a JSON file
with open('extraction_template.json', 'w') as json_file:
    json.dump(extraction_template, json_file, indent=4)

# Save extracted data to a separate JSON file
with open('extracted_data.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

# Function to extract invoice amounts with different formats
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
            # Handle the case where amount is in words
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

# Test cases for the extract_invoice_amount function
def test_extract_invoice_amount():
    test_cases = [
        {"input": "Total Amount: $500", "expected": "500"},
        {"input": "Amount Due: 500.00", "expected": "500.00"},
        {"input": "Amount: 1000", "expected": "1000"},
        {"input": "Amount: Five Hundred", "expected": "500"},  # Now this will pass
        {"input": "Amount:", "expected": "N/A"},               # Missing amount
    ]
    
    for idx, case in enumerate(test_cases):
        result = extract_invoice_amount(case["input"])
        # Ensure both result and expected are stripped and compared as strings
        assert result.strip() == case["expected"].strip(), f"Test case {idx+1} failed: expected {case['expected']}, got {result}"
        print(f"Test case {idx+1} passed!")

# Run the test cases
test_extract_invoice_amount()

# Optionally, you can also return or display the extracted data for verification
print("Extracted Data:", extracted_data)

if __name__ == "__main__":
    extracted_text = textExtraction(pdf_path)
    # Test the extract_invoice_amount function
    test_extract_invoice_amount()




