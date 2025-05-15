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