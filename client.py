import asyncio
from aiocache import caches, SimpleMemoryCache
from aiocache.serializers import StringSerializer, PickleSerializer
import uuid
import time

ELEMENTS_IN_CACHE = 10000
CACHE_NAME = 'default'
CACHE_TTL_SECONDS = 5

# You can use either classes or strings for referencing classes
caches.set_config({
	'default': {
		'cache': "aiocache.SimpleMemoryCache",
		'serializer': {
			'class': "aiocache.serializers.StringSerializer"
		},
		'ttl': CACHE_TTL_SECONDS # we keep this super short for demonstration purposes
	},
})

# We globally scope this for demo purposes
cache = caches.get(CACHE_NAME)  

async def add(key, value):
	await cache.set(key, value)
	# This is just for testing
	# assert await cache.get(key) == value

async def increment(key):
	await cache.increment(key)

async def main():

	# Presumably in practice our main routine would accept outside input
	# or do something more interesting than this.
	print("Populating cache with {} elements...".format(ELEMENTS_IN_CACHE))

	# Populate the cache with some stuff
	# This crumbles at scale since the cache expiration is so short....
	tasks = [add("key-{}".format(i), uuid.uuid4().hex) for i in range(ELEMENTS_IN_CACHE)]
	await asyncio.gather(*tasks)
	print("Done")
	print("Here are the first 10:")
	for i in range (0,10):
		# This is actually a good example of how the await keyword can be embedded.
		print("Value of key-{} is:\t{}".format(i,await cache.get("key-{}".format(i))))

	print("Here is how we would implement simple incrementing")
	await cache.set("incremental",0)
	await cache.increment("incremental")
	print("Value of surviving incremented key is {}".format(await(cache.get("incremental"))))

	print("Letting the cache expire, see you in {} seconds...".format(CACHE_TTL_SECONDS))

	# Here's how one key would keep alive, although the simple memory cache is behaving strangely:
	for i in range(CACHE_TTL_SECONDS):
		time.sleep(1)
		await cache.increment("incremental")
		print("Value of surviving incremented key is {}".format(await(cache.get("incremental"))))		

	print("Oops! Cache is expired.")
	for i in range (0,10):
		print("Value of key-{} is:\t{}".format(i,await cache.get("key-{}".format(i))))

	print("Value of surviving incremented key is {}".format(await(cache.get("incremental"))))



if __name__ == "__main__":
	asyncio.run(main())