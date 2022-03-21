from email import message
from multiprocessing import context
import profile
from unicodedata import name
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course, Session_Year, Staff_Notification, Student_Notification, Student, CustomUser, Staff, Student_feedback, Subject, Staff_leave, Staff_feedback, Student_leave, Attendance, Attendance_Report
from django.contrib import messages


@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }

    return render(request, 'Hod/home.html', context)


# Hod Student Section
@login_required(login_url='/')
def addStudent(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken.')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken.')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                profile_pic=profile_pic,
                email=email,
                username=username,
                user_type=3,
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin=user,
                address=address,
                gender=gender,
                course_id=course,
                session_year_id=session_year,

            )
            student.save()
            messages.success(request, user.first_name + ' ' +
                             user.last_name + ' Are Successfully Added.')
            return redirect('add_student')

    context = {
        'course': course,
        'session_year': session_year,
    }

    return render(request, 'Hod/add_student.html', context)


@login_required(login_url='/')
def viewStudent(request):
    student = Student.objects.all()
    context = {
        'students': student,
    }
    return render(request, 'Hod/view_student.html', context)


@login_required(login_url='/')
def editStudent(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context = {
        'students': student,
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/edit_student.html', context)


@login_required(login_url='/')
def updateStudent(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        address = request.POST.get('address')

        customuser = CustomUser.objects.get(id=student_id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.email = email
        customuser.username = username

        if profile_pic != None and profile_pic != "":
            customuser.profile_pic = profile_pic

        if password != None and password != "":
            customuser.set_password(password)
        customuser.save()

        student = Student.objects.get(admin=student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session

        student.save()
        messages.success(request, 'Record are successfully updated!')
        return redirect('view_student')

    return render(request, 'Hod/edit_student.html')


@login_required(login_url='/')
def deleteStudent(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.warning(request, 'Record are successfully deleted!')
    return redirect('view_student')

# Hod Course Section


@login_required(login_url='/')
def addCourse(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course = Course(
            name=course_name,
        )
        course.save()
        messages.success(request, "Course are successfully created.")
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')


@login_required(login_url='/')
def viewCourse(request):
    course = Course.objects.all()
    context = {
        'courses': course,
    }
    return render(request, 'Hod/view_course.html', context)


@login_required(login_url='/')
def editCourse(request, id):
    course = Course.objects.get(id=id)
    context = {
        'courses': course,
    }
    return render(request, 'Hod/edit_course.html', context)


@login_required(login_url='/')
def updateCourse(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id=course_id)
        course.name = course_name
        course.save()
        messages.success(request, 'Course are updated successfully')
        return redirect('view_course')
    return render(request, 'Hod/edit_course.html')


@login_required(login_url='/')
def deleteCourse(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.warning(request, 'Course are deleted successfully')
    return redirect('view_course')


# Hod Staff Section
@login_required(login_url='/')
def addStaff(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken!')
            return redirect('add_staff')
        else:
            user = CustomUser(first_name=first_name, last_name=last_name,
                              email=email, username=username, profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender,
            )
            staff.save()
            messages.success(request, 'Staff are successfully added')
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def viewStaff(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def editStaff(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
def updateStaff(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        user = CustomUser.objects.get(id=staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.first_name = first_name

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        if password != None and password != "":
            user.set_password(password)
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender
        staff.save()
        messages.success(request, 'Staff is a successfully updated')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')


@login_required(login_url='/')
def deleteStaff(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.warning(request, 'Staff deleted successfully!')
    return redirect('view_staff')


# HOD Subject Panel
@login_required(login_url='/')
def addSubject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            name=name,
            course_id=course,
            staff_id=staff,
        )
        subject.save()
        messages.success(request, 'Subject are added successfully.')
        return redirect('add_subject')

    context = {
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/add_subject.html', context)


@login_required(login_url='/')
def viewSubject(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/view_subject.html', context)


@login_required(login_url='/')
def editSubject(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'subject': subject,
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/edit_subject.html', context)


@login_required(login_url='/')
def updateSubject(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            id=subject_id,
            name=name,
            course_id=course,
            staff_id=staff,
        )
        subject.save()
        messages.success(request, 'Subject updated successfully')
        return redirect('view_subject')


@login_required(login_url='/')
def deleteSubject(request, id):
    subject = Subject.objects.filter(id=id)
    subject.delete()
    messages.warning(request, 'Subject deleted successfully')
    return redirect('view_subject')


@login_required(login_url='/')
def addSession(request):
    if request.method == "POST":
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        session = Session_Year(
            session_start=session_start,
            session_end=session_end,
        )
        session.save()
        messages.success(request, 'Subject are created successfully')
        return redirect('add_session')
    return render(request, 'Hod/add_session.html')


@login_required(login_url='/')
def viewSession(request):
    session = Session_Year.objects.all()
    context = {
        'session': session,
    }
    return render(request, 'Hod/view_session.html', context)


@login_required(login_url='/')
def editSession(request, id):
    session = Session_Year.objects.filter(id=id)
    context = {
        'session': session,
    }
    return render(request, 'Hod/edit_session.html', context)


@login_required(login_url='/')
def updateSession(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        session = Session_Year(
            id=session_id,
            session_start=session_start,
            session_end=session_end,
        )
        session.save()
        messages.success(request, 'Session are successfully updated')
        return redirect('view_session')


@login_required(login_url='/')
def deleteSession(request, id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.warning(request, 'Session are deleted successfully')
    return redirect('view_session')


@login_required(login_url='/')
def send_Notification(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by(
        '-id')[0:5]  # last five message
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Hod/staff_notification.html', context)


@login_required(login_url='/')
def save_Notification(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id=staff,
            message=message
        )
        notification.save()
        messages.success(request, 'Notification are successfully send')
        return redirect('send_notification')


@login_required(login_url='/')
def student_Send_Notification(request):
    student = Student.objects.all()
    see_notification = Student_Notification.objects.all().order_by(
        '-id')
    context = {
        'student': student,
        'see_notification': see_notification,
    }
    return render(request, 'Hod/student_notification.html', context)


@login_required(login_url='/')
def student_Save_Notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')

        student = Student.objects.get(admin=student_id)
        notification = Student_Notification(
            student_id=student,
            message=message
        )
        notification.save()
        messages.success(request, 'Notification are successfully send')
        return redirect('student_send_notification')


@login_required(login_url='/')
def Staff_leave_view(request):
    staff_leave = Staff_leave.objects.all()
    context = {
        'staff_leave': staff_leave,
    }
    return render(request, 'Hod/staff_leave.html', context)


@login_required(login_url='/')
def Staff_Approve_Leave(request, id):
    approve = Staff_leave.objects.get(id=id)
    approve.status = 1
    approve.save()
    return redirect('staff_leave_view')


@login_required(login_url='/')
def Staff_Disapprove_Leave(request, id):
    disapprove = Staff_leave.objects.get(id=id)
    disapprove.status = 2
    disapprove.save()
    return redirect('staff_leave_view')


@login_required(login_url='/')
def student_Leave_View(request):
    student_leave = Student_leave.objects.all()
    context = {
        'student_leave': student_leave,
    }
    return render(request, 'Hod/student_leave.html', context)


@login_required(login_url='/')
def student_Approve_Leave(request, id):
    approve = Student_leave.objects.get(id=id)
    approve.status = 1
    approve.save()
    return redirect('student_leave_view')


@login_required(login_url='/')
def student_Disapprove_Leave(request, id):
    disapprove = Student_leave.objects.get(id=id)
    disapprove.status = 2
    disapprove.save()
    return redirect('student_leave_view')


@login_required(login_url='/')
def Hod_staff_feedback(request):
    feedback = Staff_feedback.objects.all()
    feedback_history = Staff_feedback.objects.all().order_by("-id")[0:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history
    }
    return render(request, 'Hod/staff_feedback.html', context)


@login_required(login_url='/')
def Hod_staff_feedback_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()

        return redirect('hod_staff_feedback')


@login_required(login_url='/')
def Hod_student_feedback(request):
    feedback = Student_feedback.objects.all()
    feedback_history = Student_feedback.objects.all().order_by("-id")[0:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history
    }
    return render(request, 'Hod/student_feedback.html', context)


@login_required(login_url='/')
def Hod_student_feedback_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()

        return redirect('hod_student_feedback')


@login_required(login_url='/')
def hod_View_Attendance(request):
    subject = Subject.objects.all()
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
    return render(request, 'Hod/view_attendance.html', context)
