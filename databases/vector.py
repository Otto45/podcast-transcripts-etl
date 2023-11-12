import os
from typing import Dict

from utils.podcast_episode_document import prep_episode_document_for_vector_embedding

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi, ServerApiVersion
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

def create_and_save_vector_embeddings(document: Dict[str, str]) -> None:
    uri = os.environ['MONGODB_ATLAS_CLUSTER_URI']
    client = MongoClient(uri, server_api=ServerApi(ServerApiVersion.V1))

    db_name = "pod_search"
    collection_name = "podcast_episode_embeddings"
    collection = client[db_name][collection_name]
    index_name = "episode_embeddings"

    vector_store = MongoDBAtlasVectorSearch(
        collection,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        index_name=index_name
    )

    text_chunks, metadatas = prep_episode_document_for_vector_embedding(document)

    vector_store.add_texts(text_chunks, metadatas)
