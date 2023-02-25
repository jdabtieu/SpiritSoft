import csv
from datetime import datetime
from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
import random
import tempfile

from main.models import Student, Prize
from .models import *

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

class CreateReportView(View):
    @method_decorator(staff_member_required)
    @method_decorator(permission_required("actions.can_create_report", login_url="/admin/"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Create Report',
        )
        return render(request, "createreport.html", context)

    def post(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Create Report',
        )
        if Student.objects.count() == 0:
            messages.error(request, "At least 1 student required to generate a report")
            return render(request, "createreport.html", context)
        layout = request.POST.get("layout")
        output = []
        if layout == "together":
            students = list(Student.objects.all().order_by('-points', 'first_name', 'last_name'))
            prev_pts, prev_place = -1, -1
            for i in range(len(students)):
                if students[i].points != prev_pts:
                    prev_pts = students[i].points
                    prev_place = i + 1
                place = prev_place
                output.append([
                    place,
                    students[i].first_name + " " + students[i].last_name,
                    students[i].points
                ])
            output = [["School Ranking", output]]
            context["lb"] = output
            return render(request, "createreport.html", context)
        elif layout == "sepgrade":
            for grade in Student.objects.order_by('grade').values_list('grade', flat=True).distinct():
                curgrade = []
                students = list(Student.objects.filter(grade=grade).order_by('-points', 'first_name', 'last_name'))
                prev_pts, prev_place = -1, -1
                for i in range(len(students)):
                    if students[i].points != prev_pts:
                        prev_pts = students[i].points
                        prev_place = i + 1
                    place = prev_place
                    curgrade.append([
                        place,
                        students[i].first_name + " " + students[i].last_name,
                        students[i].points
                    ])
                output.append([f"Grade {grade}", curgrade])
            context["lb"] = output
            return render(request, "createreport.html", context)
        else:
            messages.error(request, "Invalid selection")
            return render(request, "createreport.html", context)

class QuarterlyWinnerView(View):
    @method_decorator(staff_member_required)
    @method_decorator(permission_required("actions.can_view_winners", login_url="/admin/"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Pick Quarterly Winners',
            past_winners=list(QuarterlyWinner.objects.all().order_by("-date"))[:20]
        )
        return render(request, "quarterlywinners.html", context)

    @method_decorator(permission_required("actions.can_pick_winners", login_url="/admin/"))
    def post(self, request):
        context = dict(
            admin.site.each_context(request),
            title='Pick Quarterly Winners',
            past_winners=list(QuarterlyWinner.objects.all().order_by("-date"))[:20]
        )
        if Student.objects.count() == 0:
            messages.error(request, "At least 1 student required to generate a report")
            return render(request, "quarterlywinners.html", context)
        topscore = request.POST.get("topscore")
        rngscore = request.POST.get("random")
        output = []
        students = list(Student.objects.values())
        winners = {}
        if topscore == "all":
            max_score = max([s["points"] for s in students])
            scorers = [s for s in students if s["points"] == max_score]
            winner = random.choice(scorers)
            students.remove(winner)
            winners["Top Scorer"] = winner
        elif topscore == "gr":
            grades = {}
            for s in students:
                if s["grade"] not in grades:
                    grades[s["grade"]] = []
                grades[s["grade"]].append(s)
            for grade, stus in grades.items():
                max_score = max([s["points"] for s in stus])
                scorers = [s for s in stus if s["points"] == max_score]
                winner = random.choice(scorers)
                students.remove(winner)
                winners[f"Grade {grade}"] = winner
        if rngscore == "all" and len(students) > 0:
            winner = random.choice(students)
            students.remove(winner)
            winners["Random Student"] = winner
        elif rngscore == "gr":
            grades = {}
            for s in students:
                if s["grade"] not in grades:
                    grades[s["grade"]] = []
                grades[s["grade"]].append(s)
            for grade, stus in grades.items():
                winner = random.choice(students)
                students.remove(winner)
                winners[f"Random (Grade {grade})"] = winner
        context["winners"] = winners
        context["prizes"] = Prize.objects.all().order_by("-points", "name")

        if request.POST.get("clearpoints"):
            for student in winners.values():
                student = Student.objects.get(id=student["id"])
                student.points = 0
                student.save()
        if request.POST.get("clearpointsall"):
            Student.objects.all().update(points=0)

        # Create log entries
        for student in winners.values():
            student = Student.objects.get(id=student["id"])
            date = datetime.now()
            points = student.points
            e = QuarterlyWinner.objects.create(student=student, date=date, points=points)
            e.save()

        return render(request, "quarterlywinners.html", context)
