#!/usr/bin/env python3
'''Top students'''


# Using Aggregation
def top_students(mongo_collection):
    '''function that returns all students sorted by average score'''

    pipeline = [
        {
            "$project": {
                '_id': 1,
                'name': 1,
                'averageScore': {'$avg': '$topics.score'},
            }
        },
        {
            '$sort': {'averageScore': -1},
        }
    ]

    results = mongo_collection.aggregate(pipeline)
    return results
