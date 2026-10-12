from django.urls import path

from website.apps.entry import views as v

app_name = 'entry'

urlpatterns = [
    path('', v.TaskIndex.as_view(), name="index"),
    path('task/quick', v.quick_entry, name="quick"),
    path('task/<int:task_id>', v.task_detail, name="detail"),
    path('task/<int:pk>/done', v.TaskComplete.as_view(), name="complete"),
]