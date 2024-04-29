#!/usr/bin/env python3
'''Log stats'''

from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
nginx_collection = client.logs.nginx

methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

print(f'{nginx_collection.count_documents({})} logs')

print('Methods:')
for method in methods:
    count = nginx_collection.count_documents({'method': method})
    print(f'\tmethod {method}: {count}')

print(f'{nginx_collection.count_documents({"path": "/status"})} status check')
