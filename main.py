import os
import argparse
from openai import OpenAI
from pymongo import MongoClient

from ingest import ingest
from search import query_results

MONGO_URI = os.environ.get("MONGO_URI")

parser = argparse.ArgumentParser()
parser.add_argument("--ingest", action="store_true", help="Run ingest pipeline")
parser.add_argument("--query", action="store_true", help="Run query")
args = parser.parse_args()

if __name__ == "__main__":
    # Set up mongo and openai clients
    mongo_client = MongoClient(MONGO_URI)
    openai_client = OpenAI(
        base_url="https://demo.deployradiant.com/mongodb-rag-example/openai",
        api_key="notNeeded",
    )

    pdf_path = "0704.0044.pdf"
    db = mongo_client.plasmaPhysics
    collection = db.pdfs

    embedding_field_name = "openai_text_embedding_ada_002"

    if args.ingest:
        # Ingest the pdf
        ingest(openai_client=openai_client, pdf_file=pdf_path, collection=collection, embedding_field_name=embedding_field_name)
        # The following line has been commented out because it needs a newer version of MongoDB Cluster.
        # create_search_index(collection=collection, embedding_field_name=embedding_field_name, index=embedding_field_name + "_index", dimensions=1536)

    if args.query:
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

