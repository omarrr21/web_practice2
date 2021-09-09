from django import forms
from django.contrib.auth import authenticate
from .models import Usuario

class Userregisterform(forms.ModelForm):
    password1=forms.CharField(label='Contraseña',required=True,widget=forms.PasswordInput(
        attrs={'placeholder':'contraseña'}))
    password2 = forms.CharField(label='Confirmación contraseña', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'repetir contraseña'}))
    class Meta:
        model= Usuario
        fields=(
            'email','name','last_name','contry','genero','date_birth',
        )
        labels={
            'email':'Correo electronico','date_birth':'fecha de nacimiento','last_name':'Apellidos'
        }
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class Loginform(forms.Form):
    email=forms.EmailField(label='email',required=True,widget=forms.EmailInput(attrs={'placeholder':'Email',
                                                                                          'style':'{margin:10px}'}))
    password = forms.CharField(label='contraseña', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'contraseña'}))

    def clean(self):
        #clean por si solo significa que es una validacion que debe hacerse primero, cuando tiene _ (barra baja)
        #validara el campo despues de la barra
        cleaned_data = super(Loginform, self).clean()
        user=self.cleaned_data['mail']
        passw=self.cleaned_data['password']
        if not authenticate(username=user,password=passw):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        return self.cleaned_data

class Updatepassform(forms.Form):
    password1=forms.CharField(label='contraseña1',required=True,
                              widget=forms.PasswordInput(attrs={'placeholder':'Contraseña actual'}))
    password2=forms.CharField(label='contraseña2',required=True,
                              widget=forms.PasswordInput(attrs={'placeholder':'contraseña nueva'}))


class Verifyform(forms.Form):
    code=forms.CharField(required=True)

    def __init__(self,pk,*args,**kwargs):
        self.id_user=pk
        super(Verifyform, self).__init__(*args,**kwargs)

    def clean_code(self):
        codigo=self.cleaned_data['code']
        if len(codigo)==6:
            #verificamos si el codigo  e id son validos
            actv=Usuario.objects.code_validation(self.id_user,codigo)
            if not actv:
                raise forms.ValidationError('codigo incorrecto')
        else:
            raise forms.ValidationError('codigo incorrecto')


