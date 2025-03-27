import os
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize Redis Client
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True  # Ensures string values
)
