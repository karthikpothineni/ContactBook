from __future__ import unicode_literals

from django.db import models
from .base import BaseModel
from django.core.validators import RegexValidator


class Contact(BaseModel):

    contact_id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$',
                                 message="Phone number must be entered in the format: '+8888888888'."
                                         "Min:8 digits." "Max:15 digits.")
    phone = models.CharField(validators=[phone_regex], max_length=16)

    class Meta(BaseModel.Meta):
        app_label = 'contact_book'
        db_table = 'contacts'
        unique_together = [("name", "email")]

    def __str__(self):
        return str(self.contact_id)




class User(BaseModel):

    id = models.AutoField(primary_key=True, auto_created=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'contact_book'
        db_table = 'users'

    def __str__(self):
        return self.email




class TokenValidation(BaseModel):
    token_id = models.AutoField(primary_key=True, auto_created=True )
    email = models.EmailField()
    token_md5 = models.CharField(max_length=100)


    class Meta:
        app_label = 'contact_book'
        db_table = 'token_validation'

    def __str__(self):
        return str(self.token_id)



