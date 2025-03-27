from backend.redis_client import redis_client
from backend.models import Service
import json

CACHE_EXPIRY = 60 * 30  # Cache for 30minutes

def get_cached_services():
    """Fetch services from Redis or database."""
    cached_services = redis_client.get("services_list")
    if cached_services:
        print("✅ Cache HIT: Returning cached data")
        return json.loads(cached_services)
    
    print("❌ Cache MISS: Fetching from DB...")

    services = Service.query.all()
    services_data = [{"id": s.id, "name": s.name, "base_price": s.base_price, "time_required":s.time_required} for s in services]

    redis_client.setex("services_list", CACHE_EXPIRY, json.dumps(services_data))
    print("🔄 Cache Updated!")
    return services_data

def clear_service_cache():
    """Invalidate cached services list."""
    print("❌ Clearing service cache...")
    redis_client.delete("services_list")
