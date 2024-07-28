from django.urls import path
from CallerInsight.views import *

urlpatterns=[
	path('register/',Register.as_view(),name='register'),
	path('login/',Login.as_view(),name='login'),

	path('search_by_name/',SearchByName.as_view(),name='search_by_name'),
	path('search_by_phone_number/',SearchByPhoneNumber.as_view(),name='search_by_phone_number'),	
]