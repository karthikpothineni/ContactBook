import traceback
from enum import Enum
from rest_framework.response import Response
from rest_framework import status
from .serializers.contactSerializers import *
from django.core.cache import cache

class EntityStatus(Enum):
    ACTIVE = False
    INACTIVE = True


class Generics:
    def __init__(self):
        pass


    @staticmethod
    def get_user_data_by_token(request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return Response("Please Provide Authorization In Headers", status=status.HTTP_400_BAD_REQUEST)

        if cache.get(request.META['HTTP_AUTHORIZATION']) is not None:
            value = cache.get(request.META['HTTP_AUTHORIZATION'])
            return value

        token_obj = TokenValidation.objects.filter(token_md5=request.META['HTTP_AUTHORIZATION'], soft_delete=False)
        if not token_obj:
            return Response("Please provide valid token",status=status.HTTP_403_FORBIDDEN)

        user_obj = User.objects.filter(email=token_obj.values()[0]['email'],soft_delete=False)
        if not user_obj:
            return Response("Authentication Failed",status=status.HTTP_403_FORBIDDEN)

        if user_obj.values()[0]['is_admin'] == True:
            return True
        else:
            return False



    @staticmethod
    def createGeneric(model, model_type, request):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            if model == User:
                serializer = eval(model.__name__+"Serializer")(data=request.data,context={'password': request.data['password']})
            else:
                serializer = eval(model.__name__+"Serializer")(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)


    @staticmethod
    def retrieveGeneric(model, model_type, request, pk, column_name):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            kwargs = {
                '{0}'.format(column_name): pk
            }
            obj = model.objects.filter(**kwargs)
            if obj:
                return Response(eval(model.__name__+"Serializer")(obj, many=True).data, status=status.HTTP_200_OK)
            else:
                return Response("%s with particular rule id does not exist." % model_type, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)



    @staticmethod
    def listGeneric(model, model_type, request):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            obj = model.objects.all()
            return Response(eval(model.__name__+"Serializer")(obj, many=True).data,status=status.HTTP_200_OK)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)


    @staticmethod
    def updateGeneric(model, model_type, request, pk, column_name):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            kwargs = {
                '{0}'.format(column_name): pk
            }
            obj = model.objects.filter(**kwargs)
            if obj:
                serializer = eval(model.__name__+"Serializer")(obj[0], data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response("%s with particular rule id does not exist." % model_type, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)


    @staticmethod
    def destroyGeneric(model, model_type, request, pk, column_name):
        result = Generics.get_user_data_by_token(request)
        if type(result) is not bool and result.status_code != 200:
            return Response(result.data,result.status_code)

        if result is True:
            kwargs = {
                '{0}'.format(column_name): pk
            }
            obj = model.objects.filter(**kwargs)
            if obj:
                obj.delete()
                return Response("%s successfully deleted" % model_type, status=status.HTTP_200_OK)
            else:
                return Response("%s already deleted or does not exist" % model_type, status=status.HTTP_200_OK)
        else:
            return Response("User do not have permissions",status=status.HTTP_403_FORBIDDEN)








