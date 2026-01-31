import utils
import streamlit as st

st.set_page_config(
    page_title="GitHub Repo Explainer",
    layout="centered"
)


st.title("📦 GitHub Repository Explainer")
st.write("Analyze any GitHub repository and ask questions using RAG")

st.subheader("🔍 Repository Analysis")

repo_url = st.text_input(
    label="Enter GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)

chunked_docs = utils.extract_chunked_docs(repo_url)

analyze_btn = st.button("Analyze Repository")

repo_explanation = ""



# for d in chunked_docs:
#     print(d.metadata)
#     print(d.page_content)
#     print("-----")



if analyze_btn:
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
    else:
        with st.spinner("Cloning repository and analyzing..."):
            try:
                repo_explanation = utils.summarize_repo_in_text(chunked_docs)
                st.success("Repository analysis completed!")
            except Exception as e:
                st.error(f"Error analyzing repository: {str(e)}")
    

st.text_area(
    label="Repository Explanation",
    value=repo_explanation,
    height=300,
    disabled=True
)


st.subheader("💬 Ask Questions About the Repository")

user_question = st.text_input(
    label="Ask a question",
    placeholder="Which APIs are used in this repository?"
)

qa_btn = st.button("Get Answer")

qa_answer = ""

if qa_btn:
    if not user_question:
        st.error("Please enter a question.")
    else:
        with st.spinner("Searching repository and generating answer..."):
            try:
                qa_answer = utils.answer_repo_query(user_question, chunked_docs)
                st.success("Answer generated!")
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")

st.text_area(
    label="Answer",
    value=qa_answer,
    height=200,
    disabled=True
)





    