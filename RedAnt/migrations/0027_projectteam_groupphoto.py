# Generated by Django 2.0.3 on 2018-06-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0026_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectteam',
            name='GroupPhoto',
            field=models.ImageField(default='/static/images/LOGO1.png', upload_to='photos/'),
            preserve_default=False,
        ),
    ]