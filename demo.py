from openai import AzureOpenAI
import json
# Set up Azure OpenAI credentials
azure_endpoint = "https://.openai.azure.com"
azure_deployment = "gpt-4o"
api_key = ""
api_version = "2024-10-21"

az_client = AzureOpenAI(azure_endpoint=azure_endpoint,api_version=api_version,api_key=api_key)
user_input = 'What are the best 5 movies?'
messages=[
    {"role": "system", "content": """
You are a helpful assistant that translates English to MongoDB Aggregation Pipeline array. Only respond with the array, ready to use.
"""},
                {"role": "user", "content": f"""
[context]
collection = "movies"
[verified pipelines]
[user_input=`What are the best 1337 movies`]
{[
    {
        '$project': {
            'title': 1, 
            'imdb_rating': '$imdb.rating', 
            'tomatoes_viewer_rating': '$tomatoes.viewer.rating'
        }
    }, {
        '$addFields': {
            'combined_rating': {
                '$avg': [
                    '$imdb_rating', '$tomatoes_viewer_rating'
                ]
            }
        }
    }, {
        '$sort': {
            'combined_rating': -1
        }
    }, {
        '$limit': 1337
    }
]}
[/verified pipelines]
[/context]
     
USE THE [verified pipelines] IN THE [context] TO RESPOND TO [user_input=`{user_input}`] AND RETURN A JSON ARRAY MONGODB AGGREGATION PIPELINE

[response criteria]
        - JSON object with keys 'pipeline' and 'user_input'
        - response must be JSON 
[/response criteria]
"""}
]
ai_msg = az_client.chat.completions.create(model="gpt-4o", messages=messages, response_format={ "type": "json_object" } )
ai_msg = json.loads(ai_msg.choices[0].message.content)
print(ai_msg['pipeline'])
"""
[{'$project': {'title': 1, 'imdb_rating': '$imdb.rating', 'tomatoes_viewer_rating': '$tomatoes.viewer.rating'}}, {'$addFields': {'combined_rating': {'$avg': ['$imdb_rating', '$tomatoes_viewer_rating']}}}, {'$sort': {'combined_rating': -1}}, {'$limit': 5}]
"""
