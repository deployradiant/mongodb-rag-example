import os
import argparse
from openai import OpenAI
from pymongo import MongoClient
from pathlib import Path

from ingest import ingest
from search import query_results

MONGO_URI = os.environ.get("MONGO_URI")

parser = argparse.ArgumentParser()
parser.add_argument("--ingest", action="store_true", help="Run ingest pipeline")
parser.add_argument("--query", action="store_true", help="Run query")
parser.add_argument("--pdf", type=str, help="Path to PDF file")
parser.add_argument("--embedding-field-name", type=str, help="Name of embedding field")
parser.add_argument("--query-text", type=str, help="Query string")
args = parser.parse_args()

if __name__ == "__main__":
    # Set up mongo and openai clients
    mongo_client = MongoClient(MONGO_URI)
    openai_client = OpenAI(
        base_url="https://demo.deployradiant.com/mongodb-rag-example/openai",
        api_key="notNeeded",
    )

    # Set database to `plasmaPhysics` and collection to `pdfs`
    # This is configured in MongoDB Atlas
    db = mongo_client.plasmaPhysics
    collection = db.pdfs

    embedding_field_name = "openai_text_embedding_ada_002"
    if args.embedding_field_name:
        embedding_field_name = args["embedding-field-name"]

    if args.ingest:
        if not args.pdf:
            raise ValueError("--pdf argument required with --ingest")

        pdf_path = args.pdf
        if pdf_path:
            if os.path.isdir(pdf_path):
                # Path provided is a directory
                pdf_files = Path(pdf_path).glob("**/*.pdf")
                for pdf_file in pdf_files:
                    ingest(
                        openai_client=openai_client,
                        pdf_file=pdf_file,
                        collection=collection,
                        embedding_field_name=embedding_field_name,
                    )

            else:
                # Single file provided
                ingest(
                    openai_client=openai_client,
                    pdf_file=pdf_path,
                    collection=collection,
                    embedding_field_name=embedding_field_name,
                )
        # The following line has been commented out because it needs a newer version of MongoDB Cluster.
        # create_search_index(collection=collection, embedding_field_name=embedding_field_name, index=embedding_field_name + "_index", dimensions=1536)

    if args.query:
        if not args.query_text:
            raise ValueError("--query-text argument required with --query")
        # Query the pdf
        query = args.query_text
        result = query_results(
            openai_client=openai_client,
            collection=collection,
            field=embedding_field_name,
            index=embedding_field_name + "_index",
            query=query,
        )
        print(result)
