import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# Configure the API key
genai.configure(api_key="AIzaSyAe8rheF4wv2ZHJB2YboUhyyVlM2y0vmlk")

# Instantiate the model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-001")

# Define the Excel file path
excel_file_path = r"generated_summaries.xlsx"

# Initialize the Excel file if it doesn't exist
if not os.path.exists(excel_file_path):
    df = pd.DataFrame(columns=["Prompt", "Notes", "Generated Summary"])
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

def save_to_excel(prompt, notes, summary):
    # Load the existing data, specifying the engine explicitly
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    
    # Create a DataFrame for the new row
    new_row = pd.DataFrame({"Prompt": [prompt], "Notes": [notes], "Generated Summary": [summary]})
    
    # Concatenate the new row with the existing data
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to the Excel file, specifying the engine explicitly
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

def generate_summary(notes_text, prompt_text):
    full_prompt = f"{prompt_text}\n\nNotes:\n{notes_text}"
    
    try:
        # Generate the content
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0,      # Ensures deterministic output
                top_p=0.85,         # Reducing top_p to limit sampling randomness
            )
        )
        generated_summary = response.text
        save_to_excel(prompt_text, notes_text, generated_summary)
        return generated_summary
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.title("Medical Summary Generator")
st.write("Generate summaries for medical records or consultations.")

notes = st.text_area("Enter the notes here:")
custom_prompt = st.text_area("Enter your custom prompt here:")
if st.button("Generate for Medical Record"):
    if notes:
        prompt = "Summarize the patient's medical history, including symptoms, imaging findings, and the proposed treatment plan for medical record purposes."
        summary = generate_summary(notes, prompt)
        st.write(summary)
    else:
        st.warning("Please enter the notes.")

if st.button("Generate for Consultation"):
    if notes:
        prompt = "Summarize the patient's medical history, including symptoms, imaging findings, and the proposed treatment plan for consultation purposes."
        summary = generate_summary(notes, prompt)
        st.write(summary)
    else:
        st.warning("Please enter the notes.")

if st.button("Generate Custom Summary"):
    if notes and custom_prompt:
        summary = generate_summary(notes, custom_prompt)
        st.write(summary)
    else:
        st.warning("Please enter both the notes and your custom prompt.")
