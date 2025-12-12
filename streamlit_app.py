import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="AI MCQ Master", page_icon="📝", layout="centered")

# --- 1. AUTHENTICATION (The Lock) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    password = st.sidebar.text_input("Enter Password to Access:", type="password")
    if password == "admin123":  # <--- PASSWORD IS: admin123
        st.session_state["authenticated"] = True
        st.rerun()

if not st.session_state["authenticated"]:
    st.title("🔒 Login Required")
    check_password()
    st.stop()  # Stop here if not logged in

# --- 2. THE APP (Once Logged In) ---
st.title("🌍 World Internet MCQ Generator")
st.markdown("Generates questions from the world's knowledge base instantly.")

# API Key Input (Paste your AIza... key here when running)
api_key = st.sidebar.text_input("Google API Key:", type="password", help="Paste your Gemini API Key here")

# User Inputs
with st.form("mcq_form"):
    subject = st.text_input("Enter Subject / Topic:", placeholder="e.g. Current Affairs 2024, Python Lists, Anatomy of Heart")
    
    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard", "Expert"])
    with col2:
        count = st.slider("Number of Questions:", 5, 20, 10)
        
    submitted = st.form_submit_button("Generate Questions 🚀")

# --- 3. THE BRAIN (Gemini Logic) ---
if submitted:
    if not api_key:
        st.error("❌ Please paste your Google API Key in the sidebar.")
    elif not subject:
        st.error("❌ Please enter a subject.")
    else:
        try:
            # Connect to Google
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash') # Fast & Smart

            # The Prompt
            prompt = f"""
            Act as a strict Examiner. Create {count} Multiple Choice Questions (MCQs) about: '{subject}'.
            Difficulty Level: {difficulty}.
            
            SOURCE: Use your internal training data covering the world internet knowledge.

            OUTPUT FORMAT:
            ### Question [Number]
            [Question Text]
            
            A) [Option]
            B) [Option]
            C) [Option]
            D) [Option]
            
            **Correct Answer:** [Letter]
            *Explanation: [Short reason why]*
            
            ---
            """
            
            with st.spinner("🔍 Scanning knowledge base & generating..."):
                response = model.generate_content(prompt)
                
            # Display Results
            st.success("✅ Questions Generated Successfully!")
            st.markdown(response.text)
            
            # Download Button
            st.download_button(
                label="📥 Download Questions (Text File)",
                data=response.text,
                file_name=f"{subject}_MCQ.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")
