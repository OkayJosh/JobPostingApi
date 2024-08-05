"""
Talentpool Interface Serializers Module
"""

from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from talentpool.models import User, JobAdvert, JobApplication


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        return user, token

    def save(self, **kwargs):
        """
        The inspiration was from rest_framework/serializers.py
        :param kwargs:
        :return:
        """
        token = None
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            # i include token here only
            self.instance, token = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance, token


class JobAdvertSerializer(serializers.ModelSerializer):
    """
    JobAdvertSerializer
    """
    applicant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = JobAdvert
        fields = ['uuid', 'title', 'company_name',
                  'employment_type', 'experience_level', 'description', 'location',
                  'job_description', 'is_published', 'applicant_count',
                  'publish_at', 'is_scheduled']

    def validate_publish_at(self, value):
        """
        Validate publish_at
        NOTE: To schedule a post just make publish_at not null
        A Time in the Future (atleast) 5 minutes from now
        :param value:
        :return:
        """
        if value is not None:
            min_publish_time = timezone.now() + timezone.timedelta(minutes=5)
            if value < min_publish_time:
                raise serializers.ValidationError(
                    "Publish time must be at least five minutes into the future."
                )
        return value


class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Job Application Serializer
    """
    class Meta:
        model = JobApplication
        fields = ['uuid', 'job_advert', 'first_name',
                  'last_name', 'email', 'phone', 'linkedin_profile', 'github_profile',
                  'website', 'years_of_experience', 'cover_letter']

    def validate_job_advert(self, value):
        """
        Validate job_advert, you can only apply to a job that is_published
        :param value:
        :return:
        """
        job_advert = JobAdvert.objects.get(uuid=value.job_advert)
        if job_advert.is_published is not True:
            raise ValidationError("You cannot apply for a job that is not published.")
        return value
