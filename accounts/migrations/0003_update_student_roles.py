from django.db import migrations


def forwards(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(role='student').update(role='facility')


def backwards(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(role='facility').update(role='student')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_studentid_to_facilityid'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
