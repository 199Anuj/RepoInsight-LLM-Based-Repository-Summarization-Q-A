from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import prompts

load_dotenv()


python_separators = [
    "\nclass ",
    "\ndef ",
    "\n\n",
    "\n"
]

react_separators = [
    "\nfunction ",
    "\nconst ",
    "\nexport default",
    "\nreturn (",
    "\n\n",
    "\n"
]


ts_separators = [
    "\ninterface ",
    "\ntype ",
    "\nclass ",
    "\nfunction ",
    "\nexport ",
    "\n\n",
    "\n"
]

java_separators = [
    "\nclass ",
    "\npublic ",
    "\nprivate ",
    "\nprotected ",
    "\n\n",
    "\n"
]

json_separators = [
    "\n},",
    "\n],",
    "\n"
]

js_separators = [
    "\nfunction ",
    "\nconst ",
    "\nlet ",
    "\nclass ",
    "\nexport ",
    "\n\n",
    "\n"
]


model = ChatGroq( model="llama-3.3-70b-versatile")

def create_documents(augumented_file_data):
    documents = []

    for file in augumented_file_data:
        augmented_text = f"""
                         Content:
                         {file['content']}
                    """

        documents.append(
            Document(
                page_content=augmented_text,
                metadata={"source": file['file_path']}
            )
        )

    return documents


# def extract_augumented_files(file_tuples):
# 
#     augmented_docs = []
#     for file_path, file_content in file_tuples:
#           final_purpose_prompt = prompts.purpose_prompt.invoke({
#             "file_path": file_path,
#             "file_content": file_content
#         })
#         
#           response = model.invoke(final_purpose_prompt)
#           print(f"Response for {file_path}:\n{response.content}\n")
# 
#           output = response.content.strip()
#  
#           language = ""
#           purpose = ""
#   
#           for line in output.splitlines():
#                if line.lower().startswith("language:"):
#                    language = line.split(":", 1)[1].strip()
#                elif line.lower().startswith("purpose:"):
#                    purpose = line.split(":", 1)[1].strip()
#   
#           augmented_docs.append({
#               "file_path": file_path,
#               "language": language,
#               "purpose": purpose,
#               "content": file_content
#           })
# 
#     return augmented_docs


def detect_language(file_path):
    if file_path.endswith(".py"):
        return "python"
    elif file_path.endswith((".js", ".jsx")):
        return "javascript"
    elif file_path.endswith((".ts", ".tsx")):
        return "typescript"
    elif file_path.endswith(".java"):
        return "java"
    elif file_path.endswith(".json"):
        return "json"
    elif file_path.endswith(".json"):
        return "text"
    else:
        return "None"

def get_splitter(language):
    separator_map = {
        "python": python_separators,
        "javascript": js_separators,
        "typescript": ts_separators,
        "java": java_separators,
        "json": json_separators
    }

    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=separator_map.get(language, ["\n\n", "\n"])
    )