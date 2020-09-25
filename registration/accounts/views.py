from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponse
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

from .forms import RegisterForm, PhoneVerificationForm, LoginForm, ActivateForm
from .models import User


SUBJECT_LETTER = 'subject'
HTML_TEMPLATE_LETTER = 'letter.html'


def send_verfication_code(user):
    return {'success': True, 'message': 'OK'}


def verify_sent_code(user, verification_code):
    return {'success': True, 'message': 'OK'}


def send_email(user, request):
    html_template = get_template(HTML_TEMPLATE_LETTER)
    context = {
        'link': request.build_absolute_uri(reverse(
                    'accounts:activate',
                    kwargs={'token': user.token}))
    }
    html_content = html_template.render(context)
    msg = EmailMultiAlternatives(
        subject=SUBJECT_LETTER,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, 'text/html')
    return msg.send()


class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'registr.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                       The verification code is valid for 10 minutes."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options'] = ['a', 'b', 'c']
        return context

    @atomic
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        password = self.request.POST['password1']
        option = self.request.POST['option']

        is_send_code = True

        try:
            response = send_verfication_code(user)
        except Exception as e:
            is_send_code = False

        if is_send_code and response['success']:
            kwargs = {'user': user}
            self.request.method = 'GET'
            return phone_verification_view(self.request, **kwargs)

        user.delete()
        return HttpResponse('verification code not sent. \nPlease re-register.')   


def phone_verification_view(request, **kwargs):
    template_name = 'phone_confirm.html'

    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.get(username=username)
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            verification_code = request.POST['verification_code']
            response = verify_sent_code(user, verification_code)

            if response['success'] == True:
                # лучше подключить celery 
                is_send = send_email(user, request)
                user.is_send_letter = is_send
                user.save()
                return redirect('accounts:login')
            else:
                user.delete()
                # нужно удалить юзера, если он слишком часто ошибается
                # можно в юзере создать количество попыток и потом ограничить
                return redirect('accounts:register')
        else:
            return HttpResponse('Invalid code')

    else:
        form = PhoneVerificationForm()
        try:
            user = kwargs['user']
            return render(request, template_name, {'user': user, 'form': form,})
        except:
            return HttpResponse("Not Allowed")


def user_login(request):
    template_name = 'login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form})
 

class LinkRegistrationView(FormView):
    template_name = 'activate.html'
    form_class = ActivateForm

    def dispatch(self, request, token): 
    # вероятность того, что токен неуникальный будет ничтожно мала
    # или можно дописать проверку и при генерации проверять уникальность
        self.user = get_object_or_404(User, token=token)

        if self.user.is_active:
            # ссылка уже была использована
            return redirect('accounts:login')
        return super().dispatch(request, token)

    def get_initial(self):
        return {'is_active': True}

    @atomic
    def form_valid(self, form):
        # обновляем статус пользователя
        self.user.is_active = True
        self.user.save()
        return redirect('accounts:login') # ну или сразу произвести вход
