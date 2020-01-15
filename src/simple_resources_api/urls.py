"""template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include

from users.urls import register_urlpatterns, auth_urlpatterns, users_urlpatterns
from resources.urls import user_quota_urlpatterns, resources_urlpatterns
from .schema import schema_view

urlpatterns = [
    url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^api/v1/register', include(register_urlpatterns)),
    url(r'^api/v1/login', include(auth_urlpatterns)),
    url(r'^api/v1/users', include(users_urlpatterns)),
    url(r'^api/v1/quotas', include(user_quota_urlpatterns)),
    url(r'^api/v1/resources', include(resources_urlpatterns)),
]
