# Generated by Django 2.0.3 on 2018-04-07 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0011_blog_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='name',
            new_name='introduction',
        ),
    ]
