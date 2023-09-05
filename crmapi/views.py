from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import authentication,permissions


# Create your views here.
# 
class EmployeeSerializer(serializers.ModelSerializer):
    # queryset<--->native conversion(seralizer used,,,process-serialization)
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        fields="__all__"
        # exclude=("id",)


class EmployeesView(ViewSet):
    # list create retrive delete update
    # get list retrive
    # post create
    # put update
    # delete distroy

    def list(self,request,*args,**arg):
        # localhost:8000/api/employees/
        # method:get
        # deserialization
        # {'department': ['hr']}>
        qs=Employee.objects.all()
        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department__iexact=dept) #for case sensitive matchinng---__iexact
        
        if "salary_gt" in request.query_params:
            sal=request.query_params.get("salary_gt")
            qs=qs.filter(salary__gte=sal)
        serializer=EmployeeSerializer(qs,many=True)

        return Response(data=serializer.data)
    def create(self,request,*args,**arg):
        # localhost:8000/api/employees/
        # method:post

        # creating employee records
        
        serializer=EmployeeSerializer(data=request.data) #seralization
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
    def retrieve(self,request,*args,**arg):
        # localhost:8000/api/employees/{id}
        # method:get
        id=arg.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data) 
    def update(self,request,*args,**arg):
        # localhost:8000/api/employees/{id}
        # method:put
        id=arg.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data) 
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**arg):
        # localhost:8000/api/employees/{id}
        # method:delete
        id=arg.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted") 
        except Exception:
            return Response(data="no matching records found")
        
# custom methods
 # depts=Employee.objects.all().values_list("department",flat= True).distinct()
#  localhost:8000/api/employees/departments/
    @action(methods=["get"],detail=False)
    # particular obj--detail=true
    def departments(self,request,*args,**arg):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return  Response(data=qs)


class EmployeeViewSetView(ModelViewSet):
    serializer_class=EmployeeSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]

#python manage.py createsuperuser

# authentication basic authentication,token,jwt
# isAdminUser,IsAuthenticated,AllowAny,IsAuthenticatedReadOnly



