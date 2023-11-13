# Generated by Django 4.2.7 on 2023-11-13 22:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UOMCategory',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.basemodel')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=200)),
            ],
            bases=('web.basemodel',),
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.AddField(
            model_name='unitofmeasure',
            name='sub_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supra_unit', to='web.unitofmeasure'),
        ),
        migrations.AddField(
            model_name='unitofmeasure',
            name='sub_unit_multiplier',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ReciepeLine',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.basemodel')),
                ('quantity', models.FloatField()),
                ('note', models.TextField(blank=True, max_length=255)),
                ('rec_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ingredient')),
                ('related_reciepe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciepe_lines', to='web.reciepe')),
            ],
            bases=('web.basemodel',),
        ),
        migrations.AddField(
            model_name='unitofmeasure',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.uomcategory'),
        ),
    ]