# Generated by Django 4.2 on 2023-05-04 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pathlib
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('professor', models.CharField(blank=True, max_length=255, null=True)),
                ('identifier_field', models.CharField(blank=True, max_length=255, null=True)),
                ('identifier_text', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='problems.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('score', models.PositiveIntegerField()),
                ('content', tinymce.models.HTMLField()),
                ('template', models.FilePathField(allow_files=False, allow_folders=True, path=pathlib.PurePosixPath('/home/mahdi/Workspace/colleague/kntu-utils/grader/testers/templates'))),
                ('gitlab_id', models.BigIntegerField(blank=True, unique=True)),
                ('gitlab_path', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gitlab_path', models.CharField(blank=True, max_length=255)),
                ('gitlab_id', models.BigIntegerField(blank=True, unique=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('participation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='problems.participation')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='problems.problem')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CREATED', 'created'), ('PENDING', 'pending'), ('RUNNING', 'running'), ('JUDGED', 'judged'), ('CANCELLED', 'cancelled')], default='PENDING', max_length=15)),
                ('commit_sha', models.CharField(max_length=40)),
                ('pipeline_id', models.BigIntegerField()),
                ('public_log', models.TextField()),
                ('private_log', models.TextField()),
                ('score_ratio', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='problems.repository')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('base_content', tinymce.models.HTMLField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_sets', to='problems.course')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='problems.problemset'),
        ),
        migrations.AddField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(related_name='courses', through='problems.Participation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='submission',
            constraint=models.UniqueConstraint(fields=('repository', 'commit_sha'), name='problems_submission_repository_commit_sha_uniq'),
        ),
        migrations.AddConstraint(
            model_name='participation',
            constraint=models.UniqueConstraint(fields=('course', 'identifier'), name='problems_participation_course_identifier_uniq'),
        ),
    ]
