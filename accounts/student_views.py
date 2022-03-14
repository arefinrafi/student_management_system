from email import message
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Notification, Student_feedback
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
