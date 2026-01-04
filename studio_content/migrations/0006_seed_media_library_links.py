from datetime import date

from django.db import migrations


def seed_media_library_links(apps, schema_editor):
    MediaAsset = apps.get_model("studio_content", "MediaAsset")

    MediaAsset.objects.get_or_create(
        name="First Gear - Wellington 25May2024",
        defaults={
            "kind": "EMBED",
            "url": "https://drive.google.com/file/d/1k1vG-92wZBUSmIrJKwzAMfyE-342JKJz/view?usp=drive_link",
            "public_url": "https://drive.google.com/file/d/1k1vG-92wZBUSmIrJKwzAMfyE-342JKJz/view?usp=drive_link",
            "published_date": date.today(),
            "is_finished": True,
        },
    )

    MediaAsset.objects.get_or_create(
        name="First Gear - Otaki 19Dec2025",
        defaults={
            "kind": "EMBED",
            "url": "https://www.canva.com/design/DAG8LTKGYx4/SUb0HolK0pZAAI6j7qcxRQ/view?utm_content=DAG8LTKGYx4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h6515eedf14",
            "public_url": "https://www.canva.com/design/DAG8LTKGYx4/SUb0HolK0pZAAI6j7qcxRQ/view?utm_content=DAG8LTKGYx4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h6515eedf14",
            "published_date": date.today(),
            "is_finished": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("studio_content", "0005_alter_update_options"),
    ]

    operations = [
        migrations.RunPython(seed_media_library_links),
    ]
