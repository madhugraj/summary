import streamlit as st
import google.generativeai as genai
import pandas as pd
import io
import os  # Import os module

# Retrieve the API key and password from secrets
api_key = st.secrets["api_key"]
passwords = st.secrets["passwords"]

# Configure the API key
genai.configure(api_key=api_key)

# Define the Excel file path
excel_file_path = "generated_summaries.xlsx"

# Initialize the Excel file if it doesn't exist
def initialize_excel_file():
    df = pd.DataFrame(columns=["Prompt", "Notes", "Generated Summary"])
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

if not os.path.exists(excel_file_path):
    st.write("Creating new Excel file...")
    initialize_excel_file()
    st.write("Excel file created.")

def save_to_excel(prompt, notes, summary):
    # Load the existing data, specifying the engine explicitly
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return

    # Create a DataFrame for the new row
    new_row = pd.DataFrame({"Prompt": [prompt], "Notes": [notes], "Generated Summary": [summary]})
    
    # Concatenate the new row with the existing data
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to the Excel file, specifying the engine explicitly
    try:
        with pd.ExcelWriter(excel_file_path, index=False, engine='openpyxl') as writer:
            df.to_excel(writer)
        st.write("Data saved to Excel file.")
    except Exception as e:
        st.error(f"Error saving to Excel file: {e}")

def generate_summary(notes_text, prompt_text):
    full_prompt = f"{prompt_text}\n\nNotes:\n{notes_text}"
    
    try:
        # Generate the content
        response = genai.GenerativeModel(model_name="models/gemini-1.5-flash-001").generate_content(
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

# Streamlit UI
st.title("Chart Notes & Summary Generator")
st.write("Generate summaries for medical records and chart notes from medical transcripts")

notes = st.text_area("Enter the notes/transcripts here:")
custom_prompt = st.text_area("Enter your custom prompt here:")

if st.button("Summary for Medical Record"):
    if notes:
        prompt = "Summarize the patient's medical history, including symptoms, imaging findings, and the proposed treatment plan"
        summary = generate_summary(notes, prompt)
        st.write(summary)
    else:
        st.warning("Please enter the notes.")

if st.button("Generate Chart Notes"):
    if notes:
        prompt = """You are a medical scribe. Create medical chart notes by following US healthcare styles using the following health care transcript.
Example: {Untagged Data
Chief Complaint
HAP
#Reason for Visit (Summary/Chief Complaint):  
 #45 y.o. female presents for an annual physical exam and follow up of hypertension and gastric reflux.  
  
#See care plans and review of systems below for further history details. See
#associated Encounter Report for vitals, allergies, medications, and orders
#that were reviewed and associated with this visit. Relevant past medical and
#surgical history, social history, family history were reviewed and updated as
#a part of today\'s visit. Recent relevant labs and past chart notes were
#reviewed.  
 #History, Assessment, and Plans By Problem:  
#Unaccompanied today.  
 #Preventative Care Summary  
 #Status Date Due Completion Date  
#Tetanus Overdue 01/17/1979 \\---  
 #Health maintenance reviewed and updated.  
Labs & screening:  
# * Reviewed and discussed the previous lab report.  
# * Ordered labs.  
 
#Social screening:  
#She was a smoker in the past  
  
 # * Ordered MAMMO 3D TOMOSYNTHESIS SCREENING BILAT W/CAD.  

 # Primary hypertension  
#She has hypertension and ..  

 #* Informed that the high blood pressure …
  
#\\-   lisinopril (PRINIVIL) 10 MG tablet; Take 1 tablet (10 mg total) by mouth daily.  

#History of sleeve gastrectomy  
#Patient had her gastric sleeve ….
 # * Informed that her weight gain is due to her eating habits.  

 # \\-   ZINC; Future  

  
#Gastroesophageal reflux disease without esophagitis .. 
  # * Prescribed pantoprazole (PROTONIX) 40 mg tablet; Take 1 tablet (40 mg total) by mouth daily.  
 
#\\-   HEMOGLOBIN A1C W/EAG; Future; Expected date: 08/20/2024  
   
#Review of System:  
#[Resp] : No snoring.  
#[GI] : (+) Vomiting.  
#[Neuro] : (+) Headache.  
  
#ROS was obtained as per above and HPI and all other systems reviewed otherwise negative.  
  
#Physical Examination:  
#Vitals:  
#08/20/24 1000 08/20/24 1001 08/20/24 1002 08/20/24 1003  
#BP: (!) 154/99 (!) 157/102 (!) 149/99 (!) 153/100  
#Pulse:  
#Resp:  

#Body mass index is 42.53 kg/m².  
  
#Constitutional: (+) Morbid obesity, well dressed, no acute distress. Vitals
#reviewed and stable.  
#HEENT: Atraumatic and normo-cephalic. No discharge, no eyelid swelling, sclera
#normal. Normal appearing outer ear, nose and lips. TMs normal. (+) Has some posterior pharynx erythema.  
#Neck: Normal appearing neck, no thyroid nodules or lymphadenopathy.  
 
#Current Outpatient Medications  
#Medication Sig  
#• cyanocobalamin 1000 MCG tablet Take 1 tablet (1,000 mcg total) by mouth daily.  
#No current facility-administered medications for this visit.  
  
#No follow-ups on file.  
  
#Patient expressed understanding of the care plan.  
#All questions and concerns addressed.  
#A copy of the patient\'s after visit summary was provided at discharge for review.  
  
#“I personally evaluated the patient and reviewed the history, as documented by scribe Aseem Hafiz...”  
 
#ROS
#PE
#Past medical history
#Past surgical history
#Past social history
#Disclaimer }
Make sure to follow US health care chart note writing patterns"""

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

# Add download button for Excel file with password prompt
st.write("---")
with st.expander("Download Excel file (Password Protected)"):
    password_input = st.text_input("Enter the password to download the file:", type="password")

    if st.button("Download Excel"):
        if password_input in passwords:
            # Use BytesIO to handle file download more smoothly
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df = pd.read_excel(excel_file_path, engine='openpyxl')
                df.to_excel(writer, index=False)
            buffer.seek(0)
            st.download_button(
                label="Click to Download",
                data=buffer,
                file_name="generated_summaries.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Access denied. Incorrect password.")
