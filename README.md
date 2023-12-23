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

Thank you for your interest in contributing to our project! Before you begin writing code, it would be helpful if you read these guidelines. Following them will make the contribution process easier and more efficient for everyone involved.

Please note that the project is released with an [MIT License](https://opensource.org/licenses/MIT).

### How to contribute

Firstly, ensure you have forked the repository and are working on a branch that is based off of our 'main' branch. If you're unsure about how to do this, there are many guides available online that will help.

Then follow these steps:
  1. **Bugs**: Describe bugs by creating a new issue. Explain what you expected to see, what you saw instead, steps to reproduce it, and any additional context or screenshots that might be helpful.
  2. **Feature requests**: Propose features by opening a new issue. Explain what the feature should do, how it would be used, and why you believe it would be a useful addition.
  3. **Pull Requests**: Fix or add functionality to the project by making changes to the codebase yourself. Ensure that your code is following the coding standards outlined in the next section and make sure all tests pass before submitting a PR.

### Community

We aim to maintain a welcoming and respectful community. Keep all discussions on topic and refrain from rude or inappropriate behavior. Keep in mind that this a place where people come to learn and share, so please respect their efforts.

### Submitting a Pull Request

Before you submit your pull request consider the following guidelines:

  - Try to make your pull request as small as possible. The quicker it can be reviewed, the quicker it can be merged!
  - Include reasoning for your changes, this makes it a lot easier to review
  - If your PR resolves an open issue(s), list them in your PR comment

That's it! You're ready to go. Thanks again for contributing to this project.
