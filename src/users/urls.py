from django.urls import path

from .views import RegisterViewSet, AuthViewSet, UserViewSet, MeUserViewSet

register_urlpatterns = [
    path(r'', RegisterViewSet.as_view({'post': 'create'}), name='register')
]

auth_urlpatterns = [
    path(r'', AuthViewSet.as_view({'post': 'obtain_token'}), name='login')
]

users_urlpatterns = [
    path(r'', UserViewSet.as_view({'post': 'create', 'get': 'list'}), name='users'),
    path(r'/<int:pk>', UserViewSet.as_view({'get': 'retrieve',
                                            'delete': 'destroy',
                                            'put': 'update',
                                            'patch': 'partial_update'}), name='user'),
    path(r'/me', MeUserViewSet.as_view({'get': 'retrieve',
                                        'put': 'update',
                                        'patch': 'partial_update'}), name='me-user'),
]
