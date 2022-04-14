from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import TaskList


@login_required
def todolist(request):
    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
        messages.success(request, ('New task added!'))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks': all_tasks})


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request, ('Access Restricted, You Are Not Allowed!'))
    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ('Task edited!'))
        return redirect('todolist')

    task_obj = TaskList.objects.get(pk=task_id)
    return render(request, 'edit.html', {'task_obj': task_obj})


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ('Access Restricted, You Are Not Allowed!'))
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')


def index(request):
    context = {'welcome_text': "Welcome to index page"}
    return render(request, 'index.html', context)


def contact(request):
    context = {'welcome_text': "Welcome to Contact Us page"}
    return render(request, 'contact.html', context)


def about(request):
    context = {'welcome_text': "Welcome to About Us page"}
    return render(request, 'about.html', context)
