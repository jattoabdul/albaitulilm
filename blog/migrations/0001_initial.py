# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-05 14:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=75)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Post Title')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('date', models.DateField(auto_now=True)),
                ('time', models.TimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('posted', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('meta_description', models.CharField(blank=True, max_length=500, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, max_length=250, verbose_name='Meta Keywords')),
                ('body', models.TextField()),
                ('published', models.BooleanField(default=None)),
                ('post_image', models.ImageField(upload_to='blog', verbose_name='News Post Image')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Categories')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Posts'),
        ),
    ]