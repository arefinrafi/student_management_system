from email import message
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Notification, Student_feedback, Student_leave, Subject, Attendance, Attendance_Report
from django.contrib import messages


def HOME(request):
    return render(request, 'Student/home.html')


def student_Notifications(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(
            student_id=student_id)
        context = {
            'notification': notification,
        }
        return render(request, 'Student/notification.html', context)


def student_notifications_mark_as_done(request, status):
    notification = Student_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notifications')


def student_Feedback(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_feedback.objects.filter(student_id=student_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'Student/feedback.html', context)


def student_Feedback_Save(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin=request.user.id)

        feedback_save = Student_feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply="",
        )
        feedback_save.save()
        messages.success(request, 'Feedback Sent')
        return redirect('student_feedback')


def student_Apply_Leave(request):
    student = Student.objects.get(admin=request.user.id)
    student_leave_history = Student_leave.objects.filter(student_id=student)

    context = {
        'student_leave_history': student_leave_history,
    }
    return render(request, 'Student/apply_leave.html', context)


def student_Leave_Save(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student = Student.objects.get(admin=request.user.id)

        student_leave = Student_leave(
            student_id=student,
            date=leave_date,
            message=leave_message,
        )
        student_leave.save()
        messages.success(request, 'Apply for leave successfully sent!')
        return redirect('student_apply_leave')


def student_View_Attendance(request):
    student = Student.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(course_id=student.course_id)

    action = request.GET.get('action')

    get_subject = None
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            # attendance = Attendance.objects.get(subject_id=subject_id)
            attendance_report = Attendance_Report.objects.filter(
                student_id=student, attendance_id__subject_id=subject_id)

    context = {
        'subjects': subject,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report,
    }
    return render(request, 'Student/view_attendance.html', context)
