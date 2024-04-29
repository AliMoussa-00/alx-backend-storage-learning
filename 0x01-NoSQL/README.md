# MongoDB

MongoDB is a **document-oriented** database classified as NoSQL

[MongoDB and Python]([Python and MongoDB: Connecting to NoSQL Databases – Real Python](https://realpython.com/introduction-to-mongodb-and-python/))

[tasks]()

---

## Introduction:

MongoDB is a popular document-oriented NoSQL database, known for its flexibility, scalability, and ease of use. Unlike traditional relational databases, MongoDB stores data in flexible, **JSON-like documents** with **dynamic schemas**. Here's a simple introduction to MongoDB:

1. **Document-Oriented**: MongoDB stores data in collections, where each collection contains documents. These documents are similar to JSON objects and can have varying structures, allowing for easy storage of complex and nested data.
  
2. **Dynamic Schema**: MongoDB is schema-less or has a dynamic schema, meaning that documents in a collection do not need to have the same structure. This flexibility makes MongoDB well-suited for handling semi-structured or unstructured data.
  
3. **Scalability**: MongoDB is designed to scale horizontally, meaning you can add more servers to distribute the load and accommodate growing data volumes and traffic. It supports sharding, replication, and automatic failover to ensure high availability and performance.
  
4. **Querying and Indexing**: MongoDB provides powerful querying capabilities using a rich query language and supports indexing to optimize query performance. You can perform CRUD operations (Create, Read, Update, Delete) as well as complex queries, aggregations, and geospatial queries.
  
5. **High Performance**: MongoDB is known for its high performance, especially for read and write-heavy workloads. It uses memory-mapped files for storage and supports in-memory computing for caching frequently accessed data, resulting in low latency and fast response times.
  
6. **Rich Ecosystem**: MongoDB has a rich ecosystem with official drivers available for various programming languages, including Python, Java, Node.js, and others. It also provides tools for monitoring, management, and data visualization, making it easy to work with MongoDB in different environments.
  
7. **Use Cases**: MongoDB is used in a wide range of applications, including web and mobile app development, content management systems, real-time analytics, IoT (Internet of Things), and more. Its flexibility and scalability make it suitable for both small-scale projects and large-scale enterprise applications.
  

---

## Installation:

[install for Ubuntu]([Install MongoDB Community Edition on Ubuntu - MongoDB Manual v7.0](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/))

---

## Manage MongoDB

To run and manage your `mongod` process, you will be using your operating system's built-in **init system** .

 Recent versions of Linux tend to use **systemd** (which uses the `systemctl` command), while older versions of Linux tend to use **System V init** (which uses the `service` command).

### Start

```bash
sudo systemctl start mongod
```

- !! If you receive an error similar to the following when starting `mongod`
  

`Failed to start mongod.service: Unit mongod.service not found.`

Run the following command first:

```bash
sudo systemctl daemon-reload
```

### Verify that MongoDB has started successfully.

```bash
sudo systemctl status mongod
```

- !! You can optionally ensure that MongoDB will start following a system reboot by issuing the following command
  

```bash
sudo systemctl enable mongod
```

### Stop MongoDB

```bash
sudo systemctl stop mongod
```

### Restart MongoDB

```bash
sudo systemctl restart mongod
```

### Logs

You can follow the state of the process for errors or important messages by watching the output in the `/var/log/mongodb/mongod.log` file

### Begin using MongoDB

Start a `mongosh` session on the same host machine as the `mongod`. You can run `mongosh` without any command-line options to connect to a `mongod`that is running on your localhost with default port `27017.`

```bash
mongosh
```

# Using MongoDB With Python and PyMongo

In general, PyMongo provides a rich set of tools that you can use to communicate with a MongoDB server. It provides functionality to query, retrieve results, write and delete data, and run database commands.

## Installing PyMongo

#### start vertual environment

```bash
$ python3 -m venv .env
```

#### install PyMongo

```bash
$ pip install pymongo
```

## Establishing a Connection

```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
# or we can use
client = MongoClient(host="localhost", port=27017)

# Access a database (create it if it doesn't exist)
db = client['mydatabase']

# Access a collection within the database (create it if it doesn't exist)
collection = db['mycollection']

# Now you can perform operations on the collection

```

---

## Working With Databases, Collections, and Documents

```python
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Step 2: Access a database
db = client['mydatabase']

# Step 3: Access or create a collection within the database
collection = db['mycollection']

# Step 4: Inserting documents into the collection
# You can insert single documents
post_1 = {"title": "Python Basics", "content": "Python programming fundamentals"}
post_2 = {"title": "Data Analysis", "content": "Analyzing data using Python libraries"}
collection.insert_one(post_1)
collection.insert_one(post_2)

# Or insert multiple documents
posts = [
    {"title": "Web Development", "content": "Building web applications with Flask"},
    {"title": "Machine Learning", "content": "Using machine learning algorithms with scikit-learn"}
]
collection.insert_many(posts)

# Step 5: Querying documents from the collection
# Find one document
result = collection.find_one({"title": "Python Basics"})
print(result)

# Find all documents
all_posts = collection.find()
for post in all_posts:
    print(post)

# Find documents based on a specific condition
python_posts = collection.find({"title": {"$regex": "^Python"}})
for post in python_posts:
    print(post)

# Step 6: Updating documents
# Update one document
collection.update_one({"title": "Python Basics"}, {"$set": {"content": "Python programming for beginners"}})

# Update multiple documents
collection.update_many({"title": {"$regex": "^Python"}}, {"$set": {"content": "Python programming"}})

# Step 7: Deleting documents
# Delete one document
collection.delete_one({"title": "Python Basics"})

# Delete multiple documents
collection.delete_many({"title": {"$regex": "^Python"}})

# Step 8: Dropping the collection (optional)
# This will delete the collection entirely
db.drop_collection('mycollection')

# Step 9: Dropping the database (optional)
# This will delete the entire database
client.drop_database('mydatabase')

```

---

## Closing Connections

Establishing a connection to a MongoDB database is typically an expensive operation. If you have an application that constantly retrieves and manipulates data in a MongoDB database, then you probably don’t want to be opening and closing the connection all the time since this might affect your application’s performance.

In this kind of situation, you should keep your connection alive and only close it before exiting the application to clear all the acquired resources. You can close the connection by calling `.close()` on the `MongoClient` instance:

```python
client.close()
```

OR

Another situation is when you have an application that occasionally uses a MongoDB database. In this case, you might want to open the connection when needed and close it immediately after use for freeing the acquired resources. A consistent approach to this problem would be to use the `with` statement.

we don't need to call ``.close()` in this case

```python
import pprint
from pymongo import MongoClient

with MongoClient() as client:
    db = client.rptutorials
    for doc in db.tutorial.find():
        pprint.pprint(doc)
```

---

# Using (ODM) MongoDB With Python and MongoEngine

While `PyMongo` is a great and powerful Python driver for interfacing with MongoDB, it’s probably a bit **too low-level** for many of your projects. With PyMongo, you’ll have to write a lot of code to consistently insert, retrieve, update, and delete documents.

## Installing MongoEngine

```bash
pip install mongoengine
```

## Working With Collections and Documents

```python
from mongoengine import connect, Document, StringField, IntField

# Step 1: Connect to MongoDB
connect('mydatabase', host='localhost', port=27017)

# Step 2: Define your data models
class User(Document):
    name = StringField(required=True, max_length=50)
    age = IntField(required=True)

# Step 3: Create and save documents
# Create new user objects
user1 = User(name="Alice", age=30)
user2 = User(name="Bob", age=25)

# Save them to the database
user1.save()
user2.save()

# Step 4: Querying documents
# Find all users
all_users = User.objects()
for user in all_users:
    print(user.name, user.age)

# Find users based on a specific condition
bob = User.objects(name="Bob").first()
print(bob.name, bob.age)

# Step 5: Updating documents
# Update a user's age
bob.update(age=26)

# Step 6: Deleting documents
# Delete a user
bob.delete()

# Step 7: Dropping the collection (optional)
# This will delete all documents in the collection
User.objects().delete()

# Step 8: Dropping the database (optional)
# This will delete the entire database
connect().drop_database('mydatabase')

```

There are a few general parameters that you can use to validate fields. Here are some of the more commonly used parameters:

- **`db_field`** specifies a different field name.
- **`required`** ensures that the field is provided.
- **`default`** provides a default value for a given field if no value is given.
- **`unique`** ensures that no other document in the collection has the same value for this field.

# MongoDB Command File

To create a MongoDB command file, you can simply write MongoDB commands line by line in a text file. MongoDB command files typically have a `.js` extension, indicating that they contain JavaScript code that MongoDB shell (`mongo`) can execute.

```javascript
// This is a comment
use mydatabase;

db.mycollection.insertOne({
    name: "John",
    age: 30,
    status: "active"
});

db.mycollection.find();

```

then we can use

```bash
cat mongo_db_file.js | mongosh
# OR
mongosh < mongo_db_file.js
```
