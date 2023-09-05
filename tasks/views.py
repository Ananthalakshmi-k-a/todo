from django.shortcuts import render,redirect
from django.views.generic import View
# Create your views here.
from django import forms
from django.contrib import messages
from tasks.models import Todo

class TodoForm(forms.Form):
    task_name=forms.CharField()
    # user=forms.CharField()
class TodoCreateView(View):
    def get(self,request,*args,**arg):
        form=TodoForm()
        return render(request,"todo-add.html",{"form":form})
    def post(self,request,*args,**arg):
        form=TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Todo.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"todo has been created succesfully")
            return redirect("todo-list")
        messages.error(request,"fail to create todo")
        return render(request,"todo-add.html",{"form":form})
    
class TodoListView(View):
    def get(self,request,*args,**arg):
        qs=Todo.objects.filter(status=False,user=request.user).order_by("-date")
        return render(request,"todo-list.html",{"todos":qs})
    
class TodoDetailsView(View):
    def get(self,request,*args,**arg):
        id=arg.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo-detail.html",{"todo":qs})

class TodoDeleteView(View):
    def get(self,request,*args,**arg):
        id=arg.get("pk")
        qs=Todo.objects.filter(id=id).delete()
        messages.success(request,"todo deleted succesfully")
        return redirect("todo-list")
    
class TodoMarkAsDoneView(View):
    def get(self,request,*args,**arg):
        id=arg.get("pk")
        qs=Todo.objects.filter(id=id).update(status=True)
        messages.success(request,"todo has been updated succesfully")
        return redirect("todo-list")
class TodoCompletedView(View):
    def get(self,request,*args,**arg):
        qs=Todo.objects.filter(status=True)
        return render(request,"todo-completed.html",{"todos":qs})