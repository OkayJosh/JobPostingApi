""" Talentpool tests """
from django.urls import reverse
from django.utils import timezone

import pytest

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient

from talentpool.models import JobAdvert, JobApplication
from talentpool.application.services import (
    JobAdvertService, JobApplicationService)
from tests.talentpool.factories import UserFactory, JobAdvertFactory, JobApplicationFactory


@pytest.mark.django_db
class TestJobAdvertService:
    """
    Test for Job Advert Service
    """

    def setup_method(self):
        """
        Method setup
        :return:
        """
        self.client = APIClient()  # pylint: disable=W0201
        self.user = UserFactory()  # pylint: disable=W0201
        self.job_advert = JobAdvertFactory.create(is_published=True)  # pylint: disable=W0201

    def test_create_job_advert(self):
        """
        Create Job advert from service directly
        :return:
        """
        data = {
            'title': 'New Job',
            'company_name': 'New Company',
            'employment_type': 'full_time',
            'experience_level': 'entry',
            'description': 'Job description',
            'location': 'Location',
            'job_description': 'Detailed job description',
            'is_published': True
        }
        job_advert = JobAdvertService.create_job_advert(data)
        assert job_advert.title == 'New Job'
        assert job_advert.is_published

    def test_update_job_advert(self):
        """
        Update Job Advert from Service directly
        :return:
        """
        data = {
            'title': 'Updated Job Title'
        }
        updated_job_advert = JobAdvertService.update_job_advert(self.job_advert.uuid, data)
        assert updated_job_advert.title == 'Updated Job Title'

    def test_delete_job_advert_for_publish_post(self):
        """
        Published Job Advert should raise Validation Error
        When deleted
        :return:
        """

        with pytest.raises(ValidationError):
            JobAdvertService.delete_job_advert(self.job_advert.uuid)

    def test_delete_job_advert_for_unpublish_post(self):
        """
        UnPublished Job Advert can be deleted
        :return:
        """
        JobAdvertService.unpublish_job_advert(self.job_advert.uuid)
        # need to get updated data from db: i think job advert is cached in memory
        self.job_advert.refresh_from_db()
        # Returning None indicate that the job advert has been deleted
        assert JobAdvertService.delete_job_advert(self.job_advert.uuid) is None

    def test_publish_job_advert(self):
        """
        Publish Job Advert from service directly
        :return:
        """
        JobAdvertService.publish_job_advert(self.job_advert.uuid)
        job_advert = JobAdvert.objects.get(uuid=self.job_advert.uuid)
        assert job_advert.is_published

    def test_unpublish_job_advert(self):
        """
        Unpublish Job Advert from Service class
        :return:
        """
        JobAdvertService.unpublish_job_advert(self.job_advert.uuid)
        job_advert = JobAdvert.objects.get(uuid=self.job_advert.uuid)
        assert not job_advert.is_published

    def test_list_job_adverts(self):
        """
        You should be able to see the list of job advert even while a guest user
        :return:
        """
        response = self.client.get(reverse('job-advert-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_get_job_advert_details_without_authentication(self):
        """
        Returns the detail of published job advert
        NOTE: This endpoint require authentication
        :return:
        """
        response = self.client.get(
            reverse('job-advert-detail', args=[self.job_advert.uuid])
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_job_advert_details_with_authentication(self):
        """
        Returns the detail of published job advert
        NOTE: This endpoint require authentication
        :return:
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('job-advert-detail', args=[self.job_advert.uuid])
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == self.job_advert.title

    def test_schedule_job_advert(self):
        """
        Test that you can schedule a job advert
        NOTE: This works without authentication
        :return:
        """
        future_publish_time = timezone.now() + timezone.timedelta(days=1)
        data = {
            'title': 'Schedule Job',
            'company_name': 'New Company',
            'employment_type': 'full_time',
            'experience_level': 'entry',
            'description': 'Job description',
            'location': 'Location',
            'job_description': 'Detailed job description',
            'publish_at': future_publish_time,
            'is_scheduled': True
        }
        job_advert = JobAdvertService.create_job_advert(data)
        assert job_advert.publish_at == future_publish_time
        assert job_advert.is_scheduled
        assert job_advert.is_published is False


@pytest.mark.django_db
class TestJobApplicationService:
    """
    Test Job Application Service
    """

    def setup_method(self):
        """
        Method setup
        :return:
        """
        self.client = APIClient()  # pylint: disable=W0201
        self.user = UserFactory()  # pylint: disable=W0201
        self.job_advert = JobAdvertFactory.create(is_published=True)  # pylint: disable=W0201

    def test_create_job_application(self):
        """
        Test Job Application for a Job Advert
        :return:
        """
        data = {
            'job_advert': self.job_advert.uuid,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'linkedin_profile': 'https://linkedin.com/in/johndoe',
            'github_profile': 'https://github.com/johndoe',
            'website': 'https://johndoe.com',
            'years_of_experience': '1-2',
            'cover_letter': 'Cover letter content'
        }
        job_application = JobApplicationService.create_job_application(data)
        assert job_application.first_name == 'John'

    def test_get_job_applications_unauthenticated(self):
        """
        Tes that i can not get all job application associated with a
        when unauthenticated
        Job Advert
        :return:
        """
        JobApplicationFactory.create(job_advert=self.job_advert)
        response = self.client.get(reverse(
            'job-application', args=[self.job_advert.uuid])
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_job_applications_authenticated(self):
        """
        Tes that i can get all job application associated with a
        when authenticated
        Job Advert
        :return:
        """
        self.client.force_authenticate(user=self.user)
        JobApplicationFactory.create(job_advert=self.job_advert)
        response = self.client.get(reverse(
            'job-application', args=[self.job_advert.uuid])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_get_job_application_unauthenticated(self):
        """
        Test that i am not able to get Job application detail when a guest user
        :return:
        """
        job_application = JobApplicationFactory.create(job_advert=self.job_advert)
        response = self.client.get(
            reverse('job-application-detail', args=[job_application.uuid])
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_job_application_authenticated(self):
        """
        Test that i am not able to get Job application detail when a guest user
        :return:
        """
        self.client.force_authenticate(user=self.user)
        job_application = JobApplicationFactory.create(job_advert=self.job_advert)
        response = self.client.get(
            reverse('job-application-detail', args=[job_application.uuid])
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == job_application.first_name

    def test_delete_job_application(self):
        """
        Test that application is deleted and
        when looked for after the deletion, would not be found in the database
        NOTE: this deletion is not done from the API: so it works without authentication
        :return:
        """
        job_application = JobApplicationFactory.create(job_advert=self.job_advert)
        JobApplicationService.delete_job_application(job_application.uuid)
        with pytest.raises(JobApplication.DoesNotExist):
            JobApplication.objects.get(uuid=job_application.uuid)


@pytest.mark.django_db
class TestUserAPI:
    """
    Test User API
    """

    @pytest.fixture
    def client(self):
        """
        API Client fixture
        :return:
        """
        return APIClient()

    @pytest.fixture
    def user(self):
        """
        user fixture
        :return:
        """
        return UserFactory.create(username='testuser', password='testpass123')

    def test_user_login(self, client, user):
        """
        Test user login
        :param client:
        :param user:
        :return:
        """
        url = reverse('user-login')
        data = {
            'username': user.username,
            'password': 'testpass123'
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_user_logout(self, client, user):
        """
        Test user Logout
        :param client:
        :param user:
        :return:
        """
        token = Token.objects.get(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('user-login')
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Token.objects.filter(user=user).exists()
