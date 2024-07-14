from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough , RunnableLambda
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_nomic import NomicEmbeddings

loader = CSVLoader(file_path='cardamom data.csv')
data = loader.load()

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size= 200,
    chunk_overlap=14
)
chunks=text_splitter.split_documents(data)

vector_db= Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(
        model='nomic-embed-text'
        ),
    collection_name='vectorDB'
    )

retriever=vector_db.as_retriever()
print(retriever.get_relevant_documents("last auctioneer?"))


# llm=ChatOllama(
#     base_url='http://localhost:11434',
#     model="mistral:7b-instruct",
#     temperature=0.5,
#     )

# QUERY_PROMPT=PromptTemplate(
#     input_variables=["question"],
#     template='''You are an AI language model assistant. Your task is to generate
#                 five different versions of the given user questions to retrieve relevant documents from a vector database. 
#                 by generatingg multiple perspectives on the user questions,
#                 your goal is to help the user overcome some of the limitations of the distance-based
#                 similarity search. Provide these alternative questions seperated by newlines.
#                 original question:{question}
#             '''
#     )

# retriever=MultiQueryRetriever.from_llm(
#     vector_db.as_retriever(),
#     llm,
#     prompt=QUERY_PROMPT
#     )

# template='''Answer the question based on the following context:
#             {context}
#             Question: {question}
#         '''
# prompt=ChatPromptTemplate.from_template(template)

# chain=({'context':retriever,
#         'question':RunnablePassthrough()}
#         |prompt
#         |llm
#         |StrOutputParser())
# chain.invoke(input('what is this about?'))


# userprompt=input("enter prompt : ")
# prompt = userprompt

# for chunks in llm.stream(prompt):
#     print(chunks, end="",flush=True) 