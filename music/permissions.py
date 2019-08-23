import requests

from django.conf import settings

from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        access_token = request.META.get('HTTP_AUTHORIZATION', None)
        url = settings.HANLIGHT_BASE_URL + "user"

        headers = {
            'access_token': access_token
        }
        res = requests.get(url, headers=headers)

        return True if res.status_code == 200 else False
