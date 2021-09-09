from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from PIL import Image
from django.db.models.signals import post_save


class Usuario(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    email = models.EmailField(unique=True)
    name = models.CharField('Nombre', max_length=80)
    last_name=models.CharField('Apellidos',max_length=80)
    contry=models.CharField('Nacionalidad',max_length=50,blank=True)
    genero = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)
    date_birth = models.DateField('Fecha de nacimiento',blank=True,null=True)
    codreg = models.CharField(max_length=6, blank=True)
    imagen=models.ImageField(upload_to='userprof',default='default.png')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name','last_name']

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.name + self.last_name

def optimize_img(sender, instance, **kwargs):
    if instance.imagen:
        imagen = Image.open(instance.imagen.path)
        imagen.save(instance.imagen.path,quality=20,optimize=True)

post_save.connect(optimize_img,sender=Usuario)