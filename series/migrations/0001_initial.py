# Generated by Django 4.1.4 on 2022-12-26 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_title', models.CharField(max_length=570)),
                ('episode_image', models.ImageField(blank=True, upload_to='episodes')),
                ('episode_type', models.CharField(max_length=570)),
                ('episode_video', models.FileField(blank=True, upload_to='')),
                ('episode_duration', models.CharField(blank=True, default='08:42', max_length=10)),
                ('episode_shorttext', models.CharField(blank=True, max_length=200)),
                ('episode_is_free', models.BooleanField(default=False)),
                ('episode_is_published', models.BooleanField(default=False)),
                ('episode_slug', models.CharField(max_length=570)),
                ('episode_text', tinymce.models.HTMLField()),
                ('episode_position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EpisodeFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='files/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='ParentEpisode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('title', models.CharField(max_length=570)),
                ('episodes', models.ManyToManyField(blank=True, to='series.episode')),
            ],
        ),
        migrations.CreateModel(
            name='SerieCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=570)),
                ('icon', models.CharField(max_length=570)),
            ],
        ),
        migrations.CreateModel(
            name='SerieWatcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie_id', models.IntegerField()),
                ('is_bought', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SerieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.IntegerField()),
                ('serie_id', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SerieDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie_id', models.IntegerField()),
                ('episode_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=570)),
                ('slug', models.CharField(blank=True, max_length=570)),
                ('description', models.TextField(blank=True)),
                ('serie_image', models.ImageField(blank=True, upload_to='media/series/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('uzatmadegeri', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('featured', models.BooleanField(default=False)),
                ('trending', models.BooleanField(default=False)),
                ('popular', models.BooleanField(default=False)),
                ('meta_title', models.CharField(max_length=570)),
                ('meta_description', models.TextField()),
                ('meta_keywords', models.TextField()),
                ('is_published', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('rater', models.DecimalField(decimal_places=2, default=4.5, max_digits=3)),
                ('rateoran', models.IntegerField(default=90)),
                ('parent_episode', models.ManyToManyField(blank=True, null=True, to='series.parentepisode')),
                ('serie_category', models.ManyToManyField(to='series.seriecategory')),
                ('teacher', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='episode_files',
            field=models.ManyToManyField(blank=True, to='series.episodefiles'),
        ),
    ]
