#!/usr/bin/env python3
'''Log stats'''

from pymongo import MongoClient


def get_log_stats(nginx_collection):
    '''a function to get the so status'''
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    print(f'{nginx_collection.count_documents({})} logs')

    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    status = nginx_collection.count_documents({"path": "/status"})
    print(f'{status} status check')


def main():
    '''main function'''
    client = MongoClient('mongodb://127.0.0.1:27017')

    get_log_stats(client.logs.nginx)


if __name__ == '__main__':
    main()
