import streamlit as st
from google import genai

# ---------------------------------------------------------
# 1. API CONFIGURATION
# ---------------------------------------------------------
# Your API Key is placed here directly so users don't have to enter it
API_KEY = "WRTE THE API KEY HERE"

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="AI Resume Builder", page_icon="📄")
st.title("🎓 AI Resume & Portfolio Builder")
st.write("Fill in your details and generate a professional resume using AI.")

# -----------------------------
# User Input Fields
# -----------------------------
name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
education = st.text_area("Education / Degrees", placeholder="e.g. B.Tech in Computer Science")
skills = st.text_area("Skills (comma separated)", placeholder="e.g. Python, Java, SQL")
experience = st.text_area("Work Experience / Internships", placeholder="e.g. Intern at Edunet")
projects = st.text_area("Projects / Achievements", placeholder="e.g. Smart India Hackathon")

# -----------------------------
# Configure Google GenAI Client
# -----------------------------
client = genai.Client(api_key=API_KEY)

# -----------------------------
# Generate Resume Button
# -----------------------------
if st.button("Generate Resume", type="primary"):
    if not name.strip():
        st.warning("⚠️ Please enter your name.")
    else:
        # Professional prompt for better AI results
        prompt = f"""
        Act as a professional career coach. Create a high-quality resume in Markdown format.
        Name: {name}
        Education: {education}
        Skills: {skills}
        Experience: {experience}
        Projects: {projects}
        
        Formatting: Use bold headers and clean bullet points.
        """

        try:
            with st.spinner("AI is crafting your resume..."):
                # Note: 'gemini-1.5-flash' is the stable identifier in the current SDK.
                # If you specifically want Pro, use 'gemini-1.5-pro'.
                # The 404 error usually occurs because of an incorrect model string or regional access.
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                if response and response.text:
                    st.divider()
                    st.subheader("📝 Generated Resume:")
                    # Use markdown to render bold text and bullet points correctly
                    st.markdown(response.text)
                    
                    # Add a download button
                    st.download_button(
                        label="Download Resume as Text",
                        data=response.text,
                        file_name=f"{name.replace(' ', '_')}_Resume.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("The AI returned an empty response. Please try again.")

        except Exception as e:
            # Enhanced error handling for model availability
            error_str = str(e)
            if "404" in error_str:
                st.error("❌ Model Error: The requested model was not found. This can happen if the model ID is typed incorrectly or is not available in your API region.")
                st.info("Try switching the model name to 'gemini-1.5-flash' in your code, as it has the highest availability.")
            elif "401" in error_str or "API_KEY_INVALID" in error_str:
                st.error("❌ API Key Error: Please check if your API key is valid and has not expired.")
            else:
                st.error(f"❌ Error: {e}")

st.divider()
st.caption("Powered by Google Gemini 1.5 Flash")