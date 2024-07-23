# Generated by Django 4.0.6 on 2023-12-04 11:16

from django.db import migrations, models


def remove_duplicates(model_name, field_name, parent_model_name, parent_field_name):
    def migration(apps, schema_editor):
        ModelClass = apps.get_model("visits", model_name)
        ParentModelClass = apps.get_model("visits", parent_model_name)
        db_alias = schema_editor.connection.alias

        unique_values = ModelClass.objects.using(db_alias).values_list(field_name, flat=True).distinct()
        for unique_value in unique_values:
            objects = ModelClass.objects.using(db_alias).filter(**{field_name: unique_value})
            pks = objects.values_list("id", flat=True)[1:]
            ParentModelClass.objects.using(db_alias).filter(
                **{f"{parent_field_name}__in": pks}
            ).update(
                **{parent_field_name: objects.first().id}
            )
            ModelClass.objects.using(db_alias).filter(id__in=pks).delete()

    return migration

class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0004_add_user_agent_table'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates("country", "name", "visit", "country")),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.RunPython(remove_duplicates("ipaddress", "ip", "visit", "ip")),
        migrations.AlterField(
            model_name='ipaddress',
            name='ip',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.RunPython(remove_duplicates("url", "url", "visit", "url")),
        migrations.AlterField(
            model_name='url',
            name='url',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.RunPython(remove_duplicates("useragent", "name", "visit", "user_agent")),
        migrations.AlterField(
            model_name='useragent',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]