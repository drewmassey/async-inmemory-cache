# Sample Async In Memory Cache

This repo provides a simple template for an asynchronous, in memory cache in python 3.

# Some assumptions / use case

Since identity and security providers often provide tokens with a limited duration, one way to design a system would be to identify separate caches with separate times-to-live. In `client.py` we just have a single cache with a 5-second duration -- not so useful in practice. In the context of a temporary credential for AWS (which is typically 3600 seconds), we might have a cache named `1-hour` or some such. Single-use tokens would presumably never be written to cache (since they would serve no purpose after that one use).

There is of course the option of implementing a single TTL cache with various expirations, which would simplify the code by only having one cache, but (depending on the distribution of the tokens with respect to their longevity) have a less obvious way of horizontally scaling resources.

A weird quirk of the `SimpleMemoryCache` in this python library seems to be that the entire cache expires after the specified time, as demonstrated in `client.py`. Per-item cache TTL is not documented.

# General Information

## Local Deployment
```
cd <repo>
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python client.py
```

## Working in an asynchronous setting

The main reason to use an async cache here is so that you are not waiting for blocking io calls that slow you down; you would have to be at a much higher performing system (probably unlikely to be written in python) for this to be an issue.

## Error Modes
Depending on your setup, you could have a couple of problems:
	- Cache misses (i.e., looking up values that aren't there)
	- Cache invalidation. Not implemented here, but returning a token that is expired or has been revoked.

## Tests (and linting)

Given the simplicity of the code I've provided, I haven't provided a lot of tests.
A test suite would want to make sure that it correctly anticipated the results of the async calls.

## Documentation
Please see the code for a few call out of interesting behavior in the comments


# Other Considerations

## Performance/complexity trade offs

As mentioned in the code, it might be worth making a few separate caches depending on TTL.
By default the asyncio library uses a Least Requested Unit (LRU) for ejecting entries from the cache; there might be preferable algorithms depending on the specific use case.

## Problem Areas

There doesn't seem to be any obvious way to specify the size of a SimpleMemoryCache in the example provided; obviously in a production context we would like to understand very clearly the average cache payload and the scale of requests that we would like to cache.

# Further Reading

Some of the sources consulted for this project were:
- https://pypi.org/project/aiocache/
- https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e