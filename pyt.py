import pytesseract
from pdf2image import convert_from_path
import re
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image):
    # Function to preprocess images for better OCR results
    image = image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

def extract_invoice_details_natures(text):
    invoice_details = []
    
    # Split the text into lines
    lines = text.splitlines()
    
    for line in lines:
        # Match for date format
        date_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})'
        date_match = re.search(date_pattern, line)
        
        if date_match:
            # Extract the invoice date
            invoice_date = date_match.group(1)
            
            # Look for the invoice number in the same or preceding line
            # Assuming invoice number is directly before the date
            invoice_no_pattern = r'(\d{8})'
            
            # Check for invoice number in the current line after the date
            invoice_no_match = re.search(invoice_no_pattern, line[date_match.start():])
            if invoice_no_match:
                invoice_no = invoice_no_match.group(1)
                # Append the extracted details to the list
                if (invoice_no, invoice_date) not in invoice_details:
                    invoice_details.append((invoice_no, invoice_date))
            else:
                # If not found, look in the previous line
                previous_line_index = lines.index(line) - 1
                if previous_line_index >= 0:
                    prev_line = lines[previous_line_index]
                    invoice_no_match = re.search(invoice_no_pattern, prev_line)
                    if invoice_no_match:
                        invoice_no = invoice_no_match.group(1)
                        # Append the extracted details to the list
                        if (invoice_no, invoice_date) not in invoice_details:
                            invoice_details.append((invoice_no, invoice_date))
    
    return invoice_details


def leChef1(pdf_path):
    images = convert_from_path(pdf_path)
    invoice_details = []  # Store all details

    # Regular expression patterns
    invoice_no_pattern = r"INVOICE NO:\s*(\S+)"
    net_amount_pattern = r"NET AMOUNT:\s*USD\s*\$\s*([\d,]+\.\d{2})"
    invoice_date_pattern = r"INVOICE DATE:\s*(\S+)"

    for image in images:
        text = pytesseract.image_to_string(image)
        invoice_nos = re.findall(invoice_no_pattern, text)
        net_amounts = re.findall(net_amount_pattern, text)
        invoice_dates = re.findall(invoice_date_pattern, text)

        # Combine all details found on this page
        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))
    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def natures_online(pdf_path):
    images = convert_from_path(pdf_path)
    invoice_details = []

    invoice_no_pattern = r"Order Detail\s*-\s*Sales Order\s*#(\d+)"
    net_amount_pattern = r"\$\s*([\d,]+\.\d{2})"
    invoice_date_pattern = r"INVOICE DATE:\s*(\S+)"

    for image in images:
        text = pytesseract.image_to_string(image)
        invoice_nos = re.findall(invoice_no_pattern, text)
        net_amounts = re.findall(net_amount_pattern, text)
        invoice_dates = re.findall(invoice_date_pattern, text)

        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[-1] if net_amounts else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))

    return invoice_details
