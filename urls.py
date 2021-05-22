from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:id>/', views.BookDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
