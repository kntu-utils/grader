from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

import uuid


class Participation(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('myauth.User', on_delete=models.CASCADE, related_name='participants')
    identifier = models.CharField(max_length=255)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('course', 'identifier'),
                                    name='problems_participation_course_identifier_uniq'),
        )


class Course(models.Model):
    title = models.CharField(max_length=255)
    users = models.ManyToManyField('myauth.User', related_name='courses', through=Participation)
    password = models.CharField(max_length=255, blank=True, null=True)
    professor = models.CharField(max_length=255, blank=True, null=True)
    identifier_field = models.CharField(max_length=255, blank=True, null=True)
    identifier_text = models.CharField(max_length=255, blank=True)


class ProblemSet(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='problem_sets')
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    base_content = HTMLField()


class Problem(models.Model):
    title = models.CharField(max_length=255)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE, related_name='problems')
    score = models.PositiveIntegerField()
    content = HTMLField()
    template = models.FilePathField(path=settings.TESTERS_TEMPLATE_DIR, recursive=False, allow_files=False, allow_folders=True)
    gitlab_id = models.BigIntegerField(unique=True, blank=True)
    gitlab_path = models.CharField(max_length=255, blank=True)


class Repository(models.Model):
    gitlab_path = models.CharField(max_length=255, blank=True)
    gitlab_id = models.BigIntegerField(unique=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='repositories')
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='repositories')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Submission(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', _('created')
        PENDING = 'PENDING', _('pending')
        RUNNING = 'RUNNING', _('running')
        JUDGED = 'JUDGED', _('judged')
        CANCELLED = 'CANCELLED', _('cancelled')

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='submissions')
    commit_sha = models.CharField(max_length=40)
    pipeline_id = models.BigIntegerField()
    public_log = models.TextField()
    private_log = models.TextField()
    score_ratio = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('repository', 'commit_sha'),
                                    name='problems_submission_repository_commit_sha_uniq'),
        )
