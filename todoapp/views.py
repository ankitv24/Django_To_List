from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib import messages

def task_list(request):
    tasks = Task.objects.all().order_by('completed', 'priority', 'due_date')
    filter_by = request.GET.get('filter', 'all')

    if filter_by == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_by == 'pending':
        tasks = tasks.filter(completed=False)

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')

    return render(request, 'todoapp/task_list.html', {'tasks': tasks, 'form': form, 'filter_by': filter_by})

def mark_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.warning(request, 'Task deleted.')
    return redirect('task_list')
