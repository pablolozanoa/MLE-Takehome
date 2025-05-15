import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
from .prompts import SOAP_NOTE_PROMPT_TEMPLATE

load_dotenv()

try:
    client = OpenAI()
    if not client.api_key:
        print("Error: OPENAI_API_KEY not found or client not properly configured. Please check .env file.")
        client = None
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

def generate_soap_note_from_transcript(transcript_text: str) -> Optional[str]:
    if not client: # Check if client was initialized successfully
        print("OpenAI client is not initialized. Cannot generate SOAP note.")
        return None

    if not transcript_text.strip():
        print("Transcript text is empty. Cannot generate SOAP note.")
        return None

    prompt = SOAP_NOTE_PROMPT_TEMPLATE.format(transcript_text=transcript_text)

    print("Sending prompt to OpenAI LLM...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or any other OpenAI language model (ej: gpt-3.5-turbo, gpt-4o-mini, etc.)
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1, 
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_soap_note = response.choices[0].message.content.strip()
        print("SOAP note generated successfully.")
        return generated_soap_note
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

if __name__ == '__main__':
    current_script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_script_dir, ".."))
    example_transcript_path = os.path.join(project_root, "transcripts", "encounter_1.txt")

    if not os.path.exists(example_transcript_path):
        print(f"Example transcript file not found at: {example_transcript_path}")
    else:
        try:
            with open(example_transcript_path, 'r', encoding='utf-8') as f:
                sample_transcript = f.read()
            print(f"\n--- Testing SOAP note generation for: {example_transcript_path} ---")
            # This test uses the globally defined SOAP_NOTE_PROMPT_TEMPLATE which is now V3
            soap_note = generate_soap_note_from_transcript(sample_transcript)
            if soap_note:
                print("\n--- Generated SOAP Note (Test) ---")
                print(soap_note)
                if client and client.api_key:
                    # Ensure correct import path if pdf_generator is in the same 'src' package
                    from src.pdf_generator import create_soap_pdf_bytes 
                    pdf_bytes = create_soap_pdf_bytes(soap_note)
                    test_pdf_filename = "test_output_v3_from_process_transcript.pdf" # New name for test
                    with open(test_pdf_filename, "wb") as f:
                        f.write(pdf_bytes.getvalue())
                    print(f"Test PDF also generated: {test_pdf_filename} (in src directory if run from src, or project root if run as module)")
                else:
                    print("Skipping PDF generation test as OpenAI client is not properly configured.")
            else:
                print("Failed to generate SOAP note.")
        except ImportError as ie:
            print(f"Import error during test: {ie}")
        except Exception as e:
            print(f"Error during test: {e}")