from django.db import migrations, models


def add_user_agent(apps, schema_editor):
    Visit = apps.get_model("visits", "Visit")
    UserAgent = apps.get_model("visits", "UserAgent")

    user_agent = UserAgent.objects.create(name="")
    for visit in Visit.objects.all():
        visit.user_agent = user_agent
        visit.save()


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0003_split_into_multiple_tables"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAgent",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name="visit",
            name="user_agent",
            field=models.ForeignKey("visits.useragent", on_delete=models.PROTECT, null=True),
        ),
        migrations.RunPython(add_user_agent),
        migrations.AlterField(
            model_name="visit",
            name="user_agent",
            field=models.ForeignKey("visits.useragent", on_delete=models.PROTECT),
        ),
    ]
