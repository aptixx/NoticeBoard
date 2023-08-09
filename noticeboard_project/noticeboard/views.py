from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Advert, Response
from .forms import AdvertForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                user_profile = UserProfile.objects.create(user=user)
                user_profile.send_registration_confirmation_email()
            except Exception as e:
                print(f"Error sending email: {e}")

            return redirect('registration_confirmation')
    else:
        form = CustomUserCreationForm()

    return render(request, 'noticeboard/register.html', {'form': form})


def registration_confirmation(request):
    return render(request, 'noticeboard/registration_confirmation.html')


def view_advert(request, advert_id):
    advert = Advert.objects.get(id=advert_id)
    return render(request, 'noticeboard/view_advert.html', {'advert': advert})


@login_required
def home(request):
    adverts = Advert.objects.all()
    return render(request, 'noticeboard/home.html', {'adverts': adverts, 'user': request.user})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'noticeboard/login.html', {'form': form})


@login_required
def create_edit_advert(request, advert_id=None):
    if advert_id:
        advert = Advert.objects.get(pk=advert_id)
    else:
        advert = None

    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES, instance=advert)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')
    else:
        form = AdvertForm(instance=advert)

    return render(request, 'noticeboard/create_edit_advert.html', {'form': form})


@login_required
def delete_advert(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)

    if request.method == 'POST':
        advert.delete()
        return redirect('home')

    return redirect('view_advert', advert_id=advert_id)


@login_required
def view_responses(request, advert_id):
    advert = Advert.objects.get(pk=advert_id)

    # Exclude responses with accepted=False
    responses = Response.objects.filter(advert=advert, accepted=True)

    # Get the error parameter from the query string
    error_message = request.GET.get('error', None)

    context = {
        'advert': advert,
        'responses': responses,
        'error_message': error_message
    }

    return render(request, 'noticeboard/view_responses.html', context)


@login_required
def leave_response(request, advert_id):
    advert = Advert.objects.get(pk=advert_id)

    if request.method == 'POST':
        response_text = request.POST.get('response_text')

        if response_text:
            try:
                response = Response.objects.create(
                    advert=advert, user=request.user, text=response_text, accepted=False
                )
                # Send email notification to advert owner
                if request.user != advert.user:
                    subject = f"New Response to Your Advert: {advert.headline}"
                    message = f"A new response has been left for your advert:\n{response_text}"
                    from_email = "test@test.com"
                    recipient_list = [advert.user.email]
                    send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Handle any errors (e.g., email sending error)
                print(f"Error while processing response: {e}")

            return redirect('view_responses', advert_id=advert_id)

    return render(request, 'noticeboard/leave_response.html', {'advert': advert})


@login_required
def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'noticeboard/profile.html', {'user': user})


@login_required
def user_responses(request):
    user_adverts = Advert.objects.filter(user=request.user)
    responses = Response.objects.filter(advert__in=user_adverts).exclude(user=request.user)

    # Filter by advert if form is submitted
    advert_filter = request.GET.get('advert_filter')
    if advert_filter:
        responses = responses.filter(advert_id=advert_filter)

    return render(request, 'noticeboard/user_responses.html', {'responses': responses, 'user_adverts': user_adverts})


@login_required
def my_responses(request):
    my_responses = Response.objects.filter(user=request.user)

    # Extract the advert IDs for which the user has left responses
    advert_ids_with_responses = my_responses.values_list('advert_id', flat=True)

    # Get the adverts for which the user has left responses
    user_adverts = Advert.objects.filter(id__in=advert_ids_with_responses)

    # Filter by advert if form is submitted
    advert_filter = request.GET.get('advert_filter')
    if advert_filter:
        my_responses = my_responses.filter(advert_id=advert_filter)

    return render(request, 'noticeboard/my_responses.html', {'my_responses': my_responses, 'user_adverts': user_adverts})


@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    if request.method == 'POST':
        if response.user == request.user or response.advert.user == request.user:
            response.delete()
    return redirect('home')


@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if request.method == 'POST':
        if request.user == response.advert.user:
            response.accepted = True
            response.save()

            # Send email to the user who sent the response
            try:
                subject = f"Your Response has been Accepted"
                message = f"Your response to the advert '{response.advert.headline}' has been accepted."
                from_email = "test@test.com"
                recipient_list = [response.user.email]
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Handle any errors (e.g., email sending error)
                print(f"Error while processing response: {e}")

    return redirect('user_responses', advert_id=response.advert.id)
