# Generated by Django 4.2.9 on 2024-02-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sudayun", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="resource",
            old_name="serverFileName",
            new_name="fileName",
        ),
        migrations.AlterField(
            model_name="resource_detail",
            name="isDir",
            field=models.BooleanField(default=False, verbose_name="是否目录"),
        ),
    ]