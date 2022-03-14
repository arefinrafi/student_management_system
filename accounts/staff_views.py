from email import message
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course, Session_Year, Staff_feedback, Student, CustomUser, Staff, Subject, Staff_Notification, Staff_leave, Staff_feedback
from django.contrib import messages


@login_required(login_url='/')
def HOME(request):
    return render(request, 'Staff/home.html')


@login_required(login_url='/')
def Notifications(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        notifications = Staff_Notification.objects.filter(staff_id=staff_id)
        context = {
            'notifications': notifications,
        }
        return render(request, 'Staff/notification.html', context)


@login_required(login_url='/')
def notifications_mark_as_done(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notifications')


@login_required(login_url='/')
def Staff_Apply_Leave(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)

        context = {
            'staff_leave_history': staff_leave_history
        }
    return render(request, 'Staff/apply_leave.html', context)


@login_required(login_url='/')
def Staff_Apply_Leave_Save(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_leave(
            staff_id=staff,
            date=leave_date,
            message=leave_message,
        )
        leave.save()
        messages.success(request, 'Apply for leave successfully sent!')
        return redirect('staff_apply_leave')


@login_required(login_url='/')
def Staff_Feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_feedback.objects.filter(staff_id=staff_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'Staff/feedback.html', context)


@login_required(login_url='/')
def Staff_Feedback_Save(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        staff = Staff.objects.get(admin=request.user.id)

        feedback_save = Staff_feedback(
            staff_id=staff,
            feedback=feedback,
            feedback_reply="",
        )
        feedback_save.save()
        messages.success(request, 'Feedback Sent')
        return redirect('staff_feedback')
