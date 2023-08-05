# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import separatedvaluesfield.models


def add_application_grant_types(apps, schema_editor):
    """
    Adds Application.grant_types field to table.
    """
    Application = apps.get_model('oauth2_provider', 'Application')
    apps = Application.objects.using(schema_editor.connection.alias).all()
    for app in apps:
        app.grant_types = [app.authorization_grant_type]
        app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_provider', '0002_08_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='authorization_grant_type',
            field=models.CharField(blank=True, max_length=32, null=True, choices=[(b'authorization-code', 'Authorization code'), (b'implicit', 'Implicit'), (b'password', 'Resource owner password-based'), (b'client-credentials', 'Client credentials')]),
        ),
        migrations.AddField(
            model_name='application',
            name='grant_types',
            field=separatedvaluesfield.models.SeparatedValuesField(default=[b'password'], max_length=150, verbose_name='grant types', choices=[(b'authorization-code', 'Authorization code'), (b'implicit', 'Implicit'), (b'password', 'Resource owner password-based'), (b'client-credentials', 'Client credentials')]),
        ),
        migrations.RunPython(add_application_grant_types),
    ]
