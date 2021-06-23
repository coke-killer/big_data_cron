# __author__: "Yu Dongyue"
# date: 2021/6/2
from django.urls import path
from db_building.views import InsertDbscriptView, DeleteDbscriptView, AllDbscriptView, SelectDbscriptView, \
    UpdateDbscriptView, StartDbscriptView, StopDbscriptView

app_name = 'al_building'
urlpatterns = [
    path('all/<int:pj_id>/<int:pg>', AllDbscriptView.as_view(), name='all_dbscript'),
    path('insert/<int:pj_id>', InsertDbscriptView.as_view(), name='insert_dbscript'),
    path('delete/<int:pj_id>/<int:db_id>', DeleteDbscriptView.as_view(), name='delete_dbscript'),
    path('update/', UpdateDbscriptView.as_view(), name='update_dbscript'),
    path('select/<int:db_id>', SelectDbscriptView.as_view(), name='select_dbscript'),
    path('start/<int:db_id>', StartDbscriptView.as_view(), name='start_dbscript'),
    path('stop/<int:db_id>', StopDbscriptView.as_view(), name='stop_dbscript'),
]
