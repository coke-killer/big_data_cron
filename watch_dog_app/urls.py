# __author__: "Yu Dongyue"
# date: 2021/5/31
from django.urls import path
from watch_dog_app import views
from watch_dog_app.views import InsertProjectView, SelectProjectView, AllProjectView, DeleteProjectView, \
    UpdateProjectView

app_name = 'watch_dog_app'
urlpatterns = [
    path('insert/', InsertProjectView.as_view(), name='insert_project'),
    path('all/<int:pg>', AllProjectView.as_view(), name='all_project'),
    path('select/<int:pj_id>', SelectProjectView.as_view(), name='select_project'),
    path('delete/<int:pj_id>', DeleteProjectView.as_view(), name='delete_project'),
    path('update/', UpdateProjectView.as_view(),name='update_project'),
]
