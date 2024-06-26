# Generated by Django 5.0.4 on 2024-05-01 13:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_experience_category_alter_perk_detail_and_more'),
        ('rooms', '0005_alter_room_category_alter_room_owner'),
        ('wishlists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='experiences',
            field=models.ManyToManyField(related_name='wishlists', to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='rooms',
            field=models.ManyToManyField(related_name='wishlists', to='rooms.room'),
        ),
    ]
