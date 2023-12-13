import PyPDF2
from pymongo import InsertOne
from pymongo.operations import SearchIndexModel, ReplaceOne

from utils import generate_embedding


def ingest(openai_client, pdf_file, collection, embedding_field_name):
    documents = []
    with open(pdf_file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)

        page_num = 1
        print(f"Processing file {pdf_file}")
        for page in pdf_reader.pages:
            print(f"Processing page: {page_num}")
            text = page.extract_text()
            embedding = generate_embedding(openai_client=openai_client, text=text)
            documents.append(
                InsertOne(
                    {embedding_field_name: embedding, "text": text, "pdf": pdf_file}
                )
            )

            page_num += 1

    collection.bulk_write(documents)


# This requires Python Driver for MongoDB and MongoDB server version 7.0+ Atlas cluster
def create_search_index(collection, embedding_field_name, index, dimensions):
    collection.create_search_index(
        SearchIndexModel(
            definition={
                "mappings": {
                    "dynamic": True,
                    "fields": {
                        embedding_field_name: {
                            "dimensions": dimensions,
                            "similarity": "dotProduct",
                            "type": "knnVector",
                        }
                    },
                }
            },
            name=index,
        )
    )


def add_embedding(openai_client, collection, embedding_field_name):
    documents = []
    for doc in collection.find({"text": {"$exists": True}}):
        embedding = generate_embedding(openai_client=openai_client, text=doc["text"])
        doc[embedding_field_name] = embedding
        documents.append(ReplaceOne({"_id": doc["_id"]}, doc))

    collection.bulk_write(documents)
