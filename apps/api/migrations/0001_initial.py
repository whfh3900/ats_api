# Generated by Django 4.2 on 2023-04-21 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tagghist",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("CORP_ID", models.CharField(max_length=20)),
                ("MODEL_ID", models.CharField(max_length=30)),
                ("UPLD_FILE_NM", models.CharField(max_length=50)),
                ("REG_DT", models.CharField(max_length=14)),
            ],
        ),
    ]
