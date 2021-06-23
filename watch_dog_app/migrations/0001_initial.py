# Generated by Django 3.2.3 on 2021-06-02 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('project_information', models.CharField(max_length=200)),
                ('project_creatime', models.DateField()),
                ('project_creater', models.CharField(max_length=20)),
                ('project_root', models.CharField(max_length=100)),
                ('project_otherkey', models.CharField(blank=True, max_length=3000, null=True)),
            ],
            options={
                'db_table': 'wda_projects_info',
            },
        ),
    ]
