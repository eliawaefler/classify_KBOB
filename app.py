# /classify_KBOB/app.py
import streamlit as st
from unstructured.io import load_txt
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import pinecone
import os

# Function to add document to Pinecone
def add_document_to_pinecone(text):
    doc = load_txt(text)
    doc_text = " ".join(doc)
    doc_embedding = embeddings.embed(doc_text)
    index.upsert([(text, doc_embedding)])

# Function to classify query
def is_bim2fm_related(query):
    keywords = ["BIM2FM", "BIM2FM", "building information modeling", "facility management"]
    return any(keyword.lower() in query.lower() for keyword in keywords)

def main():
    # Initialize
    pinecone.init(api_key="your-pinecone-api-key", environment="your-pinecone-environment")
    index_name = "your-index-name"
    embeddings = OpenAIEmbeddings()
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=1536)
    index = pinecone.Index(index_name)
    

    
    st.title("RAG App with Pinecone")
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Document Content", text, height=300)
        
        if st.button("Add Document to Pinecone"):
            add_document_to_pinecone(text)
            st.success("Document added to Pinecone!")
    
    # Query input
    query = st.text_input("Enter your query:")
    if st.button("Retrieve and Generate Answer"):
        if is_bim2fm_related(query):
            query_embedding = embeddings.embed(query)
            results = index.query(query_embedding, top_k=5)
            retrieved_texts = [result["metadata"]["text"] for result in results["matches"]]
            combined_text = " ".join(retrieved_texts)
            
            # Generate answer using OpenAI
            llm = OpenAI(model="text-davinci-002")
            prompt = PromptTemplate(template="Given the following context: {context}\nAnswer the question: {question}",
                                    context=combined_text, question=query)
            answer = llm(prompt)
            
            # Display answer
            st.write("Answer:", answer)
        else:
            st.write("I cannot help with that...")
    
    # Close Pinecone connection
    index.close()
    pinecone.deinit()



if __name__ == "__main__":
    #MyUtils.check_version()
    main()
