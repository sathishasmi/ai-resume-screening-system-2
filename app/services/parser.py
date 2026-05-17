import re
from PyPDF2 import PdfReader


# Extract text from PDF

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except:
        text = ""
    return text



# Extract Email

def extract_email(text):
    match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match[0] if match else "Not Found"



# Extract Phone

def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s-]{8,}\d", text)
    return match[0] if match else "Not Found"


# Extract Name

def extract_name(text):
    lines = text.split("\n")

    for line in lines[:10]:  # check first 10 lines
        line = line.strip()

        if not line:
            continue

        # Skip unwanted lines
        if any(word in line.lower() for word in ["resume", "cv", "profile", "email", "phone"]):
            continue

        # Skip if contains numbers or email
        if "@" in line or any(char.isdigit() for char in line):
            continue

        # Likely name (2–4 words)
        if 2 <= len(line.split()) <= 4:
            return line

    return "Candidate"



# MAIN FUNCTION

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    return {
        "text": text.lower(),
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }