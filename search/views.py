from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .decorators import cache_response
import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

GITHUB_API_URL = 'https://api.github.com/search'

def abstract_search_result(type, item):
    if type not in ['users', 'repositories', 'issues']:
        return {}
    #We are only considering 'users' and 'repositories' on the Frontend
    if type == 'users':
        return {
                'avatar': item.get('avatar_url'),
                'name': item.get('login'),
                'id': item.get('id'),
                'score': item.get('score'),
                'url': item.get('html_url'),
            }
    elif type == 'repositories':
        user = item.get('owner')
        return {
            'id': item.get('id'),
            'name': item.get('name'),
            'isPublic': not item.get('private'),
            'url': item.get('html_url'),
            'description': item.get('description'),
            'createdAt': item.get('created_at'),
            'updatedAt': item.get('updated_at'),
            'size': item.get('size'),
            'language': item.get('language'),
            'owner': user.get('login'),
            'avatar': user.get('avatar_url'),
        }
    else: #For this type (issues), it is not declared on Frontend requirement.
        #This is mock requirement data for issues.(We don't display issues on Frontend)
        user = item.get('user')
        return {
            'id': item.get('id'),
            'url': item.get('url'),
            'owner': user.get('login'),
            'avatar': user.get('avatar_url'),
            'score': item.get('score'),
            'body': item.get('body')
        }

@swagger_auto_schema(
    method='post',
    operation_description="Search GitHub users, repositories, or issues",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['users', 'repositories', 'issues']),
            'search_text': openapi.Schema(type=openapi.TYPE_STRING),
            'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
            'per_page': openapi.Schema(type=openapi.TYPE_INTEGER, default=20),
        },
        required=['search_type', 'search_text'],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Search results",
            examples={
                'application/json': {
                    "total_count": 123,
                    "incomplete_results": False,
                    "items": [
                        {
                            "id": 1,
                            "name": "repository-name",
                            "isPublic": True,
                            "url": "https://github.com/user/repo",
                            "description": "Repository description",
                            "owner": "username",
                            "avatar": "https://avatars.githubusercontent.com/u/12345",
                        }
                    ]
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: "Invalid search type or missing search text",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "GitHub API request failed",
    }
)
@api_view(['POST'])
@cache_response
def search(request):
    search_type = request.data.get('search_type')
    search_text = request.data.get('search_text')
    page = request.data.get('page', 1) 
    per_page = request.data.get('per_page', 20)

    if search_type not in ['users', 'repositories', 'issues']:
        return Response({'error': 'Invalid search type'}, status=status.HTTP_400_BAD_REQUEST)
    if not search_text:
        return Response({'error': 'Search text is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = requests.get(f"{GITHUB_API_URL}/{search_type}", params={
            'q': search_text,
            'page': page,
            'per_page': per_page
        })
        response.raise_for_status() 
    except requests.RequestException as e:
        return Response({'error': f'GitHub API request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = response.json()
    filtered_items = []

    for item in data.get('items', []):
        filtered_items.append(abstract_search_result(search_type, item))
    
    filtered_data = {
        'totalCount': data.get('total_count'),
        'isCompleted': not data.get('incomplete_results'),
        'items': filtered_items,
        'type': search_type
    }

    return Response(filtered_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Cleares Cache, used online REDIS cloud service",
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Sucessfully cleared cache",
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Redis server access failed",
    }
)
@api_view(['POST'])
def clear_cache(request):
    try:
        cache.clear()
        return Response({'message': 'Cache cleared'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'An error occurred while clearing the cache: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)