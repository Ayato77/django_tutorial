from django.urls import path

from . import views

# URLconfに名前空間を追加
app_name = 'polls'

urlpatterns = [
    # 汎用ビューを使うため書き換えた
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]