from django.contrib import auth
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import redirect, render

# Create your views here.
from .forms import SignUpForm, ProfileForm, ChangePasswordForm
from .tokens import account_activation_token


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('account/active_email.html', {
                    'user': user, 'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

            mail_subject = 'Activate your account of "IRememberYourPast.com".'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'account/send_email_for_confirm.html', {'email': to_email})

    else:
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('profile_edit')
    else:
        return render(request, 'account/auth_fail.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            # profile.user = request.user
            profile.save()
                        
            return redirect('profile_edit')
    else:
        form = ProfileForm()
        context = {'form':form}
    return render(request, 'account/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')


############################
# Email Check
############################
def checkemail(request):
    data = {}
    email = request.GET.get('email')
    if email:
        email = User.objects.filter(email = email).exists()
        if email:
            data["exists"] = True
        
    return JsonResponse(data, safe=False)


############################
# Change Password
############################
@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('account:profile_edit')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'account/password.html', {'form': form})
