# __author__: "Yu Dongyue"
# date: 2021/6/2
from django.urls import path
from al_building.views import InsertAlgorithmView, DeleteAlgorithmView, AllAlgorithmView, SelectAlgorithmView,UpdateAlgorithmView,StartAlgorithmView,StopAlgorithmView

app_name = 'al_building'
urlpatterns = [
    path('all/<int:pj_id>/<int:pg>', AllAlgorithmView.as_view(), name='all_algorithm'),
    path('insert/<int:pj_id>', InsertAlgorithmView.as_view(), name='insert_algorithm'),
    path('delete/<int:pj_id>/<int:al_id>', DeleteAlgorithmView.as_view(), name='delete_algorithm'),
    path('update/', UpdateAlgorithmView.as_view(), name='update_algorithm'),
    path('select/<int:al_id>', SelectAlgorithmView.as_view(), name='select_algorithm'),
    path('start/<int:al_id>', StartAlgorithmView.as_view(), name='start_algorithm'),
    path('stop/<int:al_id>', StopAlgorithmView.as_view(), name='stop_algorithm'),
]
