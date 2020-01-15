from django.urls import path

from .views import UserQuotaViewSet, ResourcesViewSet

user_quota_urlpatterns = [
    path(r'', UserQuotaViewSet.as_view({'get': 'list'}), name='users-quota'),
    path(r'/<int:pk>', UserQuotaViewSet.as_view({'get': 'retrieve',
                                                 'put': 'update',
                                                 'patch': 'partial_update'}), name='user-quota')
]

resources_urlpatterns = [
    path(r'', ResourcesViewSet.as_view({'post': 'create', 'get': 'list'}), name='resources'),
    path(r'/<int:pk>', ResourcesViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='resource')
]
