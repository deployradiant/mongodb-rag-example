# MongoDB RAG example using Atlas VectorSearch and Radiant
This is a simple example of using MongoDB Atlas VectorSearch and Radiant to build a RAG (Retrieval-Augmented Generation) model. 

A more thorough writeup of this example can be found [here](https://radiantai.com/blog/rag-mongo-step-by-step).

## Setup

### Set up MongoDB Atlas
1. Create a [MongoDB Atlas account](https://www.mongodb.com/cloud/atlas/register).
2. Once you have registered and logged in, go to the dashboard to create your cluster. In order to take advantage of the `$vectorSearch` operator in an aggregation pipeline, you need to run MongoDB Atlas 6.0.11 or higher. 
3. Create a database and a collection. In the example code we use a database called `plasmaPhysics` and a collection called `pdfs`

### Set up Radiant
1. Request access to the Radiant platform on the [Radiant website](https://www.radiantai.com/?show_signup).
2. Once you have access to Radiant, [set up a provider](https://docs.radiantai.com/docs/tutorials/connect-to-a-provider) that serves the embedding model you would like to use.
3. [Set up an application](https://docs.radiantai.com/docs/tutorials/migrate-an-app), and configure it with the provider you set up earlier. 


## Ingest Data

The `ingest` function in [ingest.py](./ingest.py) will ingest a pdf file into the collection you created in MongoDB Atlas. It will extract the text from the pdf and store it in the `text` field. It will also generate an embedding and store it in the provided `embedding_field_name` field.

You can ingest a pdf file by running the following command:

```
python main.py --ingest --pdf /path/to/file.pdf
```


## Create a Search Index

Create a search index for the ingested data by following MongoDB Atlas' [documentation](https://docs.atlas.mongodb.com/atlas-search/tutorial/create-index/).


## Query Data

The `query` function in [query.py](./search.py) will query the collection you created in MongoDB Atlas. 
It will use the `$vectorSearch` operator to find the most similar documents to the provided query. It will then construct a user prompt enriched with the retrieved documents. 
This enriched prompt will be used to generate a new response from an LLM using the Radiant application you created. 

You can query the collection by running the following command:

```
python main.py --query
```



## Contributing Guidelines

Thank you for your interest in contributing to our project! Before you begin writing code, it would be helpful if you read these [contributing guidelines](CONTRIBUTING.md). Following them will make the contribution process easier and more efficient for everyone involved.

Please note that the project is released with an [MIT License](https://opensource.org/licenses/MIT).

