import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from graphene.test import Client
from config.schema import schema

client = Client(schema)

query = """
    query {
        allPosts {
            id
            content
            author {
                username
            }
        }
    }
"""

result = client.execute(query)
print(json.dumps(result, indent=2))
