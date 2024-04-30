#!/usr/bin/env python3
'''Log stats - new version'''

from pymongo import MongoClient


def get_log_stats_improved(nginx_collection):
    '''a function to get the so status'''

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    print(f'{nginx_collection.count_documents({})} logs')

    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    status = nginx_collection.count_documents({"path": "/status"})
    print(f'{status} status check')

    ip_pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 10
        }
    ]

    results = nginx_collection.aggregate(ip_pipeline)

    print("IPs:")
    for res in results:
        print(f'\t{res.get("_id")}: {res.get("count")}')


def main():
    '''main function'''

    client = MongoClient('mongodb://127.0.0.1:27017')
    get_log_stats_improved(client.logs.nginx)


if __name__ == '__main__':
    main()
