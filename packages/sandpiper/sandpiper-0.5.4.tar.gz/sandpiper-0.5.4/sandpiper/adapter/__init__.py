import re

try:
    from .dynamodb import DynamoDB
except ImportError as e:
    if not re.search("No module named 'boto3'", str(e)):
        raise e

from .inmemory import InMemory
