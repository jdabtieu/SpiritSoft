import csv
from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
import tempfile

from main.models import Student

class ImportStudentsView(View):
    @method_decorator(staff_member_required)
    @method_decorator(permission_required("actions.can_import_students", login_url="/admin/"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Import Students',
        )
        return render(request, "importstudents.html", context)

    def post(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Import Students',
        )
        stu_objs = []
        try:
            with tempfile.TemporaryFile(mode='w+', newline='') as tf:
                tf.write(request.FILES["data"].read().decode('utf-8'))
                tf.seek(0)
                data_csv = [row for row in csv.reader(tf, delimiter=',', quotechar='"')]
        except Exception:
            messages.error(request, "The data is not in a valid format, please ensure you uploaded the correct file")
            return render(request, "importstudents.html", context)

        try:
            for data in data_csv:
                if list(filter(None, data)) == []:
                    continue  # Empty row
                last_name = data[0]             # str
                first_name = data[1]            # str
                email = data[2]                 # str (email)
                number = int(data[3])           # int
                if len(data) >= 6 and data[6].isdigit():  # PowerSchool
                    grade = int(data[6])        # int
                else:  # CSV
                    grade = int(data[4])        # int
                stu_objs.append(Student(last_name=last_name, first_name=first_name,
                                        email=email, number=number, grade=grade))
        except Exception:
            import traceback
            traceback.print_exc()
            messages.error(request, "The data is malformed, please check the format")
            return render(request, "importstudents.html", context)
        # If the student already exists, we don't have to re-add them
        Student.objects.bulk_create(stu_objs, ignore_conflicts=True)
        messages.success(request, "Students successfully imported!")
        return render(request, "importstudents.html", context)