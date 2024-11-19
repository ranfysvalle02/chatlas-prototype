# chatlas-prototype

---

# Chatlas: Talk with Your Data

In today's data-driven world, the ability to efficiently query and analyze large datasets is more critical than ever. MongoDB's aggregation framework offers powerful tools for data analysis, but constructing optimized aggregation pipelines can be complex. Integrating natural language interfaces with verified queries can simplify this process, allowing you to "talk with your data" while ensuring consistency, performance, and security.

Integrating natural language interfaces with verified queries allows users to interact with data intuitively while maintaining high standards of performance and security. By leveraging optimized aggregation pipelines in MongoDB, you ensure that your applications are scalable and responsive.

This approach has immense potential in various fields, including:

- **Data Analysis**: Analysts can query large datasets without needing to understand complex query languages.
- **Customer Service**: Assistants can provide customers with real-time data insights based on their queries.
- **Business Intelligence**: Decision-makers can access and analyze data quickly and efficiently.

---

## The Value of Conversational Data Interaction

### Enhanced Accessibility

- **Democratization of Data**: Natural language interfaces allow users of all technical backgrounds to access and interact with data effortlessly.
- **Intuitive Engagement**: Users can pose questions in plain English, eliminating the need to learn complex query syntax.

### Increased Efficiency

- **Faster Insights**: Immediate data retrieval accelerates decision-making processes, enabling organizations to respond swiftly to changing conditions.
- **Reduced Training Costs**: Minimizes the need for extensive training on query languages, saving time and resources.

### Improved Collaboration

- **Unified Communication**: Facilitates better communication among teams by providing a common, understandable way to interact with data.
- **Customer Engagement**: Enhances customer service by allowing representatives to access information quickly during interactions.

---

## The Challenge of Natural Language to Database Queries

Translating natural language into database queries bridges the gap between user intent and data retrieval. However, this translation must ensure:

- **Consistency**: Queries should produce reliable and expected results.
- **Generalization**: The system should handle a variety of similar queries effectively.
- **Performance**: Queries must be optimized to minimize resource usage and execution time.

Unverified or poorly constructed queries can lead to inefficiencies, inaccurate results, and potential security risks. This is where **verified queries**—predefined, tested, and optimized query patterns—play a crucial role.

---

## The Importance of Verified Queries

Using verified queries ensures:

### Consistency

- **Reliable Results**: Pre-tested queries produce expected outcomes.
- **Standardization**: Adheres to established query patterns within your applications.

### Generalization

- **Adaptability**: The assistant can handle variations of similar queries effectively.
- **Scalability**: New queries can be generated based on existing verified templates.

### Performance

- **Optimization**: Verified queries are fine-tuned for efficiency.
- **Resource Management**: Reduces database load and improves execution times.

### Security

- **Risk Mitigation**: Limits exposure to injection attacks and unauthorized data access.
- **Controlled Environment**: Ensures queries only perform intended operations.

## Understanding the Implementation

- **System Prompt**: We instruct the assistant to translate English into a MongoDB aggregation pipeline array.
- **Verified Pipelines**: We provide a verified pipeline for a similar query (`What are the best 1337 movies`) within the `[verified pipelines]` section. This serves as a template.
- **User Input**: The user asks, `What are the best 5 movies?`
- **Assistant's Task**: Use the verified pipeline to construct a new pipeline that answers the user's question, ensuring it adheres to the response criteria.

---

## Integrating Verified Queries with Azure OpenAI and MongoDB

By leveraging Azure OpenAI's language models, we can create an assistant that translates natural language into MongoDB aggregation pipelines using verified queries. Here's how it works:

```python
from openai import AzureOpenAI
import json

# Set up Azure OpenAI credentials
azure_endpoint = "https://<your-resource-name>.openai.azure.com"
azure_deployment = "gpt-4o"
api_key = "<your-api-key>"
api_version = "2024-10-21"

az_client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    api_key=api_key
)

user_input = 'What are the best 5 movies?'

messages = [
    {
        "role": "system",
        "content": """
You are a helpful assistant that translates English to MongoDB Aggregation Pipeline array. Only respond with the array, ready to use.
"""
    },
    {
        "role": "user",
        "content": f"""
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
    },
    {
        '$addFields': {
            'combined_rating': {
                '$avg': [
                    '$imdb_rating',
                    '$tomatoes_viewer_rating'
                ]
            }
        }
    },
    {
        '$sort': {
            'combined_rating': -1
        }
    },
    {
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
"""
    }
]

response = az_client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    response_format={"type": "json_object"}
)

ai_msg = json.loads(response.choices[0].message.content)
print(ai_msg['pipeline'])
```

**Output:**

