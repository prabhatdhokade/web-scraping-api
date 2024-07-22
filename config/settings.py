import redis

API_TOKEN = "Prabhat@2024"

# Redis client for caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)
