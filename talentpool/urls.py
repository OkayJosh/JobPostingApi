"""
Module talentpool.urls
"""
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from talentpool.interface.views import (UserAPIView,
                                        JobAdvertListAPIView,
                                        JobAdvertDetailAPIView,
                                        JobAdvertPublishAPIView,
                                        JobApplicationListAPIView,
                                        JobApplicationDetailAPIView, UserAuthenticationAPIView)

SchemaView = get_schema_view(
    openapi.Info(
        title="job_board API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path(
        '',
        SchemaView.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        SchemaView.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path(
        'users/',
        UserAPIView.as_view(),
        name='user-signup'
    ),
    path(
        'users/login',
        UserAuthenticationAPIView.as_view(),
        name='user-login'
    ),
    path(
        'job-adverts/',
        JobAdvertListAPIView.as_view(),
        name='job-advert'
    ),
    # path(
    #     'job-adverts/',
    #     JobAdvertDetailAPIView.as_view(),
    #     name='job-advert-create'
    # ),
    path(
        'job-adverts/<uuid:job_advert_id>/',
        JobAdvertDetailAPIView.as_view(),
        name='job-advert-detail'
    ),
    path(
        'job-adverts/<uuid:job_advert_id>/publish/',
        JobAdvertPublishAPIView.as_view(),
        name='job-advert-publish'
    ),
    path(
        'job-adverts/<uuid:job_advert_id>/applications/',
        JobApplicationListAPIView.as_view(),
        name='job-application'
    ),
    path(
        'job-application/',
        JobApplicationDetailAPIView.as_view(),
        name='job-application-create'
    ),
    path(
        'job-applications/<uuid:job_application_id>/',
        JobApplicationDetailAPIView.as_view(),
        name='job-application-detail'
    )
]
