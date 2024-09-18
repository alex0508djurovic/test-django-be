import hashlib
from django.core.cache import cache
from functools import wraps
from django.http import JsonResponse

def cache_response(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        cache_key = get_cache_key(request)
        if cache_key:
            cached_response = cache.get(cache_key)
            if cached_response:
                return JsonResponse(cached_response, safe=False)
        
        response = view_func(request, *args, **kwargs)
        if cache_key and response.status_code == 200:
            cache.set(cache_key, response.data, timeout=7200)
        return response

    def get_cache_key(request):
        if request.method != 'POST':
            return None
        path = request.path
        params = request.body.decode('utf-8')
        key = f"{path}?{params}"
        return hashlib.md5(key.encode('utf-8')).hexdigest()
    return _wrapped_view
