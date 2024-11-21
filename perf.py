import time
from pymongo import MongoClient

MDB_URI=""
# Connect to the MongoDB server
client = MongoClient(MDB_URI)
db = client['sample_mflix']
collection = db['movies']

# Define the first aggregation pipeline
pipeline1 = [{'$project': {'title': 1, 'imdb_rating': '$imdb.rating', 'tomatoes_viewer_rating': '$tomatoes.viewer.rating'}}, {'$addFields': {'combined_rating': {'$avg': ['$imdb_rating', '$tomatoes_viewer_rating']}}}, {'$sort': {'combined_rating': -1}}, {'$limit': 5}]

# Define the second aggregation pipeline
pipeline2 = [{'$project': {'title': 1, 'imdb_rating': '$imdb.rating', 'tomatoes_viewer_rating': '$tomatoes.viewer.rating'}}, {'$addFields': {'combined_rating': {'$avg': ['$imdb_rating', '$tomatoes_viewer_rating']}}}, {'$sort': {'combined_rating': -1}}, {'$limit': 5}]

# Function to measure execution time of a pipeline
def measure_execution_time(pipeline):
    start_time = time.time()
    list(collection.aggregate(pipeline))
    end_time = time.time()
    return end_time - start_time
print("cold start, no index")
time_pipeline1 = measure_execution_time(pipeline1)
print(f"Execution time for pipeline 1: {time_pipeline1:.6f} seconds")
print("warm start, no index")
time_pipeline2 = measure_execution_time(pipeline2)
print(f"Execution time for pipeline 2: {time_pipeline2:.6f} seconds")
print("drop indexes...")
# Drop the indexes
collection.drop_indexes()
time.sleep(10)
print("create indexes...")
# Create indexes on 'imdb.rating' and 'tomatoes.viewer.rating'
collection.create_index('imdb.rating')
collection.create_index('tomatoes.viewer.rating')
time.sleep(10)
time_pipeline1 = measure_execution_time(pipeline1)
print(f"Execution time for pipeline: {time_pipeline1:.6f} seconds")
time_pipeline2 = measure_execution_time(pipeline2)
print(f"Execution time for pipeline: {time_pipeline2:.6f} seconds")

"""
cold start, no index
Execution time for pipeline 1: 0.918224 seconds
warm start, no index
Execution time for pipeline 2: 0.141815 seconds
drop indexes...
create indexes...
Execution time for pipeline: 0.144723 seconds
Execution time for pipeline: 0.141932 seconds
"""
