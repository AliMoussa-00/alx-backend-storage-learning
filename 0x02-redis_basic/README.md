# Redis

[learn redis]([How to Use Redis With Python – Real Python](https://realpython.com/python-redis/))

[tasks]()

---

## Installing

[folow in this website](https://realpython.com/python-redis/#installing-redis-from-source)

check if installed:

```shell
$ redis-cli --version
```

---

## Inroduction

Redis has a **client-server architecture** and uses a **request-response model**. This means that you (the client) connect to a Redis server through TCP connection, on port 6379 by default. You request some action (like some form of reading, writing, getting, setting, or updating), and the server *serves* you back a response.

## command line interface

The `cli` in `redis-cli` stands for **command line interface**, and the `server` in `redis-server` is for, well, running a server. In the same way that you would run `python` at the command line, you can run `redis-cli` to jump into an interactive REPL (Read Eval Print Loop) where you can run client commands directly from the shell.

First, however, you’ll need to launch `redis-server` so that you have a running Redis server to talk to. A common way to do this in development is to start a server at **localhost** (IPv4 address `127.0.0.1`), which is the default unless you tell Redis otherwise. You can also pass `redis-server` the name of your configuration file, which is akin to specifying all of its key-value pairs as command-line arguments

- start redis server
  

```shell
$ redis-server /etc/redis/6379.conf
```

- now we can start Redis
  

```shell
$ redis-cli
```

---

## Commands

**!! Redis commands are case-insensitive, although their Python counterparts are most definitely not.**

- check if server working
  

```shell
127.0.0.1:6379 > PING
PONG
```

**!! the next commands will be in `redis-cli` and `pyhton`**

```shell
127.0.0.1:6379 > SET Bahamas Nassau
OK
127.0.0.1:6379 > SET Croatia Zagreb
OK
127.0.0.1:6379 > GET Croatia
"Zagreb"
127.0.0.1:6379 > GET Japan
(nil)


127.0.0.1:6379 > MSET Lebanon Beirut Norway Oslo France Paris
OK
127.0.0.1:6379 > MGET Lebanon Norway Bahamas
1) "Beirut"
2) "Oslo"
3) "Nassau"


127.0.0.1:6379 > EXISTS Norway
(integer) 1
127.0.0.1:6379 > EXISTS Sweden
(integer) 0
```

```python
>>> capitals = {}
>>> capitals["Bahamas"] = "Nassau"
>>> capitals["Croatia"] = "Zagreb"
>>> capitals.get("Croatia")
'Zagreb'
>>> capitals.get("Japan")  # None


>>> capitals.update({
...     "Lebanon": "Beirut",
...     "Norway": "Oslo",
...     "France": "Paris",
... })
>>> [capitals.get(k) for k in ("Lebanon", "Norway", "Bahamas")]
['Beirut', 'Oslo', 'Nassau']


>>> "Norway" in capitals
True
>>> "Sweden" in capitals
False
```

- Delete all the keys of the currently selected DB. This command never fails.
  

```shell
127.0.0.1:6379> FLUSHDB
OK
127.0.0.1:6379> QUIT
```

---

## Using redis-py: Redis in Python

### Install

[`redis-py`](https://github.com/andymccurdy/redis-py) is a well-established Python client library that lets you talk to a Redis server directly through Python calls:

Shell

```shell
$ python -m pip install redis
```

**!! Next, make sure that your Redis server is still up and running in the background. You can check with `pgrep redis-server`, and if you come up empty-handed, then restart a local server with `redis-server /etc/redis/6379.conf`.**

### Hello

```python
>>> import redis
>>> r = redis.Redis()
>>> r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
True
>>> r.get("Bahamas")
b'Nassau'
```

Notice also that the type of the returned object, `b'Nassau'` in Line 6, is Python’s [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) type, not `str`. It is `bytes` rather than `str` that is the most common return type across `redis-py`, so you may need to call **`r.get("Bahamas").decode("utf-8")`** depending on what you want to actually do with the returned bytestring.

### Allowed Key Types

One thing that’s worth knowing is that `redis-py` requires that you pass it keys that are `bytes`, `str`, `int`, or `float`. (It will convert the last 3 of these types to `bytes` before sending them off to the server.)

---

### Examples

#### 1. Connecting to Redis:

```python
import redis

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Optional: Test the connection
print("Redis server is running:", r.ping())
```

#### 2. String Operations:

```python
# Set a key-value pair
r.set('name', 'Alice')

# Get the value of a key
name = r.get('name')
print("Name:", name.decode('utf-8'))

# Increment a numeric value
r.set('counter', 10)
r.incr('counter')
counter = r.get('counter')
print("Counter:", int(counter))
```

#### 3. List Operations:

```python
# Push elements to the end of a list
r.rpush('fruits', 'apple', 'banana', 'cherry')

# Get all elements of the list
fruits = r.lrange('fruits', 0, -1)
print("Fruits:", [fruit.decode('utf-8') for fruit in fruits])

# Pop an element from the end of the list
fruit = r.rpop('fruits')
print("Popped Fruit:", fruit.decode('utf-8'))
```

#### 4. Set Operations:

```python
# Add elements to a set
r.sadd('colors', 'red', 'green', 'blue')

# Get all elements of the set
colors = r.smembers('colors')
print("Colors:", [color.decode('utf-8') for color in colors])

# Check if an element exists in the set
print("Is 'red' in colors set?", r.sismember('colors', 'red'))
```

#### 5. Hash Operations:

```python
# Set multiple fields of a hash
r.hmset('user:1', {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'})

# Get all fields and values of a hash
user = r.hgetall('user:1')
print("User:", {key.decode('utf-8'): value.decode('utf-8') for key, value in user.items()})

# Get the value of a specific field in a hash
age = r.hget('user:1', 'age')
print("Age:", int(age))
```

#### 6. Expire Key:

```python
# Set a key to expire after 60 seconds
r.set('temp_key', 'value', ex=60)
```

#### 7. Publish/Subscribe (Pub/Sub):

```python
# Publish a message to a channel
r.publish('channel', 'Hello, world!')

# Subscribe to a channel
pubsub = r.pubsub()
pubsub.subscribe('channel')

# Listen for messages
for message in pubsub.listen():
    print("Received:", message['data'].decode('utf-8'))
```

#### 8. Pipelining:

```python
# Use pipelining to execute multiple commands in one round trip
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.execute()
```

#### 9. Atomic Transactions:

```python
import redis

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Define the keys to watch
key_to_watch = 'balance'

# Start a transaction block
with r.pipeline() as pipe:
    while True:
        try:
            # Watch the key for changes
            pipe.watch(key_to_watch)
            
            # Get the current balance
            balance = int(pipe.get(key_to_watch))
            
            # Check if the balance is sufficient
            if balance >= 10:
                # Begin the transaction
                pipe.multi()
                
                # Decrease the balance by 10
                pipe.decrby(key_to_watch, 10)
                
                # Set the result of the purchase
                pipe.set('purchase', 'success')
                
                # Execute the transaction atomically
                pipe.execute()
                break
            else:
                print("Insufficient balance")
                break
        except redis.WatchError:
            # Another client modified the watched key
            continue

```

---
