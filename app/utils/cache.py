import time
import functools
from flask import current_app
from app import db

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.default_timeout = 300  # 5 minutes
    
    def get(self, key):
        """Get value from cache"""
        if key in self.cache:
            data, expiry = self.cache[key]
            if time.time() < expiry:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value, timeout=None):
        """Set value in cache"""
        if timeout is None:
            timeout = self.default_timeout
        
        expiry = time.time() + timeout
        self.cache[key] = (value, expiry)
    
    def delete(self, key):
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()

# Global cache instance
cache_manager = CacheManager()

def cached(timeout=300, key_prefix='cache'):
    """Decorator for caching function results"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{f.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            cache_manager.set(cache_key, result, timeout)
            
            return result
        return decorated_function
    return decorator

def cache_clear(pattern='*'):
    """Clear cache by pattern"""
    if pattern == '*':
        cache_manager.clear()
    else:
        keys_to_delete = [key for key in cache_manager.cache.keys() if pattern in key]
        for key in keys_to_delete:
            cache_manager.delete(key)

# Cached database queries
@cached(timeout=300)
def get_cached_block_prices():
    """Get block prices with caching"""
    from app.utils.price_fetcher import get_current_prices
    return get_current_prices()

@cached(timeout=600)
def get_popular_house_types(limit=10):
    """Get popular house types with caching"""
    from sqlalchemy import func
    from app.models import Project
    
    return db.session.query(
        Project.house_type,
        func.count(Project.id).label('count')
    ).group_by(Project.house_type)\
     .order_by(func.count(Project.id).desc())\
     .limit(limit).all()

@cached(timeout=3600)
def get_site_statistics():
    """Get site statistics with caching"""
    from app.models import User, Project
    
    return {
        'total_users': User.query.count(),
        'total_projects': Project.query.count(),
        'total_blocks': db.session.query(db.func.sum(Project.total_blocks)).scalar() or 0
    }