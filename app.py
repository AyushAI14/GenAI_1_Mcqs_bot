import streamlit as st
import pandas as pd
from src.Prompt.Templating import PromptTemplating
from src.Prompt.cleaning_to_csv import Cleaning_to_Csv
from src.utils.common import read_yaml_file
import json, re, os

st.set_page_config(
    page_title="AI MCQ Generator",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI MCQ Generator")
st.markdown("### Generate intelligent MCQs from any text using Gemini LLM")

# sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    param = read_yaml_file("param.yaml")

    subject = st.text_input("Subject", value=str(param.run.subject))
    tone = st.selectbox("Tone", ["formal", "friendly", "academic", "casual"], index=0)
    try:
        default_number = int(param.run.number)
    except Exception:
        default_number = 5
    number = st.slider("Number of MCQs", 1, 20, default_number)
    st.markdown("---")

# input area
st.subheader("📘 Input Text")
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
text_input = st.text_area("Or paste your text here", height=250)

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
elif text_input.strip():
    text = text_input
else:
    text = None

if st.button("🚀 Generate MCQs"):
    if not text:
        st.warning("Please provide text input first.")
        st.stop()

    with st.spinner("Generating MCQs... Please wait ⏳"):
        try:
            # Step 1: invoke prompt templating manually with updated params
            from src.Prompt.Templating import mcq_maker_prompt, response_json
            from langchain.prompts import PromptTemplate
            from langchain_core.runnables import RunnableSequence, RunnableLambda
            from src.llm.LLM_Initalize import InitializeLLM

            llm_instance = InitializeLLM()
            mcq_maker_prompt_template = PromptTemplate(
                input_variables=["text", "number", "subject", "tone", "response_json"],
                template=mcq_maker_prompt
            )

            mcq_chain = RunnableSequence(
                first=mcq_maker_prompt_template,
                last=RunnableLambda(llm_instance.InvokeLLM)
            )

            result = mcq_chain.invoke({
                "text": text,
                "number": number,       # use sidebar value
                "subject": subject,     # use sidebar value
                "tone": tone,           # use sidebar value
                "response_json": json.dumps(response_json, indent=2)
            })

            raw_output = result.content if hasattr(result, "content") else result

            # Step 2: Clean and convert to CSV
            cleaned_text = re.sub(r"^```(?:json)?", "", raw_output)
            cleaned_text = re.sub(r"```$", "", cleaned_text)
            cleaned_text = cleaned_text.strip()
            mcq_data = json.loads(cleaned_text)

            df = pd.DataFrame(mcq_data).T

            os.makedirs("data", exist_ok=True)
            csv_path = "data/mcq.csv"
            df.to_csv(csv_path, index=False)

            st.success("✅ MCQs generated successfully!")
            st.subheader("🧩 Generated MCQs")
            st.dataframe(df, width='stretch')

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download MCQs as CSV",
                data=csv,
                file_name="mcq.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray">
    Built by Ayush using Streamlit & LangChain | Powered by Gemini 
    </div>
    """,
    unsafe_allow_html=True
)
