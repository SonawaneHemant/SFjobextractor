from langchain_ollama import OllamaLLM
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import database
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough  # pyright: ignore[reportMissingImports]

def run_ai_analysis():
    # 1️⃣ Load data from SQLite
    rows = database.fetch_all_jobs()

    if not rows:
        print("No data found in database.")
        return

    # 2️⃣ Convert DB rows to text documents
    documents = []
    for row in rows:
        text = f"""
        Job ID: {row[1]}
        Created Date: {row[2]}
        Job Type: {row[4]}
        Status: {row[6]}
        Errors: {row[9]}
        """
        documents.append(Document(page_content=text))

    # 3️⃣ Create Embeddings
    embedding = OllamaEmbeddings(model="qwen2.5:3b")

    # 4️⃣ Create Vector Store
    vector_store = Chroma.from_documents(
        documents,
        embedding=embedding,
        persist_directory="./chroma_db"
    )

    # 5️⃣ Create LLM
    llm = OllamaLLM(model="qwen2.5:3b")

    # # 6️⃣ Ask Question
    # query = "Summarize the job execution status and types."

    # docs = vector_store.similarity_search(query, k=5)

    # context = "\n".join([doc.page_content for doc in docs])

    # prompt = f"""
    # Based on the following Salesforce job data:
    # {context}

    # Provide a summary of:
    # - How many jobs are completed
    # - What job types exist
    # - Any errors detected
    # """

    # response = llm.invoke(prompt)

    # print("\nAI ANALYSIS RESULT:\n")
    # print(response)

    #-------------------------------------------------------------------------------------------------------------------------
    #Another way to get the responce 
    
    # retriever = vector_store.as_retriever()
    # # Modern Prompt Template
    # template = """
    # Based on the following Salesforce job data:

    # {context}

    # Provide:
    # - Total completed jobs
    # - Job types present
    # - Any errors detected
    # """

    # prompt_template  = PromptTemplate.from_template(template)
    
    # # LCEL Chain
    # chain = (
    #     {"context": retriever, "question": RunnablePassthrough()}
    #     | prompt_template
    #     | llm
    # )

    # response = chain.invoke("Summarize job execution status")

    # print("\nAI ANALYSIS RESULT:\n")
    # print(response)

    #------------------------------------------------------------------------------------------------------------------
    #One more Another way to get the responce properly
    contextOne = "\n".join([doc.page_content for doc in documents])

    # Modern Prompt Template
    template = """
    Based on the following Salesforce job data:

    {context}

    Provide:
    - Total completed jobs
    - Job types present
    - Any errors detected
    """

    prompt_templateOne  = PromptTemplate.from_template(template)
    promptOne = prompt_templateOne.format(context=contextOne)

    response = llm.invoke(promptOne)

    print("\nAI ANALYSIS RESULT NEXT:\n")
    print(response)



# from langchain.chains import RetrievalQA

