import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.urls import reverse
from .serializers import TaskSerializer
from . import db

logger = logging.getLogger("tasks")

# --------------------------------------------------------------------
# API VIEWS (GET, POST, PUT, PATCH, DELETE)
# --------------------------------------------------------------------

class TaskListCreateAPI(APIView):

    def get(self, request):
        try:
            tasks = db.fetch_all_tasks()
            return Response(tasks)
        except Exception:
            logger.exception("Error fetching tasks")
            return Response({"detail": "Server error"}, status=500)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                tid = db.insert_task(
                    title=data["title"],
                    description=data.get("description"),
                    due_date=data.get("due_date"),
                    status=data.get("status", "pending")
                )
                return Response(db.fetch_task(tid), status=201)
            except Exception:
                logger.exception("Error inserting task")
                return Response({"detail": "Insert failed"}, status=500)
        return Response(serializer.errors, status=400)


class TaskDetailAPI(APIView):

    def get(self, request, pk):
        task = db.fetch_task(pk)
        if not task:
            return Response({"detail": "Not found"}, status=404)
        return Response(task)

    def put(self, request, pk):  # FULL UPDATE
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            updated = db.update_task(pk, **data)
            if not updated:
                return Response({"detail": "Not found"}, status=404)
            return Response(db.fetch_task(pk))
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):  # PARTIAL UPDATE
        partial = TaskSerializer(data=request.data, partial=True)
        if partial.is_valid():
            updated = db.update_task(pk, **partial.validated_data)
            if not updated:
                return Response({"detail": "Not found"}, status=404)
            return Response(db.fetch_task(pk))
        return Response(partial.errors, status=400)

    def delete(self, request, pk):
        deleted = db.delete_task(pk)
        if not deleted:
            return Response({"detail": "Not found"}, status=404)
        return Response(status=204)

# --------------------------------------------------------------------
# HTML Templates (UI)
# --------------------------------------------------------------------

def task_list_view(request):
    try:
        tasks = db.fetch_all_tasks()
        return render(request, "tasks/task_list.html", {"tasks": tasks})
    except Exception:
        logger.exception("List render failed")
        return render(request, "tasks/task_list.html", {"tasks": [], "error": "Failed to load tasks"})

def task_add_view(request):
    if request.method == "POST":
        try:
            db.insert_task(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                due_date=request.POST.get("due_date"),
                status=request.POST.get("status", "pending"),
            )
            return redirect(reverse("task_list"))
        except Exception:
            logger.exception("Add failed")
            return render(request, "tasks/task_add.html", {"error": "Failed to add"})
    return render(request, "tasks/task_add.html")

def task_edit_view(request, pk):
    task = db.fetch_task(pk)
    if not task:
        return render(request, "tasks/task_edit.html", {"error": "Not found"})

    if request.method == "POST":
        try:
            db.update_task(
                pk,
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                due_date=request.POST.get("due_date"),
                status=request.POST.get("status"),
            )
            return redirect(reverse("task_list"))
        except Exception:
            return render(request, "tasks/task_edit.html", {"task": task, "error": "Update failed"})

    return render(request, "tasks/task_edit.html", {"task": task})
