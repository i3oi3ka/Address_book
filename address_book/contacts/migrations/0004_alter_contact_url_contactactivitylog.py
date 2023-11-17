# Generated by Django 4.2.6 on 2023-11-07 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='url',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='ContactActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('CREATED', 'Created'), ('EDITED', 'Edited')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.contact')),
            ],
        ),
    ]
