from django.shortcuts import render
from django.views.generic import CreateView, View, DetailView
from django.views.generic.edit import FormView
from .forms import Userregisterform, Loginform, Updatepassform, Verifyform
from .models import Usuario
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .functions import code_gen
from django.core.mail import send_mail


#  Create your views here.

class Userregisterview(FormView):
    template_name = 'usuarios/register.html'
    form_class = Userregisterform
    success_url = '/'


    def form_valid(self, form):
        # generamos el codigo
        codigo = code_gen()
        usuario = Usuario.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name=form.cleaned_data['name'],
            last_name=form.cleaned_data['last_name'],
            contry=form.cleaned_data['contry'],
            genero=form.cleaned_data['genero'],
            date_birth=form.cleaned_data['date_birth'],
            codreg=codigo,
        )
        # enviar el codigo al email del user
        asunto = 'confirmacion de email'
        mensaje = 'codigo de verificacion: {}'.format(codigo)
        email_remit = 'omar@mail.com'
        send_mail(asunto, mensaje, email_remit, [form.cleaned_data['email']])
        # redirigir a pantalla de verificacion
        return HttpResponseRedirect(reverse('usuarios_app:userverify', kwargs={'pk': usuario.id}))


class Loginuser(FormView):
    # en este proyecto el autocompletado {% url ' aplicacion:vista' %}
    # debe ser configurado en configuracion de framework de PYCHARM
    template_name = 'usuarios/login.html'
    form_class = Loginform

    success_url = reverse_lazy('usuarios_app:registro')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])

        login(self.request, user)
        return super(Loginuser, self).form_valid(form)


class Logoutview(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('usuarios_app:loginuser'))


class Updatepass(LoginRequiredMixin,FormView):
    template_name = 'usuarios/update.html'
    form_class = Updatepassform
    success_url = reverse_lazy('usuarios_app:loginuser')
    login_url = reverse_lazy('usuarios_app:loginuser')

    def form_valid(self, form):
        user = self.request.user
        usuario = authenticate(username=user.username,
                               password=form.cleaned_data['password1'])
        if usuario:
            newpass = form.cleaned_data['password2']
            usuario.set_password(newpass)
            usuario.save()
        logout(self.request)
        return super(Updatepass, self).form_valid(form)


class Codeverify(FormView):
    template_name = 'usuarios/verify.html'
    form_class = Verifyform
    success_url = reverse_lazy('usuarios_app:loginuser')

    def get_form_kwargs(self):
        kwargs = super(Codeverify, self).get_form_kwargs()
        kwargs.update(
            {
                'pk': self.kwargs['pk']
            }
        )
        return kwargs

    def form_valid(self, form):
        Usuario.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super(Codeverify, self).form_valid(form)


class Panelusuario(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('usuarios_app:loginuser')