from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_crontab.crontab import Job
from django.contrib.auth.models import User
from .models import Advert, Response


def send_weekly_summary_email():
    users = User.objects.all()

    for user in users:
        # Count the user's adverts
        user_advert_count = Advert.objects.filter(user=user).count()

        # Count the responses to the user's adverts
        user_response_count = Response.objects.filter(advert__user=user).count()

        # Count the total number of adverts
        total_advert_count = Advert.objects.all().count()

        # Prepare the email content
        subject = 'Weekly Summary'
        message = render_to_string('noticeboard/weekly_summary_email.html', {
            'user': user,
            'user_advert_count': user_advert_count,
            'user_response_count': user_response_count,
            'total_advert_count': total_advert_count,
        })
        from_email = 'test@test.com'
        recipient_list = [user.email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)
