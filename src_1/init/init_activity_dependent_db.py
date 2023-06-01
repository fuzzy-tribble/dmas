import yaml
from pymongo import MongoClient

# Load the schema from a YAML file
with open('my_schema.yaml', 'r') as f:
    my_schema = yaml.safe_load(f)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['my_database']

# Create the collections and indexes
for collection in my_schema['collections']:
    db.create_collection(collection['name'])
    for index in collection.get('indexes', []):
        db[collection['name']].create_index(index['keys'], unique=index.get('unique', False))

# Add access permissions for collections
for collection in my_schema['collections']:
    db.command('createRole', collection['name'] + '_read', privileges=[{'resource': {'db': db.name, 'collection': collection['name']}, 'actions': ['find']}])
    db.command('createRole', collection['name'] + '_write', privileges=[{'resource': {'db': db.name, 'collection': collection['name']}, 'actions': ['insert', 'update', 'delete']}])
    
    
# Define a custom function in MongoDB
db.system.js.save({
  _id: 'insert_one_and_two',
  value: function(collection, doc1, doc2) {
    collection.insertOne(doc1);
    collection.insertOne(doc2);
  }
});

if __name__ == '__main__':
  # create the db and collections
  pass