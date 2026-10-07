"""
SmartHire — Resume Parsing Module
Author: SmartHire ML Team
Description: Extracts raw text content from uploaded resume files (PDF, DOCX, TXT).
             Uses pypdf and python-docx for high-precision text extraction.
"""

import re
import io
import pypdf
import docx

def extract_text_from_bytes(content: bytes, filename: str) -> str:
    """
    Extracts readable text from raw file bytes.
    Supports PDF, DOCX, and TXT files.
    """
    filename_lower = filename.lower()
    
    # 1. PDF files (.pdf)
    if filename_lower.endswith(".pdf"):
        try:
            reader = pypdf.PdfReader(io.BytesIO(content))
            extracted_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
            
            full_text = "\n".join(extracted_pages).strip()
            if full_text and len(full_text) > 20:
                return full_text
        except Exception as e:
            print(f"Warning: pypdf extraction failed for {filename}: {e}")

        # Fallback PDF extraction
        raw_text = content.decode("latin-1", errors="ignore")
        chunks = re.findall(r'[\w\s\.,;:!\?\-\(\)/@]{4,}', raw_text)
        return " ".join([c.strip() for c in chunks if len(c.strip()) > 3])

    # 2. DOCX files (.docx / .doc)
    if filename_lower.endswith(".docx") or filename_lower.endswith(".doc"):
        try:
            doc = docx.Document(io.BytesIO(content))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from tables if present
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            paragraphs.append(cell.text.strip())

            full_text = "\n".join(paragraphs).strip()
            if full_text and len(full_text) > 20:
                return full_text
        except Exception as e:
            print(f"Warning: python-docx extraction failed for {filename}: {e}")

        # Fallback DOCX extraction
        raw_text = content.decode("latin-1", errors="ignore")
        chunks = re.findall(r'[\w\s\.,;:!\?\-\(\)/@]{4,}', raw_text)
        return " ".join([c.strip() for c in chunks if len(c.strip()) > 3])

    # 3. Plain Text files (.txt)
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1", errors="ignore")
