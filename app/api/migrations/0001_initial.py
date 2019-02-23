# Generated by Django 2.1.5 on 2019-02-17 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=15)),
                ('real_price', models.FloatField()),
                ('start_price', models.FloatField()),
                ('title', models.CharField(max_length=150, null=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='provider', to='provider.Provider')),
            ],
            options={
                'db_table': 'stock',
            },
        ),
    ]