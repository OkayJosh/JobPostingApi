"""
Swagger docs Module
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from talentpool.interface.serializers import (UserSerializer,
                                              JobAdvertSerializer,
                                              JobApplicationSerializer)

user_login_schema = swagger_auto_schema(
    operation_description="User login",
    request_body=UserSerializer,
    responses={201: openapi.Response('Token', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='Auth Token'),
        }
    ))}
)

user_signup_schema = swagger_auto_schema(
    operation_description="User Signup",
    request_body=UserSerializer,
    responses={201: openapi.Response('Token', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='Auth Token'),
        }
    ))}
)

user_logout_schema = swagger_auto_schema(
    operation_description="User logout",
    responses={204: 'No Content'}
)

job_advert_list_schema = swagger_auto_schema(
    operation_description="The list of Job adverts in the DB",
    responses={
        200: openapi.Response('List of Job Adverts',
                              JobAdvertSerializer(many=True))
    }
)

job_advert_detail_schema = swagger_auto_schema(
    operation_description="Retrieves the detail of a job advert",
    responses={
        200: openapi.Response('Job Advert Detail',
                              JobAdvertSerializer)
    }
)

job_advert_create_schema = swagger_auto_schema(
    operation_description="Create a job advert",
    request_body=JobAdvertSerializer,
    responses={
        201: openapi.Response('Create Job Advert',
                              JobAdvertSerializer)
    }
)

job_advert_update_schema = swagger_auto_schema(
    operation_description="Updates the detail of a job advert",
    request_body=JobAdvertSerializer,
    responses={
        200: openapi.Response('Updated Job Advert',
                              JobAdvertSerializer)
    }
)

job_advert_delete_schema = swagger_auto_schema(
    operation_description="Deletes the job advert",
    responses={204: 'No Content'}
)

job_advert_publish_schema = swagger_auto_schema(
    operation_description="Publishes a job advert",
    responses={200: 'Job advert published'}
)

job_advert_unpublish_schema = swagger_auto_schema(
    operation_description="Unpublishes a job advert",
    responses={200: 'Job advert unpublished'}
)

job_application_list_schema = swagger_auto_schema(
    operation_description="Get Job Applications for a job advert",
    responses={
        200: openapi.Response('List of Job Applications',
                              JobApplicationSerializer(many=True))
    }
)

job_application_create_schema = swagger_auto_schema(
    operation_description="Submit a job application for a job advert",
    request_body=JobApplicationSerializer,
    responses={
        201: openapi.Response('Created Job Application',
                              JobApplicationSerializer)
    }
)

job_application_detail_schema = swagger_auto_schema(
    operation_description="Get the detail of a job application",
    responses={
        200: openapi.Response('Job Application Detail',
                              JobApplicationSerializer)
    }
)

job_application_delete_schema = swagger_auto_schema(
    operation_description="Delete the job application",
    responses={204: 'No Content'}
)
