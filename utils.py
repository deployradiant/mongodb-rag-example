from openai import OpenAI


def generate_embedding(openai_client: OpenAI, text: str) -> list[float]:
    return (
        openai_client.embeddings.create(input=[text], model="notNeeded")
        .data[0]
        .embedding
    )
