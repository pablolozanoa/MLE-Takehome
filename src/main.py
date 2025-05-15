import os
from .process_transcript import generate_soap_note_from_transcript
from .pdf_generator import create_soap_pdf_bytes

TRANSCRIPTS_DIR = "transcripts"             # Relative to project root
OUTPUT_TXT_DIR = "output_soap_notes_txt"            # Relative to project root
OUTPUT_PDF_DIR = "output_soap_notes_pdf"    # Relative to project root

def process_all_transcripts():
    """
    Iterates over all transcript files in TRANSCRIPTS_DIR,
    generates a SOAP note for each, and saves it as both .txt and .pdf
    in their respective output directories.
    """

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    transcripts_full_path = os.path.join(project_root, TRANSCRIPTS_DIR)
    output_text_full_path = os.path.join(project_root, OUTPUT_TXT_DIR)
    output_pdf_full_path = os.path.join(project_root, OUTPUT_PDF_DIR)

    if not os.path.exists(transcripts_full_path):
        print(f"Transcripts directory not found: {transcripts_full_path}")
        return

    if not os.path.exists(output_text_full_path):
        os.makedirs(output_text_full_path)
        print(f"Output directory created: {output_text_full_path}")
    
    if not os.path.exists(output_pdf_full_path):
        os.makedirs(output_pdf_full_path)
        print(f"PDF output directory created: {output_pdf_full_path}")

    transcript_files = [f for f in os.listdir(transcripts_full_path) if f.endswith(".txt")]

    if not transcript_files:
        print(f"No .txt files found in {transcripts_full_path}")
        return

    print(f"Found {len(transcript_files)} transcript files to process.")

    for filename in transcript_files:
        transcript_file_path = os.path.join(transcripts_full_path, filename)
        output_filename = os.path.splitext(filename)[0] + "_soap.txt"
        output_file_path = os.path.join(output_text_full_path, output_filename)
        output_pdf_file_path = os.path.join(output_pdf_full_path, os.path.splitext(filename)[0] + "_soap.pdf")


        print(f"\nProcessing: {transcript_file_path}...")

        try:
            with open(transcript_file_path, 'r', encoding='utf-8') as f:
                transcript_content = f.read()
            
            if not transcript_content.strip():
                print(f"File {filename} is empty. Skipping.")
                continue

            soap_note = generate_soap_note_from_transcript(transcript_content)

            if soap_note:
                with open(output_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(soap_note)
                print(f"SOAP note saved to: {output_file_path}")

                try:
                    pdf_bytes = create_soap_pdf_bytes(soap_note)
                    with open(output_pdf_file_path, 'wb') as f_out_pdf: # 'wb' for writing bytes
                        f_out_pdf.write(pdf_bytes.getvalue()) # getvalue() from BytesIO
                    print(f"PDF SOAP note saved to: {output_pdf_file_path}")
                except Exception as pdf_e:
                    print(f"Error generating or saving PDF for {filename}: {pdf_e}")
            else:
                print(f"Could not generate SOAP note for {filename}.")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    """
    Processes and returns SOAP notes for all the .txt files existing in "transcripts" folder
    """

    print("Starting SOAP note generation process...")
    process_all_transcripts()
    print("\nProcess completed.")