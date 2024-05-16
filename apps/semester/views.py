from django.shortcuts import render
from .models import Semester
from .serializer import SemesterSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

class SemesterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Semester.objects.all().order_by('year', 'semester_name')
    serializer_class = SemesterSerializer

    def create(self, request, *args, **kwargs):
        print("request.user", request.user)
        if not request.user.has_perm('semester.add_semester'):
            raise PermissionDenied("You do not have permission to create new semester")
        return super().create(request, *args, **kwargs)
    


class SemesterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('semester.change_semester'):
            raise PermissionDenied("You do not have permission to update semesters")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('semester.delete_semester'):
            raise PermissionDenied("You do not have permission to delete semesters")
        return super().destroy(request, *args, **kwargs)