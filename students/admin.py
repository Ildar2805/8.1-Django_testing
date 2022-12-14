from django.contrib import admin

from students.models import Student, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'birth_date']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
