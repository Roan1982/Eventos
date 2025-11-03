from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_notification_userinterest'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
