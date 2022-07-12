# Generated by Django 4.0.5 on 2022-06-23 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='nationality',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='author',
            name='native_language',
            field=models.ForeignKey(help_text='Mother tonge...???', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
