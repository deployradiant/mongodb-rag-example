import os
from openai import OpenAI
from pymongo import MongoClient

from ingest import ingest, create_search_index, add_embedding
from search import query_results

MONGO_URI = os.environ.get("MONGO_URI")

if __name__ == "__main__":
    # Set up mongo and openai clients
    mongo_client = MongoClient(MONGO_URI)
    openai_client = OpenAI(
        base_url="https://demo.deployradiant.com/mongodb-rag-example/openai/",
        api_key="notNeeded",
    )

    # Ingest the pdf
    pdf_path = "0704.0044.pdf"
    db = mongo_client.plasmaPhysics
    collection = db.pdfs

    embedding_field_name = "openai_text_embedding_ada_002"
    # ingest(openai_client=openai_client, pdf_file=pdf_path, collection=collection, embedding_field_name=embedding_field_name)
    # create_search_index(collection=collection, embedding_field_name=embedding_field_name, index=embedding_field_name + "_index", dimensions=1536)

    mistral_openai_client = OpenAI(
        base_url="https://demo.deployradiant.com/mistral-embedding/openai/",
        api_key="notNeeded",
    )
    # add_embedding(openai_client=mistral_openai_client, collection=collection, embedding_field_name="mistral_embedding")
    # Query the pdf
    query = "What is Goldreich-Sridhar scaling?"
    result = query_results(
        openai_client=openai_client,
        collection=collection,
        field=embedding_field_name,
        index=embedding_field_name + "_index",
        query=query,
    )
    print(result)

    query = "What is Goldreich-Sridhar scaling?"
    result = query_results(
        openai_client=mistral_openai_client,
        collection=collection,
        field="mistral_embedding",
        index="vector_index",
        query=query,
    )
    print(result)
