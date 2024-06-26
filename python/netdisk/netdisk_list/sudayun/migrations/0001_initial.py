# Generated by Django 4.2.9 on 2024-02-06 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("url", models.CharField(max_length=255)),
                ("alias", models.CharField(blank=True, max_length=255, null=True)),
                ("uk", models.BigIntegerField()),
                ("serverFileName", models.CharField(max_length=255)),
                ("type", models.IntegerField()),
                ("path", models.CharField(max_length=255)),
                ("fsId", models.BigIntegerField(blank=True, null=True)),
                ("remark", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Resource_detail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("serverFileName", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=255)),
                ("fsId", models.BigIntegerField(blank=True, null=True)),
                ("category", models.IntegerField()),
                ("size", models.BigIntegerField(blank=True, null=True)),
                ("serverTime", models.DateTimeField(blank=True, null=True)),
                ("isDir", models.BooleanField(default=False)),
                ("remark", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "parentId",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="sudayun.resource_detail",
                    ),
                ),
            ],
        ),
    ]
