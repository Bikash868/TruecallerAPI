from django.urls import path
from CallerInsight.views import *

urlpatterns=[
	path('register/',Register.as_view(),name='register'),
	path('login/',Login.as_view(),name='login'),	
]