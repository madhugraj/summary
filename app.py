import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="YOUR_API_KEY_HERE")

# Instantiate the model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-001")

# Streamlit app setup
st.title("Medical Summary Generator")

# Input fields
notes = st.text_area("Enter the notes here", height=200)
custom_prompt = st.text_area("Enter your custom prompt here (optional)", height=100)

# Buttons for different summaries
if st.button("Generate Medical Record Summary"):
    if notes:
        fixed_prompt_1 = "Summarize the patient\'s medical history, including her symptoms, imaging findings, and the proposed treatment plan for medical record purpose."
        full_prompt = f"{fixed_prompt_1}\n\nNotes:\n{notes}"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0,
                top_p=0.95,
                top_k=34
            )
        )
        st.write("Generated Summary for Medical Record:")
        st.write(response.text)
    else:
        st.error("Please enter the notes.")

if st.button("Generate Consultation Summary"):
    if notes:
        fixed_prompt_2 = "Summarize the patient\'s medical history, including her symptoms, imaging findings, and the proposed treatment plan for consultation purpose."
        full_prompt = f"{fixed_prompt_2}\n\nNotes:\n{notes}"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0,
                top_p=0.95,
                top_k=34
            )
        )
        st.write("Generated Summary for Consultation:")
        st.write(response.text)
    else:
        st.error("Please enter the notes.")

if st.button("Generate Custom Summary"):
    if notes and custom_prompt:
        full_prompt = f"{custom_prompt}\n\nNotes:\n{notes}"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0,
                top_p=0.95,
                top_k=34
            )
        )
        st.write("Generated Custom Summary:")
        st.write(response.text)
    else:
        st.error("Please enter both the notes and your custom prompt.")

