import get_repo_files
import chunking
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import FAISS
import prompts
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from collections import defaultdict


load_dotenv()


def get_vector_db(chunked_docs):
    embedder = NVIDIAEmbeddings()
    
    vector_db = FAISS.from_documents(
        documents = chunked_docs,
        embedding = embedder
    )
    return vector_db

def get_model():
    model = ChatGroq( model="llama-3.3-70b-versatile")
    return model

def extract_chunked_docs(repo_url):
    file_path = get_repo_files.clone_repo(repo_url)

    file_tuple = get_repo_files.get_all_files(file_path)
    
    # augumented_file_data = chunking.extract_augumented_files(res)
    
    # augumented_documents = chunking.create_documents(augumented_file_data)
    
    
    chunked_docs = []
    
    for file_path, file_content in file_tuple:
        language = chunking.detect_language(file_path)
    
        splitter = chunking.get_splitter(language)
        chunks = splitter.split_text(file_content)
    
        for idx, chunk in enumerate(chunks):
            chunked_docs.append(
                Document(
                    page_content=chunk ,
                    metadata={
                        "source": file_path,
                        "chunk_index": idx
                    }
                )
            )
    
    
    print("Total chunked docs:", len(chunked_docs))
    return chunked_docs


def answer_repo_query(user_question, chunked_docs):
    retriever = get_vector_db(chunked_docs).as_retriever(search_type="similarity", search_kwargs={"k": 4})


    retrieved_chunks = retriever.invoke(user_question)
    
    print("Retrieved Chunks:", len(retrieved_chunks))
    
    finalQ_Aprompt = prompts.Q_Aprompt.invoke({
        "context": retrieved_chunks,
        "question": user_question
    })
    
    
    
    response = get_model().invoke(finalQ_Aprompt)
    
    print("Final Q and A prompt Answer:", response.content)
    return response.content
    


def analyze_repo(repo_url, chunked_docs):
    retriever = get_vector_db(chunked_docs).as_retriever(search_type="similarity", search_kwargs={"k": 10})

        

    final_repo_explainer_prompt = prompts.repo_explainer_prompt.invoke({ 
                "context": chunked_docs
                })

    response_repo_explainer = get_model().invoke(final_repo_explainer_prompt)
    
    print("Repository Explanation:", response_repo_explainer.content)
    repo_explanation = response_repo_explainer.content
    return repo_explanation
    

def summarize_repo_in_text(chunked_docs):
     file_map = defaultdict(list)

     for doc in chunked_docs:
        file_path = doc.metadata["source"]
        file_map[file_path].append(doc.page_content)

     file_summaries = []

     for file_path, chunks in file_map.items():
         merged_code = merge_chunks_safely(chunks)
         prompt = prompts.build_file_summary_prompt(file_path, merged_code)
     
         response = get_model().invoke(prompt)
     
         file_summaries.append(
             Document(
                 page_content=response.content.strip(),
                 metadata={
                     "source": file_path,
                     "type": "file_summary"
                 }
             )
         )

     repo_explanation_prompt = prompts.build_repo_explanation_prompt(file_summaries)
     repo_explanation_response = get_model().invoke(repo_explanation_prompt)
     return repo_explanation_response.content




def merge_chunks_safely(chunks):
    merged = ""
    for chunk in chunks:
        merged += "\n" + chunk
    return merged