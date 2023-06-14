from django.db import migrations, models


def migrate_data(apps, schema_editor):
    Visit = apps.get_model("visits", "Visit")
    IPAddress = apps.get_model("visits", "IPAddress")
    Country = apps.get_model("visits", "Country")
    URL = apps.get_model("visits", "URL")

    for visit in Visit.objects.all():
        visit.ip_fk = IPAddress.objects.get_or_create(ip=visit.ip, ip_hash=visit.ip_sha1)[0]
        visit.country_fk = Country.objects.get_or_create(name=visit.country)[0]
        visit.url_fk = URL.objects.get_or_create(url=visit.url)[0]
        visit.save()

class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0002_crawler_detection"),
    ]

    operations = [
        migrations.CreateModel(
            name="IPAddress",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ip", models.GenericIPAddressField()),
                ("ip_hash", models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="URL",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("url", models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name="visit",
            name="ip_fk",
            field=models.ForeignKey("visits.ipaddress", on_delete=models.PROTECT, null=True),
        ),
        migrations.AddField(
            model_name="visit",
            name="country_fk",
            field=models.ForeignKey("visits.country", on_delete=models.PROTECT, null=True),
        ),
        migrations.AddField(
            model_name="visit",
            name="url_fk",
            field=models.ForeignKey("visits.url", on_delete=models.PROTECT, null=True),
        ),
        migrations.RunPython(migrate_data),
        migrations.RemoveField(
            model_name="visit",
            name="ip",
        ),
        migrations.RemoveField(
            model_name="visit",
            name="ip_sha1",
        ),
        migrations.RemoveField(
            model_name="visit",
            name="country",
        ),
        migrations.RemoveField(
            model_name="visit",
            name="url",
        ),
        migrations.RenameField(
            model_name="visit",
            old_name="ip_fk",
            new_name="ip",
        ),
        migrations.RenameField(
            model_name="visit",
            old_name="country_fk",
            new_name="country",
        ),
        migrations.RenameField(
            model_name="visit",
            old_name="url_fk",
            new_name="url",
        ),
        migrations.AlterField(
            model_name="visit",
            name="ip",
            field=models.ForeignKey("visits.ipaddress", on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name="visit",
            name="country",
            field=models.ForeignKey("visits.country", on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name="visit",
            name="url",
            field=models.ForeignKey("visits.url", on_delete=models.PROTECT),
        ),
    ]
