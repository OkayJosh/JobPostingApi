"""
The Service classes module
"""

from celery import shared_task
from django.contrib.auth import authenticate
# Django Import
from django.db.models import Count
from django.utils import timezone
from django.views.decorators.debug import sensitive_variables
from rest_framework.authtoken.models import Token

# Third-party imports
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from talentpool.interface.serializers import (UserSerializer, JobAdvertSerializer,
                                              JobApplicationSerializer)
from talentpool.models import User, JobAdvert, JobApplication


class JobAdvertPagination(PageNumberPagination):
    """
    Job Advert Pagination class
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserService:
    """
    The user service
    """

    @staticmethod
    @sensitive_variables("credentials")
    def authenticate(**credentials) -> tuple[User, Token]:
        """
        Authenticate User
        :param credentials:
        :return tuple[User, Token]:
        """
        user = authenticate(**credentials)
        token, _ = Token.objects.get_or_create(user=user)
        return user, token

    @staticmethod
    def create_user(data) -> tuple[User, Token]:
        """
        Create the user
        :param data:
        :return: tuple[User, Token]
        """
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user, token = serializer.save()
            return user, token
        raise ValidationError(serializer.errors)

    @staticmethod
    def login_user(data) -> tuple[User, Token]:
        """
        Login the user
        :param data:
        :return: tuple[User, Token]
        """
        try:
            # Extract and sanitize username and password from QueryDict
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                raise ValidationError("Username and password are required.")

            user, token = UserService.authenticate(
                username=username,
                password=password
            )
            return user, token
        except Exception as exc:
            raise ValidationError(exc.args[0]) from exc


class JobAdvertService:
    """
    The Job Advert service
    """

    @staticmethod
    def create_job_advert(data) -> JobAdvert:
        """
        Create the job advert +
        Schedule the job advert to be published at a later time
        :param data:
        :return JobAdvert:
        """
        serializer = JobAdvertSerializer(data=data)
        if serializer.is_valid():
            job_advert = serializer.save()
            return job_advert
        raise ValidationError(serializer.errors)

    @staticmethod
    def update_job_advert(job_advert_id, data) -> JobAdvert:
        """
        Update the job advert
        :param job_advert_id:
        :param data:
        :return:
        """
        try:
            job_advert = JobAdvert.objects.get(uuid=job_advert_id)
        except JobAdvert.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

        serializer = JobAdvertSerializer(job_advert, data=data, partial=True)
        if serializer.is_valid():
            job_advert = serializer.save()
            return job_advert
        raise ValidationError(serializer.errors)

    @staticmethod
    def delete_job_advert(job_advert_id) -> None:
        """
        Delete the job advert
        NOTE: we cannot delete a job advert unless it is unpublished
        :param job_advert_id:
        :return:
        """
        try:
            job_advert = JobAdvert.objects.get(uuid=job_advert_id)
            if not job_advert.is_published:
                job_advert.delete()
            else:
                raise ValidationError("Published job adverts cannot be deleted")
        except JobAdvert.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

    @staticmethod
    def list_job_adverts(params) -> Response:
        """
        List job adverts
        :param params:
        :return:
        """
        queryset = JobAdvert.objects.annotate(applicant_count=Count('applications')).order_by(
            '-is_published', '-applicant_count', 'created'
        )
        paginator = JobAdvertPagination()
        result_page = paginator.paginate_queryset(queryset, params)
        serializer = JobAdvertSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    def get_job_advert(job_advert_id) -> JobAdvert:
        """
        Get the job advert
        :param job_advert_id:
        :return:
        """
        try:
            job_advert = JobAdvert.objects.get(uuid=job_advert_id)
            serializer = JobAdvertSerializer(job_advert)
            return serializer.data
        except JobAdvert.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

    @staticmethod
    def publish_job_advert(job_advert_id) -> JobAdvert:
        """
        Publish the job advert
        :param job_advert_id:
        :return:
        """
        try:
            job_advert = JobAdvert.objects.get(uuid=job_advert_id)
            job_advert.is_published = True
            job_advert.save()
            serializer = JobAdvertSerializer(job_advert)
            return serializer.data
        except JobAdvert.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

    @staticmethod
    @shared_task
    def publish_scheduled_job_adverts():
        """
        Publish Scheduled Job Advert Task
        :return:
        """
        now = timezone.now()
        job_adverts = JobAdvert.objects.filter(
            is_scheduled=True,
            publish_at__lte=now,
            is_published=False
        )

        for job_advert in job_adverts:
            job_advert.is_published = True
            job_advert.is_scheduled = False
            job_advert.save()

    @staticmethod
    def unpublish_job_advert(job_advert_id) -> JobAdvert:
        """
        Unpublish the job advert
        :param job_advert_id:
        :return:
        """
        try:
            job_advert = JobAdvert.objects.get(uuid=job_advert_id)
            job_advert.is_published = False
            job_advert.save()
            serializer = JobAdvertSerializer(job_advert)
            return serializer.data
        except JobAdvert.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc


class JobApplicationService:
    """
    The Job Application service
    """

    @staticmethod
    def create_job_application(data) -> JobApplication:
        """
        Create the job application
        :param data:
        :return:
        """
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            job_application = serializer.save()
            return job_application
        raise ValidationError(serializer.errors)

    @staticmethod
    def get_job_applications(job_advert_id) -> [JobApplication]:
        """
        Get the job applications
        :param job_advert_id:
        :return:
        """
        try:
            job_applications = JobApplication.objects.filter(job_advert_id=job_advert_id)
            serializer = JobApplicationSerializer(job_applications, many=True)
            return serializer.data
        except JobApplication.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

    @staticmethod
    def get_job_application(job_application_id) -> JobApplication:
        """
        Get the job application
        :param job_application_id:
        :return:
        """
        try:
            job_application = JobApplication.objects.get(uuid=job_application_id)
            serializer = JobApplicationSerializer(job_application)
            return serializer.data
        except JobApplication.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc

    @staticmethod
    def delete_job_application(job_application_id) -> None:
        """
        Delete the job application
        :param job_application_id:
        :return:
        """
        try:
            job_application = JobApplication.objects.get(uuid=job_application_id)
            job_application.delete()
        except JobApplication.DoesNotExist as exc:
            raise ValidationError({'detail': exc.args[0]}) from exc
