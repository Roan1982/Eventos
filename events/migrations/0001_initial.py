from django.db import migrations, models
import django.db.models.deletion

CATEGORIES = [
    'Música','Arte','Deporte','Aire libre','Tecnología','Gastronomía','Cine','Teatro','Literatura','Educación','Ferias','Infantil','Moda','Bienestar','Otros'
]

def seed_categories(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={'slug': name.lower().replace(' ', '-')})

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=110, unique=True)),
            ],
            options={'verbose_name_plural': 'Categories', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_free', models.BooleanField(default=False)),
                ('venue_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('draft', 'Borrador'), ('published', 'Publicado'), ('cancelled', 'Cancelado')], default='draft', max_length=20)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.category')),
            ],
            options={'ordering': ['-featured', '-created_at']},
        ),
        migrations.CreateModel(
            name='MediaBlob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.BinaryField()),
                ('content_type', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=255)),
                ('size', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='events.event')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='events.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='events.tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='auth.user'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'event')},
        ),
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
