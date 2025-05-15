import streamlit as st
import os
from src.process_transcript import generate_soap_note_from_transcript
from src.pdf_generator import create_soap_pdf_bytes

# --- Page Configuration ---
st.set_page_config(
    page_title="SOAP Note Generator",
    page_icon="🩺",
    layout="wide", # Use "centered" or "wide"
    initial_sidebar_state="expanded" # Or "collapsed"
)

# --- Sidebar ---
with st.sidebar:
    st.title("📤 Upload Transcript")
    uploaded_file = st.file_uploader(
        "Choose a .txt transcript file",
        type=["txt"],
        help="Upload the medical encounter transcript you want to process."
    )
    
    # Disable button if no file is uploaded
    process_button_disabled = uploaded_file is None
    process_button = st.button(
        "Generate SOAP Note ✨",
        use_container_width=True,
        disabled=process_button_disabled,
        help="Click to process the uploaded transcript." if not process_button_disabled else "Upload a file to enable."
    )

    st.markdown("---") # Divider
    st.markdown(
        "**About:** This application uses an AI model (OpenAI GPT) "
        "to automatically generate a structured SOAP note from a medical transcript."
    )
    st.markdown(
        "**Instructions:**\n"
        "1. Upload your transcript file (.txt format).\n"
        "2. Click the 'Generate SOAP Note' button.\n"
        "3. Review the generated note on the right.\n"
        "4. Download the note as a PDF if satisfied."
    )
    st.markdown("---")


# --- Main Page Layout ---
st.title("SOAP Note Generator 🩺")
st.markdown(
    "Welcome! Upload a medical transcript text file using the sidebar, "
    "and this tool will generate a structured SOAP note for you. "
    "The generated note can then be downloaded as a PDF."
)
st.markdown("---") # Visual separator

# Initialize session state variables if they don't exist
if 'soap_note_generated' not in st.session_state:
    st.session_state.soap_note_generated = None # Stores the generated SOAP note text
if 'transcript_filename_for_pdf' not in st.session_state:
    st.session_state.transcript_filename_for_pdf = "soap_note" # Default PDF filename part

# --- Processing Logic ---
if process_button and uploaded_file is not None:
    # Store the original filename (without extension) for the PDF download
    st.session_state.transcript_filename_for_pdf = os.path.splitext(uploaded_file.name)[0]
    
    # Read the content of the uploaded file
    try:
        transcript_text = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {uploaded_file.name}. Ensure it's a valid UTF-8 text file. Details: {str(e)}")
        st.stop() # Stop further execution for this run

    if not transcript_text.strip():
        st.error("The uploaded transcript file is empty. Please upload a valid file.")
    else:
        # Show a spinner during processing
        with st.spinner(f"🧠 Processing '{uploaded_file.name}'... This might take a few moments."):
            try:
                # Call the function to generate the SOAP note
                st.session_state.soap_note_generated = generate_soap_note_from_transcript(transcript_text)
                
                if st.session_state.soap_note_generated:
                    st.success(f"SOAP Note generated successfully for '{uploaded_file.name}'!")
                else:
                    # This case handles if generate_soap_note_from_transcript returns None (e.g., API key error)
                    st.error("Failed to generate SOAP note. The AI model might have encountered an issue. "
                             "Please check the console output if you are running this application locally for more details.")
            except Exception as e:
                st.error(f"An unexpected error occurred during AI processing: {str(e)}")
                st.session_state.soap_note_generated = None # Reset on error

# --- Display Area for SOAP Note and Download Button ---
if st.session_state.soap_note_generated:
    st.markdown("---")
    st.subheader("Generated SOAP Note:")
    
    # Using a text area allows users to easily copy the text
    st.text_area(
        "SOAP Note Content:",
        value=st.session_state.soap_note_generated,
        height=600, # Adjust height as needed
        help="Review the generated SOAP note below. You can copy the text from here."
    )

    st.markdown("<br>", unsafe_allow_html=True) # Add some vertical space

    # PDF Download Button
    try:
        pdf_bytes = create_soap_pdf_bytes(st.session_state.soap_note_generated)
        st.download_button(
            label="📥 Download SOAP Note as PDF",
            data=pdf_bytes,
            file_name=f"{st.session_state.transcript_filename_for_pdf}_soap_note.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download the generated SOAP note in PDF format."
        )
    except Exception as e:
        st.error(f"Sorry, an error occurred while preparing the PDF for download: {str(e)}")

    st.markdown("---")
    st.info(
        "**Disclaimer:** This document is AI-generated. "
        "Always review and verify its accuracy before use in any clinical or critical setting."
    )
else:
    # Placeholder if no note has been generated yet
    st.info("Upload a transcript and click 'Generate SOAP Note' to view the results here.")

# --- Footer ---
st.markdown("---")
