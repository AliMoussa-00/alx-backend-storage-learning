#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''


from functools import wraps
from typing import Callable
import redis
import requests


r = redis.Redis()


def count_url_requests(method: Callable) -> Callable:
    '''
    A decorator that counts the number of times a url was accessed
    and increments the count in Redis with an expiration time of 10 sec.
    '''
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that increments the count of url accessed
        and adding an expiration time of 10 sec.
        """
        key = 'count: {}'.format(url)
        r.incr(key)

        r.expire(key, 10)

        return method(url)
    return wrapper


@count_url_requests
def get_page(url: str) -> str:
    '''
    function uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    '''
    response = requests.get(url)

    return (response.text)


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    response = get_page(url)
    print(response)

    # getting the cached url counter
    key = 'count: ' + url
    print(r.get(key))
