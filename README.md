# Cofactor AI - ML Engineer Take-Home: Section 1 - Idealized SOAP Note Generator

## 1. Overview

This section of the project implements a pipeline to transform unstructured medical encounter transcripts into well-structured SOAP (Subjective, Objective, Assessment, Plan) notes. The core of this pipeline leverages a Large Language Model (LLM) from OpenAI to extract, summarize, and organize relevant clinical information into the standard SOAP format.

The application offers two primary modes of operation:
1.  An interactive **Streamlit web application** for processing individual transcript files (.txt) and downloading the generated SOAP note as a PDF.
2.  A **batch processing script** (`main.py`) that can process multiple transcript files from a designated directory, saving the output as both text and PDF files.

The primary goal is to produce clinically relevant, clearly formatted SOAP notes that can serve as a foundation for medical record keeping, demonstrating an understanding of LLM application, prompt engineering, and basic MLOps principles like reproducibility and documentation.

As a reference for the SOAP note structure, the [Wikipedia article on SOAP notes](https://en.wikipedia.org/wiki/SOAP_note) was consulted, defining the sections as:
-   **S: Subjective** – What the patient says (symptoms, sensations, history, pain scale, etc.)
-   **O: Objective** – Healthcare Provider observations (vital signs, physical findings, tests, etc.)
-   **A: Assessment** – Diagnosis or clinical impression of the professional.
-   **P: Plan** – Next steps: treatments, testing, referrals, education, follow-up.

An example SOAP note was also provided in `./example_notes/Medical Visit SOAP Note.pdf` (though its content is therapy-focused, the S-O-A-P structure is relevant).

## 2. Features

*   **Transcript Upload:** Supports uploading `.txt` format medical transcripts via the Streamlit UI.
*   **AI-Powered SOAP Note Generation:** Utilizes OpenAI's GPT models (configurable, currently defaults to `gpt-4o`) for intelligent information extraction and structuring.
*   **Structured Output:** Generates notes with clear "Subjective," "Objective," "Assessment," and "Plan" sections.
*   **Interactive Display:** The Streamlit app displays the generated SOAP note for review.
*   **PDF Download:** Allows users to download the generated SOAP note in PDF format.
*   **Batch Processing:** The `main.py` script can process all transcripts in a specified directory, producing both `.txt` and `.pdf` outputs.
*   **Customizable Prompts:** Includes two distinct prompt templates (`prompts.py` for a detailed version, `reduced_prompts.py` for a token-optimized version) allowing for flexibility in balancing output detail versus processing cost.

## 3. Project Structure

```plaintext
cofactor_ai_takehome/
├── transcripts/                    # Input medical transcripts (.txt files)
├── output_soap_notes_txt/          # Output directory for .txt SOAP notes (batch mode)
├── output_soap_notes_pdf/          # Output directory for .pdf SOAP notes (batch mode)
├── src/
│ ├── init.py
│ ├── streamlit_app.py              # Main Streamlit application file
│ ├── process_transcript.py         # Core LLM interaction and SOAP note generation logic
│ ├── prompts.py                    # Detailed prompt template for the LLM
│ ├── reduced_prompts.py            # Token-optimized prompt template
│ ├── pdf_generator.py              # Utility to convert text SOAP note to PDF
│ └── main.py                       # Script for batch processing transcripts
├── docs/
│ └── images/
│ └── section1_architecture.png     # Diagram image
├── .env                            # For OpenAI API Key (MUST be filled by user)
├── .gitignore
├── README.md
└── requirements.txt                # Python dependencies
```

## 4. Setup Instructions

### Prerequisites
*   Python 3.8 or higher.
*   Conda (recommended for environment management) or `venv`.
*   An active OpenAI API account with a configured payment method and API key.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your_repository_url>
    cd cofactor_ai_takehome
    ```

2.  **Create and Activate Python Environment:**
    *   Using Conda:
        ```bash
        conda create --name cofactor_env python=3.9
        conda activate cofactor_env
        ```
    *   Using `venv`:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure `requirements.txt` includes `openai`, `python-dotenv`, `streamlit`, and your PDF generation library e.g., `reportlab` or `fpdf2`).

4.  **Set Up Environment Variables:**
    *   Create a file named `.env` in the root directory of the project (`cofactor_ai_takehome/.env`).
    *   Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY="your_sk-xxxxxxxxxxxxxxxxxxxx_key_here"
        ```
    *   **Important:** This file is listed in `.gitignore` and should NOT be committed to version control.

## 5. How to Run

### A. Streamlit Web Application (Interactive Mode)

This mode allows you to process one transcript at a time through a user-friendly web interface.

1.  Ensure your Python environment is activated and you are in the project's root directory.
2.  Run the Streamlit application:
    ```bash
    streamlit run src/streamlit_app.py
    ```
3.  Open the URL provided by Streamlit (usually `http://localhost:8501`) in your web browser.
4.  Use the sidebar to upload a `.txt` transcript file.
5.  Click the "Generate SOAP Note ✨" button.
6.  Review the generated note in the main panel.
7.  Click the "📥 Download SOAP Note as PDF" button if satisfied.

### B. Batch Processing Script (Console Mode)

This mode processes all `.txt` files found in the `transcripts/` directory and saves the outputs.

1.  Ensure your Python environment is activated and you are in the project's root directory.
2.  Place all transcript `.txt` files you want to process into the `transcripts/` folder.
3.  Run the `main.py` script as a module:
    ```bash
    python -m src.main
    ```
4.  The generated text SOAP notes will be saved in the `output_soap_notes_txt/` directory.
5.  The generated PDF SOAP notes will be saved in the `output_soap_notes_pdf/` directory.
    Console logs will indicate the progress and any errors.

## 6. System Architecture & Design Decisions

The pipeline takes a raw transcript and, through a series of steps orchestrated by either the Streamlit UI or the batch script, produces a structured SOAP note.

### Architecture Diagram

The following diagram illustrates the flow for the Streamlit application mode:

![Section 1 Architecture Diagram](images/section1_architecture.png) 

**Flow Description (Streamlit UI):**
1.  The **User** uploads a `.txt` transcript file via the **Streamlit UI** (`streamlit_app.py`).
2.  Upon clicking "Generate", the UI triggers the processing.
3.  The transcript text is passed to the `generate_soap_note_from_transcript` function in `src.process_transcript.py`.
4.  This function utilizes a prompt template (from `src.prompts.py` or `src.reduced_prompts.py`) and the transcript text to construct a detailed prompt.
5.  An API call is made to the **OpenAI LLM** (e.g., GPT-4o).
6.  The LLM processes the prompt and returns the generated SOAP note as text.
7.  This text is sent back to the Streamlit UI, where it is displayed to the User.
8.  If the User clicks "Download PDF", the generated SOAP text is passed to `src.pdf_generator.create_soap_pdf` (or `create_soap_pdf_bytes`).
9.  This function generates a PDF file (as bytes).
10. The Streamlit UI offers this PDF file for download to the User.

The batch processing script (`src.main.py`) follows a similar internal logic (steps 3-6 and 8-9) for each transcript file it finds, saving the outputs directly to disk.

### Key Design Decisions

*   **LLM Choice:**
    *   The system currently defaults to OpenAI's `gpt-4o` model (configured in `src/process_transcript.py`) due to its strong capabilities in understanding nuanced medical language and adhering to complex instructions for structured output.
    *   Alternative models like `gpt-3.5-turbo` or `gpt-4o-mini` can be used by modifying the `model` parameter in `src/process_transcript.py` to balance performance with cost.
*   **Prompt Engineering:**
    *   Two primary prompt templates are provided:
        *   **Detailed Prompt (`src/prompts.py`):** This is the default and is based on the `BALANCED_SOAP_NOTE_PROMPT_TEMPLATE_V2` discussed. It employs techniques such as explicit role-playing, a guided internal analysis step (Chain-of-Thought), and highly specific instructions for each section and formatting requirement, aiming for the highest quality output. It was developed referencing best practices from the [Prompting Guide](https://www.promptingguide.ai/).
        *   **Reduced Prompt (`src/reduced_prompts.py`):** This version is optimized for lower input token usage, offering a more concise set of instructions. It serves as an alternative where cost or token limits are a primary concern.
    *   The prompts are designed to instruct the LLM to extract information only if explicitly stated, to handle missing information gracefully, and to adhere to a precise output format (plain text for SOAP sections, specific handling for metadata and signature).
*   **Modularity:** The codebase is organized into modules with distinct responsibilities:
    *   `streamlit_app.py`: Handles user interface and interaction.
    *   `process_transcript.py`: Contains the core logic for LLM interaction and SOAP note generation.
    *   `prompts.py` / `reduced_prompts.py`: Store the LLM prompt templates.
    *   `pdf_generator.py`: Manages the conversion of text SOAP notes to PDF.
    *   `main.py`: Orchestrates batch processing.
*   **User Interface (Streamlit):** Streamlit was chosen for its ability to rapidly develop interactive web applications for Python-based data and ML projects.
*   **Output Formats:** Providing both `.txt` (for easy copying/editing) and `.pdf` (for standardized document sharing) offers flexibility.
*   **Error Handling:** Basic error handling is implemented for file operations, API calls, and PDF generation to provide feedback to the user or console.

### Parts of the System Better Done Without LLMs

While the LLM is central to understanding and structuring the transcript, several parts of the system are, and should be, handled by conventional code:

*   **File I/O:** Reading transcript files and writing output SOAP notes (text and PDF).
*   **User Interface:** Rendering the web application, handling file uploads, button clicks (all managed by Streamlit).
*   **PDF Generation:** Converting structured text to a formatted PDF is best done using dedicated PDF libraries (e.g., ReportLab, FPDF2), which offer precise control over layout and styling. The LLM provides the content, the library formats it.
*   **Directory Traversal and File Management:** Iterating through files in a directory for batch processing.
*   **Application Flow Control:** The overall logic of the Streamlit app and the batch script.

The LLM is used for its unique natural language understanding and generation capabilities, specifically for the complex task of transforming conversational text into a structured clinical note.

## 7. Limitations

*   **Dependence on OpenAI API:** The system relies on the availability, performance, and pricing of the OpenAI API. API outages, rate limits, or changes in API policy could affect functionality.
*   **Quality of LLM Output:**
    *   The accuracy and completeness of the generated SOAP note are highly dependent on the clarity and quality of the input transcript. Ambiguous or poorly recorded transcripts may lead to suboptimal results.
    *   While prompt engineering aims to minimize this, LLMs can occasionally "hallucinate" or misinterpret information. The generated notes always require human review and verification in a clinical context.
*   **Context Window:** While `gpt-4o` has a large context window (128k tokens), extremely long transcripts could still potentially exceed this limit, though this is less likely for typical medical encounters.
*   **Cost:** Using powerful models like `gpt-4o` incurs costs per API call. While optimized, frequent use or processing of many large transcripts can lead to notable expenses.
*   **PDF Formatting:** The current PDF generation might have basic formatting. Advanced styling or complex layouts would require more intricate PDF library usage.
*   **Handling of Highly Specialized Medical Jargon/Abbreviations:** While GPT models are trained on vast data, extremely niche or new abbreviations might not always be interpreted correctly without further fine-tuning or more specific prompt instructions.

## 8. Future Iterations & Improvements

*   **Model Selection in UI:** Allow users to choose the OpenAI model (e.g., GPT-4o, GPT-3.5-Turbo, GPT-4o-mini) directly from the Streamlit interface to balance cost and quality.
*   **In-UI Editing:** Enable users to edit the generated SOAP note text within the Streamlit app before downloading the PDF.
*   **Enhanced Error Handling:** Implement more granular error catching and provide more user-friendly error messages.
*   **Batch Upload/Processing in UI:** Allow users to upload multiple files or a zip archive for batch processing directly through the Streamlit interface.
*   **Advanced PDF Customization:** Offer options for customizing PDF templates, fonts, or including logos.
*   **Evaluation Metrics:** For more rigorous development, implement metrics to evaluate the quality of generated SOAP notes against a gold standard (if available).
*   **Alternative LLM Backends:** Explore integration with other LLM providers or open-source models to offer more flexibility and potentially reduce costs (e.g., using Ollama for local models).
*   **Security & Compliance (for production):** If used in a real clinical setting, rigorous security audits and compliance with healthcare data regulations (e.g., HIPAA) would be paramount.

---
**Disclaimer:** This tool is AI-generated and intended for demonstration or assistive purposes. All outputs should be carefully reviewed and verified by a qualified healthcare professional before being used in any clinical decision-making or official medical records.