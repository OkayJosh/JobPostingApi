"""
The Talentpool Interface views module
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from talentpool.application.services import (UserService, JobAdvertService,
                                             JobApplicationService)
from talentpool.interface.swagger_docs import (user_login_schema,
                                               user_logout_schema,
                                               job_advert_list_schema,
                                               job_advert_detail_schema,
                                               job_advert_update_schema,
                                               job_advert_delete_schema,
                                               job_advert_publish_schema,
                                               job_advert_unpublish_schema,
                                               job_application_delete_schema,
                                               job_application_detail_schema,
                                               job_application_create_schema,
                                               job_application_list_schema, user_signup_schema,
                                               job_advert_create_schema)


class UserAPIView(APIView):
    """
    The User onboarding View
    """
    permission_classes = []

    @user_signup_schema
    def post(self, request) -> Response:
        """
        The Signup
        :param request:
        :return Response:
        """
        _, token = UserService.create_user(request.data)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class UserAuthenticationAPIView(APIView):
    """
    The User Authentication View
    """
    permission_classes = []

    @user_login_schema
    def post(self, request) -> Response:
        """
        The Login
        :param request:
        :return Response:
        """
        _, token = UserService.login_user(request.data)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


    @user_logout_schema
    def delete(self, request) -> Response:
        """
        The logout
        :param request:
        :return Response:
        """
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobAdvertListAPIView(APIView):
    """
    The Job Advert List API
    """
    permission_classes = []

    @job_advert_list_schema
    def get(self, request) -> Response:
        """
        The list of Job adverts in the DB
        What are the challenges of making this unauthenticated
        :param request:
        :return Response:
        """
        response = JobAdvertService.list_job_adverts(request)
        return response


class JobAdvertDetailAPIView(APIView):
    """
    The Job Advert Detail API
    """
    permission_classes = [IsAuthenticated]

    @job_advert_detail_schema
    def get(self, request, job_advert_id):
        """
        Retrieves the detail of a job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        job_advert = JobAdvertService.get_job_advert(job_advert_id)
        return Response(job_advert)

    @job_advert_create_schema
    def post(self, request):
        """
        Create a job advert
        :param request:
        :return Response:
        """
        job_advert = JobAdvertService.create_job_advert(request.data)
        return Response(job_advert)

    @job_advert_update_schema
    def put(self, request, job_advert_id):
        """
        Updates the detail of a job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        job_advert = JobAdvertService.update_job_advert(job_advert_id, request.data)
        return Response(job_advert)

    @job_advert_delete_schema
    def delete(self, request, job_advert_id) -> Response:
        """
        Deletes the job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        JobAdvertService.delete_job_advert(job_advert_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobAdvertPublishAPIView(APIView):
    """
    The Job Advert Publish API
    """
    permission_classes = [IsAuthenticated]

    @job_advert_publish_schema
    def post(self, request, job_advert_id) -> Response:
        """
        Publishes a job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        JobAdvertService.publish_job_advert(job_advert_id)
        return Response(status=status.HTTP_200_OK)

    @job_advert_unpublish_schema
    def delete(self, request, job_advert_id) -> Response:
        """
        Unpublishes a job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        JobAdvertService.unpublish_job_advert(job_advert_id)
        return Response(status=status.HTTP_200_OK)


class JobApplicationListAPIView(APIView):
    """
    The JobApplicationListAPIView
    """
    permission_classes = [IsAuthenticated]

    @job_application_create_schema
    def post(self, request) -> Response:
        """
        Submit a job job_application for a job advert
        :param request:
        :return Response:
        """
        job_application = JobApplicationService.create_job_application(request.data)
        return Response(job_application, status=status.HTTP_201_CREATED)

    @job_application_list_schema
    def get(self, request, job_advert_id) -> Response:
        """
        Get Job Applications for a job advert
        :param request:
        :param job_advert_id:
        :return Response:
        """
        job_applications = JobApplicationService.get_job_applications(job_advert_id)
        return Response(job_applications)


class JobApplicationDetailAPIView(APIView):
    """
    Job Application Detail API
    """
    permission_classes = [IsAuthenticated]

    @job_application_detail_schema
    def get(self, request, job_application_id) -> Response:
        """
        Get the detail of a job application
        :param request:
        :param job_application_id:
        :return Response:
        """
        job_application = JobApplicationService.get_job_application(job_application_id)
        return Response(job_application)

    @job_application_delete_schema
    def delete(self, request, job_application_id) -> Response:
        """
        Delete the job application
        :param request:
        :param job_application_id:
        :return Response:
        """
        JobApplicationService.delete_job_application(job_application_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
