from unicodedata import name
from django.urls import path
from . import views, hod_views, staff_views, student_views


urlpatterns = [
    path('dashboard/', views.Dashboard, name='dashboard'),

    # Login & Registration Path
    path('', views.Login, name='login'),
    path('doLogin/', views.DoLogin, name='doLogin'),
    path('doLogout/', views.DoLogout, name='logout'),

    # Profile update
    path('profile/', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

    # HOD Panel
    path('HOD/Home', hod_views.HOME, name='hod_home'),

    # HOD Student Panel
    path('HOD/Student/Add', hod_views.addStudent, name='add_student'),
    path('HOD/Student/View', hod_views.viewStudent, name='view_student'),
    path('HOD/Student/Edit/<str:id>', hod_views.editStudent, name='edit_student'),
    path('HOD/Student/Update', hod_views.updateStudent, name='update_student'),
    path('HOD/Student/Delete/<str:admin>',
         hod_views.deleteStudent, name='delete_student'),

    # HOD Course Panel
    path('HOD/Course/Add', hod_views.addCourse, name='add_course'),
    path('HOD/Course/View', hod_views.viewCourse, name='view_course'),
    path('HOD/Course/Edit/<str:id>', hod_views.editCourse, name='edit_course'),
    path('HOD/Course/Update', hod_views.updateCourse, name='update_course'),
    path('HOD/Course/Delete/<str:id>',
         hod_views.deleteCourse, name='delete_course'),

    # HOD Staff Panel
    path('HOD/Staff/Add', hod_views.addStaff, name='add_staff'),
    path('HOD/Staff/View', hod_views.viewStaff, name='view_staff'),
    path('HOD/Staff/Edit/<str:id>', hod_views.editStaff, name='edit_staff'),
    path('HOD/Staff/Update', hod_views.updateStaff, name='update_staff'),
    path('HOD/Staff/Delete/<str:admin>',
         hod_views.deleteStaff, name='delete_staff'),

    # HOD Subject Panel
    path('HOD/Subject/Add', hod_views.addSubject, name='add_subject'),
    path('HOD/Subject/View', hod_views.viewSubject, name='view_subject'),
    path('HOD/Subject/Edit/<str:id>', hod_views.editSubject, name='edit_subject'),
    path('HOD/Subject/Update', hod_views.updateSubject, name='update_subject'),
    path('HOD/Subject/Delete/<str:id>',
         hod_views.deleteSubject, name='delete_subject'),

    # HOD Sessiom Panel
    path('HOD/Session/Add', hod_views.addSession, name='add_session'),
    path('HOD/Session/View', hod_views.viewSession, name='view_session'),
    path('HOD/Session/Edit/<str:id>', hod_views.editSession, name='edit_session'),
    path('HOD/Session/Update', hod_views.updateSession, name='update_session'),
    path('HOD/Session/Delete/<str:id>',
         hod_views.deleteSession, name='delete_session'),

    # This is Staff Send Notification Panel
    path('HOD/Staff/Send_Notification',
         hod_views.send_Notification, name='send_notification'),
    path('HOD/Staff/Save_Notification',
         hod_views.save_Notification, name='save_notification'),

    # This is Student Send Notification Panel
    path('HOD/Student/Send_Notification',
         hod_views.student_Send_Notification, name='student_send_notification'),
    path('HOD/Student/Save_Notification',
         hod_views.student_Save_Notification, name='student_save_notification'),

    # This is Staff Leave Panel
    path('HOD/Staff/Leave_view', hod_views.Staff_leave_view,
         name='staff_leave_view'),
    path('HOD/Staff/approve_leave/<str:id>',
         hod_views.Staff_Approve_Leave, name='staff_approve_leave'),
    path('HOD/Staff/disapprove_leave/<str:id>',
         hod_views.Staff_Disapprove_Leave, name='staff_disapprove_leave'),

    # This is Student Leave Panel
    path('HOD/Student/Leave_view', hod_views.student_Leave_View,
         name='student_leave_view'),
    path('HOD/Student/approve_leave/<str:id>',
         hod_views.student_Approve_Leave, name='student_approve_leave'),
    path('HOD/Student/disapprove_leave/<str:id>',
         hod_views.student_Disapprove_Leave, name='student_disapprove_leave'),

    # This is Staff Feedback Panel
    path('HOD/Staff/feedback', hod_views.Hod_staff_feedback,
         name='hod_staff_feedback'),
    path('HOD/Staff/feedback/save', hod_views.Hod_staff_feedback_save,
         name='hod_staff_feedback_save'),

    # This is Student Feedback Panel
    path('HOD/Student/feedback', hod_views.Hod_student_feedback,
         name='hod_student_feedback'),
    path('HOD/Student/feedback/save', hod_views.Hod_student_feedback_save,
         name='hod_student_feedback_save'),


    # This is HOD Attendence View Panel
    path('HOD/View_Attendance', hod_views.hod_View_Attendance,
         name='hod_view_attendance'),


    # This is Staff Panel
    path('Staff/Home', staff_views.HOME, name='staff_home'),

    # This is Staff Notifications Panel
    path('Staff/Notifications', staff_views.Notifications, name='notifications'),
    path('Staff/maek_as_done/<str:status>',
         staff_views.notifications_mark_as_done, name='notifications_mark_as_done'),

    # This is Staff Apply Leave Panel
    path('Staff/Apply_leave', staff_views.Staff_Apply_Leave,
         name='staff_apply_leave'),
    path('Staff/Apply_leave_save', staff_views.Staff_Apply_Leave_Save,
         name='staff_apply_leave_save'),

    # This is Staff Feedback Panel
    path('Staff/Feedback', staff_views.Staff_Feedback,
         name='staff_feedback'),
    path('Staff/Feedback_save', staff_views.Staff_Feedback_Save,
         name='staff_feedback_save'),

    # This is Staff Take Attendance Panel
    path('Staff/Take_Attendance', staff_views.staff_Take_Attendance,
         name='staff_take_attendance'),
    path('Staff/Attendance_save', staff_views.staff_Attendance_Save,
         name='staff_attendance_save'),
    path('Staff/Attendance_view', staff_views.staff_Attendance_view,
         name='staff_attendance_view'),


    # Student Panel
    path('Student/Home', student_views.HOME, name='student_home'),

    # This is Student Notifications Panel
    path('Student/Notifications', student_views.student_Notifications,
         name='student_notifications'),
    path('Student/mark_as_done/<str:status>',
         student_views.student_notifications_mark_as_done, name='student_notifications_mark_as_done'),

    # This is Student Feedback Panel
    path('Student/Feedback', student_views.student_Feedback,
         name='student_feedback'),
    path('Student/Feedback_save', student_views.student_Feedback_Save,
         name='student_feedback_save'),

    # This is Student Leave Panel
    path('Student/Apply_for_Leave', student_views.student_Apply_Leave,
         name='student_apply_leave'),
    path('Student/Leave_save', student_views.student_Leave_Save,
         name='student_leave_save'),
    #     path('HOD/Student/disapprove_leave/<str:id>',
    #          hod_views.student_Disapprove_Leave, name='student_disapprove_leave'),


    # This is Student Attendence View Panel
    path('Student/View_Attendance', student_views.student_View_Attendance,
         name='student_view_attendance'),


]
