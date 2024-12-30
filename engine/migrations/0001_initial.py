# Generated by Django 5.0.3 on 2024-12-15 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomepageSliders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_text', models.CharField(max_length=128)),
                ('large_text', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='homepage/sliders')),
                ('is_active', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Home Slider',
                'verbose_name_plural': 'Homepage Sliders',
            },
        ),
        migrations.CreateModel(
            name='PackageCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
            ],
            options={
                'verbose_name': 'Package Category',
                'verbose_name_plural': 'Package Categories',
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(help_text='Name of the person who gave the testimonial.', max_length=100)),
                ('author_email', models.EmailField(blank=True, help_text='Optional email for follow-up. Not displayed publicly.', max_length=254)),
                ('comment', models.TextField(help_text='The main content of the testimonial.')),
                ('rating', models.PositiveSmallIntegerField(blank=True, help_text='Optional rating from 1-5.', null=True)),
                ('is_approved', models.BooleanField(default=False, help_text='Only approved testimonials are displayed publicly.')),
                ('is_featured', models.BooleanField(default=False, help_text='Highlight this testimonial in featured sections.')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the testimonial was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When the testimonial was last updated.')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('short_description', models.CharField(blank=True, help_text='A brief marketing blurb.', max_length=300)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the destination.')),
                ('country', models.CharField(db_index=True, max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, help_text='Optional full address if applicable.', max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Latitude for map integration.', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Longitude for map integration.', max_digits=9, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='destinations/main_images/')),
                ('tags', models.CharField(blank=True, help_text="Comma-separated tags for easier filtering. Example: 'beach, family-friendly'", max_length=250)),
                ('average_rating', models.DecimalField(decimal_places=2, default=0.0, help_text='Average rating based on user reviews.', max_digits=3)),
                ('total_reviews', models.PositiveIntegerField(default=0)),
                ('popularity_score', models.PositiveIntegerField(default=0, help_text='A computed score for sorting.')),
                ('best_season', models.CharField(blank=True, help_text='Suggested best time of year to visit.', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('external_id', models.CharField(blank=True, help_text='ID from an external API.', max_length=100)),
                ('website', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Control whether the destination is visible.')),
                ('categories', models.ManyToManyField(blank=True, related_name='destinations', to='engine.destinationcategory')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DestinationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='destinations/gallery/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='engine.destination')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True)),
                ('short_description', models.CharField(blank=True, help_text='A concise marketing description.', max_length=300)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the package.')),
                ('price', models.DecimalField(decimal_places=2, help_text='Base price per person or per package.', max_digits=10)),
                ('currency', models.CharField(default='USD', help_text='Currency code, e.g., USD, EUR.', max_length=10)),
                ('duration_days', models.PositiveIntegerField(blank=True, help_text='Duration of the trip in days.', null=True)),
                ('start_date', models.DateField(blank=True, help_text='Start date if this is a scheduled departure.', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End date if this is a scheduled departure.', null=True)),
                ('itinerary', models.TextField(blank=True, help_text='Detailed day-by-day breakdown of activities.')),
                ('included', models.TextField(blank=True, help_text="List what's included (meals, accommodation, etc.).")),
                ('excluded', models.TextField(blank=True, help_text="List what's not included (flights, personal expenses, etc.).")),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='packages/main_images/')),
                ('tags', models.CharField(blank=True, help_text="Comma-separated tags for filtering (e.g. 'honeymoon, family-friendly')", max_length=250)),
                ('average_rating', models.DecimalField(decimal_places=2, default=0.0, help_text='Average rating based on testimonials.', max_digits=3)),
                ('total_reviews', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, help_text='Control if the package is publicly visible.')),
                ('is_featured', models.BooleanField(default=False, help_text='Highlight this package in featured sections.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('external_id', models.CharField(blank=True, help_text='External reference ID if integrated with another system.', max_length=100)),
                ('website', models.URLField(blank=True, help_text='Link to more info or booking page.')),
                ('destinations', models.ManyToManyField(blank=True, help_text='Destinations included in this package.', related_name='packages', to='engine.destination')),
                ('categories', models.ManyToManyField(blank=True, related_name='packages', to='engine.packagecategory')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='packages/gallery')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='engine.package')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddIndex(
            model_name='destination',
            index=models.Index(fields=['slug'], name='engine_dest_slug_4c9034_idx'),
        ),
        migrations.AddIndex(
            model_name='destination',
            index=models.Index(fields=['country'], name='engine_dest_country_f04056_idx'),
        ),
        migrations.AddIndex(
            model_name='package',
            index=models.Index(fields=['slug'], name='engine_pack_slug_e9dc09_idx'),
        ),
    ]
