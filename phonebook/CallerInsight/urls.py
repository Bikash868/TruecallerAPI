from django.urls import path
from CallerInsight.views import *

urlpatterns=[
	path('register/',Register.as_view(),name='register'),
	path('login/',Login.as_view(),name='login'),

	path('search_by_name/',SearchByName.as_view(),name='search_by_name'),
	path('search_by_phone_number/',SearchByPhoneNumber.as_view(),name='search_by_phone_number'),

	path('mark_spam/',MarkSpam.as_view(),name='mark_spam'),	
	
	path('contacts/',ContactList.as_view(),name='contact_list'),
]