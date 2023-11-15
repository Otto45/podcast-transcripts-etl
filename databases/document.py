import os
from typing import Dict, List

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def save_episode_document(document: Dict[str, str]):    
    uri = os.environ['MONGODB_ATLAS_CLUSTER_URI']
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        db = client['pod_search']
        collection = db['podcast_episodes']
        collection.insert_one(document)
    except Exception as e:
        print(e)

def get_episode_titles(podcast_name: str) -> List[str]:
    uri = os.environ['MONGODB_ATLAS_CLUSTER_URI']
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        db = client['pod_search']
        collection = db['podcast_episodes']

        query = {"podcast_name": podcast_name}
        projection = {"title": 1, "_id": 0}
        results = collection.find(query, projection)

        titles = []
        for document in results:
            titles.append(document["title"])
        
        return titles
        
    except Exception as e:
        print(e)