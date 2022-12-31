# Generated by Django 4.1.3 on 2022-12-31 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='hocsinh',
            name='LOPHOC',
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gr15m', models.FloatField(default=0)),
                ('gr45m', models.FloatField(default=0)),
                ('grExam', models.FloatField(default=0)),
                ('semester', models.IntegerField(null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.hocsinh')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.subject')),
            ],
        ),
        migrations.AddField(
            model_name='hocsinh',
            name='LOPHOC',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.lophoc'),
        ),
    ]
