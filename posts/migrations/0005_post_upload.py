# Generated by Django 4.1.2 on 2022-12-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_labels_post_link_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upload',
            field=models.FileField(blank='True', null='True', unique='False', upload_to='uploads/'),
            preserve_default='True',
        ),
    ]