from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


class Advert(models.Model):
    CATEGORIES = (
        ('Tanks', 'Tanks'),
        ('Healers', 'Healers'),
        ('DDs', 'DDs'),
        ('Merchants', 'Merchants'),
        ('Guildmasters', 'Guildmasters'),
        ('Questgivers', 'Questgivers'),
        ('Blacksmiths', 'Blacksmiths'),
        ('Leatherworkers', 'Leatherworkers'),
        ('Potion Makers', 'Potion Makers'),
        ('Spellmasters', 'Spellmasters'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    headline = models.CharField(max_length=100)
    text = models.TextField()
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


class Response(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response by {self.user.username} to '{self.advert.headline}'"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=16, blank=True, null=True)

    def generate_confirmation_code(self):
        self.confirmation_code = get_random_string(length=16)

    def send_registration_confirmation_email(self):
        subject = 'Registration Confirmation Code'
        message = f'Your confirmation code is: {self.confirmation_code}'
        from_email = 'test@test.com'
        recipient_list = [self.user.email]
        send_mail(subject, message, from_email, recipient_list)
