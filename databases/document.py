import os
from typing import Dict

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
