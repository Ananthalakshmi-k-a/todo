from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from todoapi.serializers import UserSerializer,TodoSerializer
from tasks.models import Todo
from rest_framework import authentication,permissions

# Create your views here.


# create user
# email username pwd


class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    model=User
    queryset=User.objects.all()
    # create,list,detail,update,destroy
    # def create(self, request, *args, **kwargs):
    #     seralizer=UserSerializer(data=request.data)
    #     if seralizer.is_valid():
    #         usr=User.objects.create_user(**seralizer.validated_data)
    #         seralizer=UserSerializer(usr)
    #         return Response(data=seralizer.data)
    #     else:
    #         return Response(data=seralizer.errors)


class TodosView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors) 
    # def list(self,request,*args,**arg):
    #     qs=Todo.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    

# token authentication
# client appln ---------------------server appln
# 
        

