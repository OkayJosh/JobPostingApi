"""Factory for creating TalentPool Model instances."""
from django.utils import timezone
import factory
from rest_framework.authtoken.models import Token

from talentpool.models import User, JobAdvert, JobApplication


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating TalentPool User Model instances.
    """
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def create_token(user, create, extracted, **kwargs):
        """
        Create Token
        :param create:
        :param extracted:
        :param kwargs:
        :return:
        """
        if not create:
            return
        Token.objects.create(user=user)


class JobAdvertFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating JobAdvert Model instances.
    """
    class Meta:
        model = JobAdvert

    title = factory.Sequence(lambda n: f'Job Title {n}')
    company_name = 'Company'
    employment_type = 'full_time'
    experience_level = 'entry'
    description = 'Job description'
    location = 'Location'
    job_description = 'Detailed job description'
    is_published = True
    publish_at = timezone.now()
    is_scheduled = False


class JobApplicationFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating JobApplication Model instances.
    """
    class Meta:
        model = JobApplication

    job_advert = factory.SubFactory(JobAdvertFactory)
    first_name = 'John'
    last_name = 'Doe'
    email = 'john.doe@example.com'
    phone = '1234567890'
    linkedin_profile = 'https://linkedin.com/in/johndoe'
    github_profile = 'https://github.com/johndoe'
    website = 'https://johndoe.com'
    years_of_experience = '1-2'
    cover_letter = 'Cover letter content'
