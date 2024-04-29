#!/usr/bin/env python3
'''Insert a document in Python'''


def insert_school(mongo_collection, **kwargs):
    '''function that inserts a new document in a collection based on kwargs'''

    insert_document = mongo_collection.insert_one(kwargs)

    return insert_document.inserted_id
