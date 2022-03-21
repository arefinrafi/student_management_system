from email import message
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course, Session_Year, Staff_feedback, Student, CustomUser, Staff, Subject, Staff_Notification, Staff_leave, Staff_feedback, Attendance, Attendance_Report
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


def staff_Take_Attendance(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id=staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course_id.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students,
    }
    return render(request, 'Staff/take_attendance.html', context)


def staff_Attendance_Save(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)

            present_students = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                student_id=present_students,
                attendance_id=attendance,
            )
            attendance_report.save()
    messages.success(request, 'Attendence Save Successfully!')
    return redirect('staff_take_attendance')


def staff_Attendance_view(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id=staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            attendance = Attendance.objects.filter(
                subject_id=get_subject, attendance_date=attendance_date)

            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(
                    attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'Staff/attendance_view.html', context)
