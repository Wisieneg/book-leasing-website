from django.urls import path

from . import views

app_name='wypozyczalnia'
urlpatterns=[
    path('',views.index,name='index'),
    path('book/<int:book_id>/',views.book_view,name='book_view'),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('account/',views.account,name='account'),
    path('book/<int:book_id>/checkout',views.checkout,name='checkout'),
    path('book/<int:book_id>/giveback',views.giveback,name='giveback'),
]
