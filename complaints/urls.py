from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',            views.dashboard,         name='dashboard'),
    path('complaints/',           views.complaints_list,   name='complaints_list'),
    path('complaints/new/',       views.submit_complaint,  name='submit_complaint'),
    path('complaints/<int:pk>/',  views.complaint_detail,  name='complaint_detail'),
    path('admin-panel/',          views.admin_dashboard,   name='admin_dashboard'),
    path('admin-panel/export/',   views.admin_export_complaints_csv, name='admin_export_complaints'),
    path('notifications/',        views.notifications_view,name='notifications'),
]
