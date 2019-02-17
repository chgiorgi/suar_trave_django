# Generated by Django 2.1.7 on 2019-02-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_auto_20190216_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pictures', verbose_name='Image')),
                ('is_main', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='tour',
            name='main_picture',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='picture',
        ),
        migrations.AddField(
            model_name='images',
            name='tour',
            field=models.ForeignKey(default=None, on_delete=False, related_name='images', to='tours.Tour'),
        ),
    ]