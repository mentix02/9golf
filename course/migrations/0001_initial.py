# Generated by Django 5.1.1 on 2024-10-06 06:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


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
                ('name', models.CharField(max_length=255)),
                ('images', models.JSONField(blank=True, default=list)),
                ('description', models.TextField(blank=True, default='')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=False, help_text='Visible to other users')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveBigIntegerField(help_text='Distance from the tee to the hole in yards')),
                ('par', models.PositiveSmallIntegerField(help_text='Number of strokes a golfer should take to complete the hole')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holes', to='course.course')),
            ],
            options={
                'unique_together': {('course', 'number')},
            },
        ),
    ]