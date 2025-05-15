from fpdf import FPDF
from io import BytesIO

class PDF(FPDF): # Extends FPDF class
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self, title_str):
        self.set_font('Arial', 'B', 12)
        # Remove potential leading/trailing colons or asterisks if LLM is inconsistent
        clean_title = title_str.strip().rstrip(':').strip('* ')
        self.cell(0, 6, clean_title + ":", 0, 1, 'L') # Ensure colon is present for consistency
        self.ln(2)

    def chapter_body(self, body_text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body_text)
        self.ln(3)

    def add_metadata_section(self, metadata_text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, metadata_text)
        self.ln(4)

def create_soap_pdf_bytes(soap_text: str) -> BytesIO:
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15) # Left, Top, Right

    lines = soap_text.split('\n')
    current_section_content = []
    metadata_ended = False
    metadata_buffer = []

    section_headers_plain = ["Subjective", "Objective", "Assessment", "Plan"] # Check without colon
    # Keywords to identify metadata lines (case-insensitive check)
    metadata_keywords_plain = [
        "client full name", "client date of birth", "date of service",
        "exact start time and end time", "session location", "diagnosis"
    ]

    first_main_section_found = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        # Normalize by removing trailing colon for checks, but preserve it for metadata output
        normalized_line_for_check = stripped_line.rstrip(':').lower()

        # Phase 1: Accumulate metadata lines
        if not metadata_ended:
            is_metadata_line = any(normalized_line_for_check.startswith(keyword) for keyword in metadata_keywords_plain)
            is_section_header_line = any(normalized_line_for_check == header.lower() for header in section_headers_plain)
            
            if is_metadata_line:
                metadata_buffer.append(line) # Keep original line
                continue
            elif metadata_buffer and (is_section_header_line or (not stripped_line and i > 0 and lines[i-1].strip() != "")): # End of metadata if section header or true blank line after content
                pdf.add_metadata_section("\n".join(metadata_buffer).strip())
                metadata_buffer = []
                metadata_ended = True

        # Phase 2: Process main SOAP sections
        if metadata_ended or not metadata_buffer: # Start processing sections if metadata done or no metadata was found
            is_current_line_main_header = False
            for header_plain in section_headers_plain:
                if normalized_line_for_check == header_plain.lower(): # Check against "Subjective", not "Subjective:"
                    if current_section_content: # Write previous section if any
                        pdf.chapter_body("\n".join(current_section_content).strip())
                        current_section_content = []
                    
                    pdf.chapter_title(stripped_line.rstrip(':')) # Pass "Subjective" or "Subjective:" to get "Subjective:"
                    is_current_line_main_header = True
                    if not first_main_section_found:
                        first_main_section_found = True # Mark that we've started the main SOAP content
                    break
            
            if not is_current_line_main_header and (first_main_section_found or not section_headers_plain): # Add to content if not a header AND we are in main SOAP body
                if stripped_line or current_section_content: # Add line if it has content or if we are in middle of a paragraph
                    current_section_content.append(line)
    
    # After the loop, write any remaining content
    if current_section_content:
        pdf.chapter_body("\n".join(current_section_content).strip())
    if metadata_buffer: # If file ends with metadata
        pdf.add_metadata_section("\n".join(metadata_buffer).strip())

    pdf_bytes_io = BytesIO()
    pdf.output(pdf_bytes_io)
    pdf_bytes_io.seek(0)
    return pdf_bytes_io