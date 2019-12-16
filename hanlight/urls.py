"""hanlight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='HanlightMusic API',
        default_version='v1',
        description='HanlightMusic API Document',
        terms_of_service='',
        contact=openapi.Contact(email='mystar09070907@gmail.com'),
        license=openapi.License(name='Hanlight License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)


urlpatterns = [
    path('api/', include('hanlight.routes')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__', include(debug_toolbar.urls)))

    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]