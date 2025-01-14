from http.client import HTTPException
from django.conf import settings
from .models import Permission, RUser
from django.http import HttpResponse
import jwt
from django.http import JsonResponse


def get_current_user(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=401)

    try:
        # Decode the access token
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = RUser .objects.get(id=user_id)  #user retrieving
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Access token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid access token'}, status=401)
    except RUser .DoesNotExist:
        return JsonResponse({'error': 'User  not found'}, status=404)

    return user  # Return the user object if everything is fine

def role_required(request, permission_name):
    user = get_current_user(request)

    if isinstance(user, JsonResponse):
        return user  # Return the error response directly

    permission = Permission.objects.filter(name=permission_name).first()
    if permission is None:
        return JsonResponse({'error': 'Permission not found'}, status=404)

    if user.role.level > permission.level:  # Changed to '<' for "not enough permissions"
        return JsonResponse({'error': 'Not enough permissions'}, status=403)  # Use 403 Forbidden

    return user  # Return the user object if they have the required permissions