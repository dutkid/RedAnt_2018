# Generated by Django 2.0.3 on 2018-05-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0006_auto_20180421_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='Name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='ShortName',
            field=models.CharField(max_length=100, null=True, verbose_name='英文缩写'),
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='TeamName',
            field=models.CharField(max_length=100, null=True, verbose_name='项目组名称'),
        ),
    ]