import os
from openai import OpenAI # Importar OpenAI directamente
from dotenv import load_dotenv
from typing import Optional
from .prompts import SOAP_NOTE_PROMPT_TEMPLATE  # Import the prompt template

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# The API key will be automatically picked up from the OPENAI_API_KEY environment variable
# if it's set. The client handles this.
try:
    client = OpenAI() # Nueva forma de inicializar
    # openai.api_key = os.getenv("OPENAI_API_KEY") # Ya no se usa así directamente
    if not os.getenv("OPENAI_API_KEY"): # Comprobación manual si es necesario
        print("Error: OPENAI_API_KEY not found in environment variables.")
        # Podrías lanzar un error aquí o manejarlo para que client sea None
        # client = None # Descomentar si quieres que las funciones fallen si la key no está
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None


def generate_soap_note_from_transcript(transcript_text: str) -> Optional[str]:
    """
    Generates a SOAP note from a medical visit transcript using OpenAI's LLM.

    Args:
        transcript_text (str): Raw text from a medical encounter transcript.

    Returns:
        Optional[str]: The generated SOAP note, or None if an error occurs.
    """
    if not client: # Comprueba si el cliente se inicializó correctamente
        print("OpenAI client not initialized. Cannot generate SOAP note.")
        return None
    
    # Comprobación adicional de la API key si la inicialización no lanza error pero la key falta
    if not client.api_key: 
        print("Error: OPENAI_API_KEY not found or client not properly configured.")
        return None

    if not transcript_text.strip():
        print("Transcript text is empty. Cannot generate SOAP note.")
        return None

    # Format the full prompt using the provided transcript
    prompt = SOAP_NOTE_PROMPT_TEMPLATE.format(transcript_text=transcript_text)

    # Optional: enable to debug prompt content
    DEBUG = False
    if DEBUG:
        print("--- Prompt Sent to LLM ---")
        print(prompt)
        print("--------------------------")

    print("Sending prompt to OpenAI LLM...")

    try:
        # Nueva forma de llamar a la API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        generated_soap_note = response.choices[0].message.content
        print("SOAP note generated successfully.")
        return generated_soap_note

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

if __name__ == '__main__':
    """
    Standalone test: Run this script directly to test SOAP note generation
    for a single example transcript file.
    """
    # Build path to example transcript file
    # Esta forma de construir la ruta es robusta
    current_script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_script_dir, ".."))
    example_transcript_path = os.path.join(project_root, "transcripts", "encounter_1.txt")


    if not os.path.exists(example_transcript_path):
        print(f"Example transcript file not found at: {example_transcript_path}")
        print("Please ensure the file exists and the path is correct for testing.")
    else:
        try:
            with open(example_transcript_path, 'r', encoding='utf-8') as f:
                sample_transcript = f.read()

            print(f"\n--- Testing SOAP note generation for: {example_transcript_path} ---")
            soap_note = generate_soap_note_from_transcript(sample_transcript)

            if soap_note:
                print("\n--- Generated SOAP Note (Test) ---")
                print(soap_note)
                print("------------------------------------")
            else:
                print("Failed to generate SOAP note.")
        except Exception as e:
            print(f"Error during test: {e}")