from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from Task API!")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show tasks that belong to the logged-in user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the task
        serializer.save(user=self.request.user)
    