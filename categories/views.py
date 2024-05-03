from django.shortcuts import render,redirect,get_object_or_404
from .models import Categories
from .forms import CategoryForm

# Create your views here.
def view_admin_categories(request):
    categories_data= Categories.objects.filter(admin_id=request.user.admin_id).values()
    return render(request,'view_categories.html',{'categories':categories_data})


def view_super_categories(request):
    categories_data= Categories.objects.filter(superuser_id=request.user.id).values()
    return render(request,'superuser_categories.html',{'categories':categories_data})


def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            cname= form.cleaned_data['cname']
            category= Categories.objects.create(
                cname= cname,
                admin_id=request.user.admin_id,
            )
            print("done")
            return redirect('view_categories')
        else:
            categories_data= Categories.objects.filter(admin_id=request.user.admin_id).values()
            return render(request,'view_categories.html',{'categories':categories_data,'form':form})

    return redirect('view_categories')


def superuser_add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            cname= form.cleaned_data['cname']
            category= Categories.objects.create(
                cname= cname,
                superuser_id= request.user.id,
            )
            print("done")
            return redirect('superuser_view_categories')
        else:
            categories_data= Categories.objects.filter(superuser_id=request.user.id).values()
            return render(request,'superuser_categories.html',{'categories':categories_data,'form':form})

    return redirect('superuser_view_categories')


def update_categories(request, pk):
    category = get_object_or_404(Categories,pk=pk)
    categories_data= Categories.objects.all().filter(admin_id=request.user.admin.id)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.cname = form.cleaned_data['cname']
            category.save()
            return redirect('view_categories')  

        else:
            return render(request, 'view_categories.html', {'categories':categories_data,'category':category,'form': form})

    return render(request, 'view_categories.html', {'categories':categories_data,'category': category})


def superuser_update_categories(request, pk):
    category = get_object_or_404(Categories,pk=pk)
    categories_data= Categories.objects.filter(superuser_id=request.user.id).values()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.cname = form.cleaned_data['cname']
            category.save()
            return redirect('superuser_view_categories')  

        else:
            return render(request, 'superuser_categories.html', {'categories':categories_data,'category':category,'form': form})

    return render(request, 'superuser_categories.html', {'categories':categories_data,'category': category})


def delete_categories(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('view_categories')
    return render(request,'view_categories.html')


def superuser_delete_categories(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('superuser_view_categories')
    return render(request,'superuser_categories.html')


 