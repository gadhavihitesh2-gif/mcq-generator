import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
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
st.title("🌍 AI MCQ Generator")
st.caption("Universal Model (No Install Mode)")

api_key = st.sidebar.text_input("Google API Key:", type="password")

with st.form("mcq"):
    subject = st.text_input("Subject:", placeholder="e.g. World War II")
    count = st.slider("Questions", 3, 10, 5)
    submitted = st.form_submit_button("Generate")

if submitted:
    if not api_key:
        st.error("❌ API Key Required")
    else:
        # --- FIXED URL: Using 'gemini-pro' (The Universal Model) ---
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        prompt_text = f"Create {count} multiple choice questions about {subject}. Format: Question, Options, Answer. Do NOT use markdown bolding."
        
        data = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }
        
        with st.spinner("Connecting to Google..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    result = response.json()
                    # Safe extraction
                    try:
                        text = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(text)
                    except:
                        st.error("AI replied, but the format was unexpected. Try again.")
                else:
                    st.error(f"Google Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