```json
[
    {
        "$project": {
            "title": 1,
            "imdb_rating": "$imdb.rating",
            "tomatoes_viewer_rating": "$tomatoes.viewer.rating"
        }
    },
    {
        "$addFields": {
            "combined_rating": {
                "$avg": [
                    "$imdb_rating",
                    "$tomatoes_viewer_rating"
                ]
            }
        }
    },
    {
        "$sort": {
            "combined_rating": -1
        }
    },
    {
        "$limit": 5
    }
]
```

---

## Understanding the Implementation

In the code above:

- **System Prompt**: We instruct the assistant to translate English into a MongoDB aggregation pipeline array.
- **Verified Pipelines**: We provide a verified pipeline for a similar query (`What are the best 1337 movies`) within the `[verified pipelines]` section. This serves as a template.
- **User Input**: The user asks, `What are the best 5 movies?`
- **Assistant's Task**: Use the verified pipeline to construct a new pipeline that answers the user's question, ensuring it adheres to the response criteria.

By adjusting the `$limit` stage from `1337` to `5`, the assistant provides an optimized and verified pipeline tailored to the user's request.

---

## The Importance of Verified Queries

Using verified queries ensures:

### Consistency

- **Reliable Results**: Pre-tested queries produce expected outcomes.
- **Standardization**: Adheres to established query patterns within your applications.

### Generalization

- **Adaptability**: The assistant can handle variations of similar queries effectively.
- **Scalability**: New queries can be generated based on existing verified templates.

### Performance

- **Optimization**: Verified queries are fine-tuned for efficiency.
- **Resource Management**: Reduces database load and improves execution times.

### Security

- **Risk Mitigation**: Limits exposure to injection attacks and unauthorized data access.
- **Controlled Environment**: Ensures queries only perform intended operations.

---

## Optimizing Aggregation Stages in MongoDB

Optimization is key to performance in MongoDB's aggregation framework. Here's how each stage in the pipeline contributes:

1. **$project**

   - **Purpose**: Includes or excludes specific fields from documents.
   - **Optimization**: Reduces data size early in the pipeline, improving subsequent stage performance.

2. **$addFields**

   - **Purpose**: Adds new fields or resets existing fields with computed values.
   - **Optimization**: Calculates necessary data within the pipeline, avoiding extra queries.

3. **$sort**

   - **Purpose**: Orders documents based on specified fields.
   - **Optimization**: Efficient sorting mechanisms enhance performance, especially with proper indexing.

4. **$limit**

   - **Purpose**: Restricts the number of documents passing through the pipeline.
   - **Optimization**: Minimizes data processed in later stages, conserving resources.

By carefully structuring these stages, you can create pipelines that are both efficient and effective.

---

Integrating natural language interfaces with verified queries allows users to interact with data intuitively while maintaining high standards of performance and security. By leveraging optimized aggregation pipelines in MongoDB, you ensure that your applications are scalable and responsive.

**Key Takeaways:**

- **Verified Queries Enhance Reliability**: They provide a foundation for consistent and secure data retrieval.
- **Optimized Pipelines Improve Performance**: Thoughtful construction of aggregation stages leads to efficient data processing.
- **Natural Language Integration Simplifies Interaction**: Users can query data without needing in-depth knowledge of query languages.

---
## Practical Use Cases

### Data Analysis

- **Empowering Analysts**: Allows data analysts to extract insights without writing complex queries, focusing on interpretation rather than data retrieval.
- **Ad-Hoc Reporting**: Facilitates quick generation of reports based on spontaneous queries from stakeholders.

### Customer Service

- **Responsive Support**: Enables customer service agents to retrieve customer information and history instantly, improving service quality.
- **Personalized Interactions**: Access to real-time data allows for tailored solutions to customer needs.

### Business Intelligence

- **Executive Access**: Provides leaders with the ability to query key performance indicators directly, aiding strategic decisions.
- **Market Trend Analysis**: Simplifies the process of analyzing market data, helping businesses stay competitive.

### DevOps and Development Teams

- **Codebase Integrity**: Ensures only optimized and approved queries are added to the codebase, enhancing application performance.
- **Developer Efficiency**: Reduces the time developers spend writing and testing queries, allowing them to focus on core functionality.

## Applications in DevOps and Codebase Management

### Enforcing Query Standards

- **Code Quality Assurance**: DevOps teams can enforce standardized query shapes within the codebase, ensuring consistency and reliability.
- **Automated Compliance Checks**: Integrate tools that validate queries against approved patterns before they are merged into the codebase.

### Continuous Integration and Deployment (CI/CD)

- **Streamlined Development**: Incorporating query validation into CI/CD pipelines catches potential issues early, reducing deployment risks.
- **Rollback Mechanisms**: Enables quick reversion of non-compliant code changes, maintaining system stability.

### Enhanced Security Protocols

- **Access Control Enforcement**: Limits database operations to predefined query shapes, preventing unauthorized actions.
- **Audit Trails**: Keeps detailed logs of query usage, aiding in monitoring and compliance efforts.