"""for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def natures(pdf_path):
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]  # Preprocess images to improve text extraction
    invoice_details = []

    # Regex patterns for extracting net amount
    net_amount_pattern = r"Net\s*:?\s*Total\s*:?\s*([\d,]+\.\d{2})"

    for image in images:
        # Convert image to string using pytesseract
        text = pytesseract.image_to_string(image)
        #print("Extracted Text:\n", text)

        # Use the custom function to extract invoice numbers and dates
        extracted_invoices = extract_invoice_details_natures(text)

        # Extract all net amounts from the text
        net_amounts = re.findall(net_amount_pattern, text)
        print(net_amounts)

        # Process each extracted invoice detail
        for invoice_no, invoice_date in extracted_invoices:
            # Assume the last net amount found applies to all extracted invoices if available
            net_amount = net_amounts[-1] if net_amounts else "Not found"
            
            # Check for uniqueness before adding
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))

    # Print all unique invoice details
    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def santaMonica(pdf_path):
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]
    invoice_details = []

    invoice_no_pattern = r'No[:\.\s]*(\d{7,})'
    net_amount_pattern = r'INVOICE\sTOTAL\s([\d,]+\.\d{2})'
    invoice_date_pattern = r'\b(\d{2}/\d{2}/\d{2})\b'

    for image in images:
        text = pytesseract.image_to_string(image)
        #print(text)
        invoice_nos = re.findall(invoice_no_pattern, text)
        net_amounts = re.findall(net_amount_pattern, text)
        invoice_dates = re.findall(invoice_date_pattern, text)

        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))

    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def usf(pdf_path):
    images = convert_from_path(pdf_path)
    invoice_details = []

    net_amount_pattern = r'\bDELIVERED\s+AMOUNT\s*[\$]?\s*([\d,]+\.\d{2})\b'
    header_pattern = r'ACCOUNT NUMBER\s+INVOICE NUMBER\s+INVOICE DATE'
    row_pattern = r'(\d+)\s+(\d{7})\s+(\d{2}/\d{2}/\d{4})'

    for image in images:
        text = pytesseract.image_to_string(image)
        net_amounts = re.findall(net_amount_pattern, text)
        header_match = re.search(header_pattern, text)

        if header_match:
            row_matches = re.findall(row_pattern, text)
            for match in row_matches:
                invoice_no = match[1]
                invoice_date = match[2]
                net_amount = net_amounts[-1] if net_amounts else "Not found"
                if not any(invoice_no == detail[0] for detail in invoice_details) and net_amount != 'Not found':
                    invoice_details.append((invoice_no, net_amount, invoice_date))

    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def wcPrime(pdf_path):
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]
    invoice_details = []

    invoice_no_pattern = r'\b(\d{7})\b'
    net_amount_pattern = r'\$([\d,]+\.\d{2})'
    invoice_date_pattern = r'\bInvoice\s*Date:\s*(\d{2}/\d{2}/\d{4})\b'

    for image in images:
        text = pytesseract.image_to_string(image)
        #print(text)
        invoice_nos = re.findall(invoice_no_pattern, text)
        net_amounts = re.findall(net_amount_pattern, text)
        invoice_dates = re.findall(invoice_date_pattern, text)

        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            if (invoice_no, net_amount, invoice_date) not in invoice_details and invoice_date != 'Not found':
                invoice_details.append((invoice_no, net_amount, invoice_date))

    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""


def ifs(pdf_path):
    images = convert_from_path(pdf_path)
    invoice_details = []

    invoice_no_pattern = r'Invoice\s*#:\s*(\d{6}-\d{2})'
    net_amount_pattern = r'\b\d+\.\d{2}\b'
    invoice_date_pattern = r'Order\s*Date:\s*(\d{2}/\d{2}/\d{4})'

    for image in images:
        text = pytesseract.image_to_string(image)
        invoice_nos = re.findall(invoice_no_pattern, text)
        net_amounts = re.findall(net_amount_pattern, text)
        invoice_dates = re.findall(invoice_date_pattern, text)

        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[-1] if net_amounts else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))

    return invoice_details
    """for details in invoice_details:
        print(f"Invoice No: {details[0]}")
        print(f"Net Amount: USD ${details[1]}")
        print(f"Invoice Date: {details[2]}")
        print("---")"""




def extract_invoice_details(text):
    invoice_no = None
    invoice_date = None
    
    lines = text.splitlines()
    for line in lines:
        # Match for date format
        date_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})'
        date_match = re.search(date_pattern, line)
        
        if date_match:
            # Extract the invoice date
            invoice_date = date_match.group(1)
            # Look for invoice number in the same or preceding line
            # Extract numbers before the date (assuming invoice number is directly before)
            invoice_no_pattern = r'(\d{8})'
            invoice_no_match = re.search(invoice_no_pattern, line[:date_match.start()])
            if invoice_no_match:
                invoice_no = invoice_no_match.group(1)
    
    return invoice_no, invoice_date

def iD(pdf_path):
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]
    invoice_nos = []
    net_amounts = []
    invoice_dates = []
    invoice_details = []

    net_amount_pattern = r'BALANCE DUE\s*([\d,]+\.\d{2})'

    for image in images:
        text = pytesseract.image_to_string(image)
        
        invoice_no, invoice_date = extract_invoice_details(text)
        
        if invoice_no:
            invoice_nos.append(invoice_no)
        if invoice_date:
            invoice_dates.append(invoice_date)
        
        net_amount_match = re.search(net_amount_pattern, text)
        if net_amount_match:
            net_amounts.append(net_amount_match.group(1))

        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            #print(i)
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))

    """print(f"Invoice Nos: {invoice_nos}")
    print(f"Invoice Dates: {invoice_dates}")
    print(f"Balance Dues: ${net_amounts}")"""

    return invoice_details



import re
import pytesseract
from pdf2image import convert_from_path

def mbc(pdf_path):
    # Convert the PDF to images (assuming your existing logic)
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]
    
    # Initialize empty lists to store extracted values
    invoice_nos = []
    net_amounts = []
    invoice_dates = []
    invoice_details = []

    # Define regex patterns
    invoice_no_pattern = r'Invoice\s*#:\s*(\d+)'
    net_amount_pattern = r'Total:\s*\$([\d,]+\.\d{2})'
    invoice_date_pattern = r'Delivery\s*Date:\s*(\d{1,2}/\d{1,2}/\d{4})'  # Matches 'Delivery Date: 8/19/2024'

    # Iterate over each image (PDF page)
    for image in images:
        # Convert image to text using pytesseract
        text = pytesseract.image_to_string(image)

        # Search for patterns and append extracted values to lists
        invoice_no_match = re.search(invoice_no_pattern, text)
        if invoice_no_match:
            invoice_nos.append(invoice_no_match.group(1))
        #print(invoice_nos)

        net_amount_match = re.search(net_amount_pattern, text)
        if net_amount_match:
            net_amounts.append(net_amount_match.group(1))
        #print(net_amounts)

        invoice_date_match = re.search(invoice_date_pattern, text)
        if invoice_date_match:
            invoice_dates.append(invoice_date_match.group(1))
        #print(invoice_dates)
        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            #print(i)
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))
            #print(invoice_details)
    """invoice_nos = list(invoice_nos) if invoice_nos else ["Not found"]
    net_amounts = list(net_amounts) if net_amounts else ["Not found"]
    invoice_dates = list(invoice_dates) if invoice_dates else ["Not found"]


    # Create invoice details list
    invoice_details = [
        {"Invoice No": invoice_no, "Delivery Date": delivery_date, "Total Amount": net_amount}
        for invoice_no, delivery_date, net_amount in zip(invoice_nos, invoice_dates, net_amounts)
    ]"""

    return invoice_details




def rb(pdf_path):
    images = convert_from_path(pdf_path)
    images = [preprocess_image(image) for image in images]

    # Using sets to store unique values
    invoice_nos = []
    net_amounts = []
    invoice_dates = []
    invoice_details = []

    invoice_no_pattern = r'Invoice\s*No\.\s*(\w+-\d+)'
    net_amount_pattern = r"Remaining\s*Balance\s*\$\s*([\d,]+\.\d{2})"
    invoice_date_pattern = r"Invoice\s*Date\s*(\d{1,2}/\d{1,2}/\d{4})"

    for image in images:
        # Convert image to string using pytesseract
        text = pytesseract.image_to_string(image)

        # Search for patterns in the text and add unique values to sets
        invoice_no_match = re.search(invoice_no_pattern, text)
        if invoice_no_match:
            invoice_nos.append(invoice_no_match.group(1))

        net_amount_match = re.search(net_amount_pattern, text)
        if net_amount_match:
            net_amounts.append(net_amount_match.group(1))

        invoice_date_match = re.search(invoice_date_pattern, text)
        if invoice_date_match:
            invoice_dates.append(invoice_date_match.group(1))

    # Convert sets to lists for easier display
        for i, invoice_no in enumerate(invoice_nos):
            net_amount = net_amounts[i] if i < len(net_amounts) else "Not found"
            invoice_date = invoice_dates[i] if i < len(invoice_dates) else "Not found"
            #print(i)
            if (invoice_no, net_amount, invoice_date) not in invoice_details:
                invoice_details.append((invoice_no, net_amount, invoice_date))
    return invoice_details


# Main Input Handling Code
"""inp = int(input(\"""1 for Le Chef Bakery
2 for Nature's Produce Online
3 for Nature's Produce
4 for Santa Monica Seafood
5 for US Foods
6 for West Coast Prime Meats
7 for Individual Food Service
8 for Imperial Dade
9 for Melrose Baking Company
10 for Rockenwagner Bakery
\"""))
pdf_path = input("Enter PDF path: ")

if inp == 1:
    print(leChef1(pdf_path))
elif inp == 2:
    natures_online(pdf_path)
elif inp == 3:
    natures(pdf_path)
elif inp == 4:
    santaMonica(pdf_path)
elif inp == 5:
    usf(pdf_path)
elif inp == 6:
    wcPrime(pdf_path)
elif inp == 7:
    ifs(pdf_path)
elif inp == 8:
    iD(pdf_path)
elif inp == 9:
    mbc(pdf_path)
elif inp == 10:
    rb(pdf_path)
else:
    print("Input is Invalid")

'/Users/reetvikchatterjee/Downloads/ifsSample19.pdf'
"""