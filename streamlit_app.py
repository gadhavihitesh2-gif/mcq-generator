import streamlit as st
import subprocess
import sys

# --- MAGIC FIX: AUTO-INSTALL GOOGLE AI ---
try:
    import google.generativeai as genai
except ImportError:
    # If the tool is missing, this forces the server to install it right now
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="AI MCQ Master", page_icon="📝")

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    password = st.sidebar.text_input("Enter Password:", type="password")
    if password == "admin123":
        st.session_state["authenticated"] = True
        st.rerun()

if not st.session_state["authenticated"]:
    st.title("🔒 Login Required")
    check_password()
    st.stop()

# --- MAIN APP ---
st.title("🌍 World Internet MCQ Generator")
st.caption("Auto-installed & Ready to go")

api_key = st.sidebar.text_input("Google API Key:", type="password")

with st.form("mcq"):
    subject = st.text_input("Subject:", placeholder="e.g. Black Holes")
    count = st.slider("Questions", 3, 10, 5)
    submitted = st.form_submit_button("Generate")

if submitted:
    if not api_key:
        st.error("❌ Need API Key")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Create {count} MCQs about {subject} with answers."
            
            with st.spinner("Generating..."):
                response = model.generate_content(prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
