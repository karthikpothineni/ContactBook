import traceback

from rest_framework import viewsets
from ..serializers.contactSerializers import *
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import View
from django.http import HttpResponse
from ..generics import Generics
import pdb
import string, random, hashlib
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings

DEFAULT_CONTACTS_PER_PAGE = 10

class ContactViewSet(viewsets.ModelViewSet):

    def create(self, request, *args):
        try:
            result = Generics.createGeneric(Contact, "Contact", request)
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to create Contacts", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, pk=None):
        try:
            result = Generics.retrieveGeneric(Contact, "Contact", request, pk, "contact_id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to retrieve Contact", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request, *args):
        try:
            result = Generics.listGeneric(Contact, "Contact", request)
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to list Contacts", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, pk=None):
        try:
            result = Generics.updateGeneric(Contact, "Contact", request, pk, "contact_id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to Update Contact", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, pk=None):
        try:
            result = Generics.destroyGeneric(Contact, "Contact", request, pk, "contact_id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to Delete Contact", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def get_contacts(request, *args):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            try:
                result = dict()
                result['default_per_page'] = DEFAULT_CONTACTS_PER_PAGE
                validation_obj = ContactViewSet.performValidations(request)
                if validation_obj is not None:
                    return Response(validation_obj.data,validation_obj.status_code)
                result['current_page'] = int(request.data.get('page') or 1)

                if 'name' in request.data:
                    contact_obj = Contact.objects.filter(name=request.data['name'],soft_delete=False)
                if 'email' in request.data:
                    contact_obj = Contact.objects.filter(email=request.data['email'],soft_delete=False)

                paginator_obj = Paginator(contact_obj, DEFAULT_CONTACTS_PER_PAGE)
                result['total_contacts'] = paginator_obj.count
                result['total_pages'] = paginator_obj.num_pages
                if int(result['current_page']) in paginator_obj.page_range:
                    result['contacts'] = ContactSerializer(paginator_obj.page(result['current_page']).object_list, many=True).data
                    result['current_page_contacts'] = len(paginator_obj.page(result['current_page']).object_list)
                else:
                    return Response("Requested page doesnot exist",status=status.HTTP_400_BAD_REQUEST)
                return Response(result,status=status.HTTP_200_OK)

            except:
                return Response("Unable to get contacts", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)



    @staticmethod
    def performValidations(request):
        if 'page' in request.data and int(request.data['page']) <= 0:
            return Response("Page number should be greater than zero",status=status.HTTP_400_BAD_REQUEST)
        if ('name' not in request.data and 'email' not in request.data) or ('name' in request.data and 'email' in request.data):
            return Response("Please provide either name or email id to search. Don't provide both",status=status.HTTP_400_BAD_REQUEST)





########################################################################################################################


class UserViewSet(viewsets.ModelViewSet):

    def create(self, request, *args):
        try:
            if 'password' in request.data:
                request.data['password'] = hashlib.md5(request.data['password'].encode('utf-8')).hexdigest()
            result = Generics.createGeneric(User, "User", request)
            return Response(result.data,result.status_code)

        except:
            return Response("Unable to create users", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, pk=None):
        try:
            result = Generics.retrieveGeneric(User, "User", request, pk, "id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to retrieve user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request, *args):
        try:
            result = Generics.listGeneric(User, "User", request)
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to list users", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, pk=None):
        try:
            if 'password' in request.data:
                request.data['password'] = hashlib.md5(request.data['password'].encode('utf-8')).hexdigest()
            result = Generics.updateGeneric(User, "User", request, pk, "id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to Update User", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, pk=None):
        try:
            result = Generics.destroyGeneric(User, "User", request, pk, "id")
            return Response(result.data,result.status_code)
        except:
            return Response("Unable to Delete User", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


########################################################################################################################


class LoginViewSet(viewsets.ModelViewSet):

    @staticmethod
    def login(request, *args):
        try:
            user_info = dict()
            if 'email' not in request.data or 'password' not in request.data:
                return Response("Please provide email and password",status=status.HTTP_400_BAD_REQUEST)

            password = hashlib.md5(request.data['password'].encode('utf-8')).hexdigest()
            user_obj = User.objects.filter(email=request.data['email'],soft_delete=False)
            if not user_obj or user_obj.values()[0]['password'] != password:
                return Response("Invalid credentials",status=status.HTTP_403_FORBIDDEN)

            token = hashlib.md5((request.data['email']+request.data['password']).encode('utf-8')).hexdigest()+LoginViewSet.id_generator()
            user_info['email'] = user_obj.values()[0]['email']
            user_info['token_md5'] = token
            token_obj = TokenValidation.objects.filter(email=user_obj.values()[0]['email'],soft_delete=False)
            if token_obj:
                cache.delete(token_obj.values()[0]['token_md5'])
                token_obj.update(soft_delete=True)
            serializer = TokenValidationSerializer(data=user_info)
            cache.set(token, user_obj.values()[0]['is_admin'], settings.CACHE_EXPIRATION_TIME)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response("Unable to login", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))



######################################################################################################################################



# Healthcheck Methods
class healthcheck_view(View):
    def get(self, request):
        return HttpResponse()
