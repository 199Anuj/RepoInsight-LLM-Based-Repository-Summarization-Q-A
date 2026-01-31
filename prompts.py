from langchain_core.prompts import PromptTemplate

purpose_prompt = PromptTemplate(input_variables=["file_path", "file_content"],
 template="""
              You are analyzing a source code file.
              
              Task:
              Identify ONLY the high-level purpose of this file.
              Do NOT explain how the code works.
              Do NOT mention implementation details.
              Be concise (1-2 sentences).
              
              File path:
              {file_path}
              
              File content:
              {file_content}
              
              Respond in this format only:
              language: <programming language>
              purpose: <high-level purpose of the file>
              """
              )


Q_Aprompt = PromptTemplate(
    template="""
You are an expert code assistant.

Answer the user's question using ONLY the provided context.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)


repo_explainer_prompt = PromptTemplate(
    input_variables=["context"],
    template="""
You are a senior software engineer reviewing a GitHub repository.

Your task is to explain what this repository does at a HIGH LEVEL.

======================
STRICT RULES (MANDATORY)
======================
- Use ONLY the information provided in the context below.
- Do NOT guess, infer, or assume anything that is not explicitly present.
- Do NOT hallucinate APIs, frameworks, features, or workflows.
- If any information is missing or unclear, explicitly state:
  "This information is not available in the repository."
- Do NOT explain code line-by-line or low-level implementation details.
- Do NOT include opinions or recommendations.

======================
CONTEXT (retrieved repository files and chunks)
======================
{context}

======================
OUTPUT FORMAT (FOLLOW EXACTLY)
======================

Repository Overview:
<2–4 sentence high-level explanation of what the repository does>

Key Capabilities:
- <capability 1>
- <capability 2>
- <capability 3>

Main Components:
- <file or module name>: <its responsibility>
- <file or module name>: <its responsibility>

Data Flow (if determinable from the code):
- <step 1>
- <step 2>
- <step 3>

Limitations / Missing Information:
- <clearly state any missing or unclear information>

IMPORTANT:
If something cannot be determined from the context, say:
"This information is not available in the repository."
"""
)


def build_file_summary_prompt(file_path, code_text):
    return f"""
You are a senior software architect.

Summarize the following source code file in **1–2 concise technical lines**.

Focus on:
- Primary responsibility of the file
- Key logic or design role
- Important integrations or dependencies

Do NOT:
- Explain line-by-line
- Mention obvious syntax
- Repeat code

File path:
{file_path}

Source code:
{code_text}
"""


def build_repo_explanation_prompt(file_summary):
    return f"""
You are a senior software architect.

Given the following **file-level technical summaries**, produce a **concise but complete repository-level technical overview** covering:

- Overall purpose of the system
- High-level architecture and design
- Major components and responsibilities
- Key technologies and frameworks
- How components interact

File summaries:
{file_summary}
"""