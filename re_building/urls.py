# __author__: "Yu Dongyue"
# date: 2021/6/4
from django.urls import path
from re_building.views import InsertReportView, DeleteReportView, AllReportView, SelectReportView, \
    UpdateReportView, StartReportView, StopReportView

app_name = 're_building'
urlpatterns = [
    path('all/<int:pj_id>/<int:pg>', AllReportView.as_view(), name='all_report'),
    path('insert/<int:pj_id>', InsertReportView.as_view(), name='insert_report'),
    path('delete/<int:pj_id>/<int:re_id>', DeleteReportView.as_view(), name='delete_report'),
    path('update/', UpdateReportView.as_view(), name='update_report'),
    path('select/<int:re_id>', SelectReportView.as_view(), name='select_report'),
    path('start/<int:re_id>', StartReportView.as_view(), name='start_report'),
    path('stop/<int:re_id>', StopReportView.as_view(), name='stop_report'),
]
