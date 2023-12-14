import os

import streamlit as st
from openai import OpenAI
from pymongo import MongoClient

from search import query_results

st.title("Plasma Physics GPT")

MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
openai_client = OpenAI(
    base_url="https://demo.deployradiant.com/mongodb-rag-example/openai",
    api_key="notNeeded",
)

db = mongo_client.plasmaPhysics
collection = db.pdfs
embedding_field_name = "openai_text_embedding_ada_002"

query = st.text_input("Enter search query:")
if query:
    result = query_results(
        openai_client=openai_client,
        collection=collection,
        field=embedding_field_name,
        index=embedding_field_name + "_index",
        query=query,
    )

    if result:
        st.write(result)
    else:
        st.write("No results found")

st.sidebar.header("About")
st.sidebar.markdown(
    """
    This is a demo of a RAG (Retrieval-Augmented Generation) model for Plasma Physics built using the Radiant platform and MongoDB Atlas.
    Here is a link to the source code: [GitHub](https://github.com/tbd-company/mongodb-rag-example)
    
    
    To learn more about Radiant please visit the [Radiant website](https://www.radiantai.com).
    To learn more about MongoDB Atlas please visit the [MongoDB Atlas website](https://www.mongodb.com/cloud/atlas).
    
    Email akanekar@radiantai.com for any questions.
    """
)
