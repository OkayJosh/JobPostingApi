"""
Talentpool models module
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    """
    Hold users information
    NOTE:
        1. I reuse the Django AbstractUser Class,
            some extra fields and functionality might be present
            is that what we want?
        2. One of the reasons I used django extensions package was due to TimestampedModel
        3. I use uuid because id ont want the id to expose the user count in the db
        4. Username/email and Password are in the AbstractUser Class
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)


class JobAdvert(TimeStampedModel):
    """
    The JobAdvert Model
    """
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
        ('part_time', 'Part Time')
    ]

    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid-level'),
        ('senior', 'Senior')
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # Why do we have to keep description and job_description separate?
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVELS)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_description = models.TextField()
    is_published = models.BooleanField(default=False)

    publish_at = models.DateTimeField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.publish_at and self.publish_at > timezone.now():
    #         self.is_published = True
    #         self.is_scheduled = True
    #     else:
    #         self.is_published = True
    #         self.is_scheduled = False
    #     super().save(*args, **kwargs)


class JobApplication(TimeStampedModel):
    """
    The JobApplication Model
    """
    YEARS_OF_EXPERIENCE = [
        ('0-1', '0 - 1'),
        ('1-2', '1 - 2'),
        ('3-4', '3 - 4'),
        ('5-6', '5 - 6'),
        ('7+', '7 and above')
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    job_advert = models.ForeignKey(
        JobAdvert, on_delete=models.CASCADE, related_name='applications'
    )
    # why do we have to keep first_name, last_name and email here when we can
    # get it from the users model
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin_profile = models.URLField()
    github_profile = models.URLField()
    website = models.URLField(blank=True, null=True)
    years_of_experience = models.CharField(max_length=10, choices=YEARS_OF_EXPERIENCE)
    cover_letter = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} for {self.job_advert.title}"
