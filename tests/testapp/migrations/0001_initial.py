# Generated by Django 4.1.4 on 2023-02-15 17:47

import django.core.validators
import django.db.models.deletion
import modelcluster.fields
import taggit.managers
import wagtail.blocks
import wagtail.fields
import wagtail.search.index

from django.conf import settings
from django.db import migrations, models

import wagtailmedia.blocks


try:
    import wagtail.models.media as collections
except ImportError:
    import wagtail.models.collections as collections

import tests.testapp.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailmedia", "0004_duration_optional_floatfield"),
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("date_from", models.DateField(null=True, verbose_name="Start date")),
                (
                    "date_to",
                    models.DateField(
                        blank=True,
                        help_text="Not required if event is on a single day",
                        null=True,
                        verbose_name="End date",
                    ),
                ),
                (
                    "time_from",
                    models.TimeField(blank=True, null=True, verbose_name="Start time"),
                ),
                (
                    "time_to",
                    models.TimeField(blank=True, null=True, verbose_name="End time"),
                ),
                ("location", models.CharField(max_length=255)),
                ("body", wagtail.fields.RichTextField(blank=True)),
                ("cost", models.CharField(max_length=255)),
                ("signup_link", models.URLField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="EventPageRelatedMedia",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("title", models.CharField(help_text="Link title", max_length=255)),
                (
                    "link_media",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailmedia.media",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_media",
                        to="wagtailmedia_tests.eventpage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomMedia",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("file", models.FileField(upload_to="media", verbose_name="file")),
                (
                    "type",
                    models.CharField(
                        choices=[("audio", "Audio file"), ("video", "Video file")],
                        max_length=255,
                    ),
                ),
                (
                    "duration",
                    models.FloatField(
                        blank=True,
                        default=0,
                        help_text="Duration in seconds",
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="duration",
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="width"
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="height"
                    ),
                ),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        upload_to="media_thumbnails",
                        verbose_name="thumbnail",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                ("fancy_caption", wagtail.fields.RichTextField(blank=True)),
                (
                    "collection",
                    models.ForeignKey(
                        default=collections.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "verbose_name": "media",
                "abstract": False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name="BlogStreamPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("author", models.CharField(max_length=255)),
                ("date", models.DateField(verbose_name="Post date")),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.blocks.CharBlock(
                                    form_classname="title", icon="title"
                                ),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                            (
                                "media",
                                tests.testapp.models.TestMediaBlock(icon="media"),
                            ),
                            (
                                "video",
                                wagtailmedia.blocks.VideoChooserBlock(icon="media"),
                            ),
                            (
                                "audio",
                                wagtailmedia.blocks.AudioChooserBlock(icon="media"),
                            ),
                        ],
                        use_json_field=True,
                    ),
                ),
                (
                    "featured_media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailmedia.media",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
