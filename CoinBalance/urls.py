from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('testing/', views.testing, name='testing'),
    path('', views.index, name='index'),
    path('login/', views.submit_form, name = 'submit_form'),
    path('register/', views.gotoReg, name = 'register'),
    path('completeReg/', views.register, name = 'testing'),
    path('logout/', views.logout, name = 'logout'),
    path('groups/', views.groups, name = 'groups'),
    path('createGroup/', views.createGroup, name = 'createGroup'),
    path('get_all_usernames/', views.get_usernames, name = 'get_all_usernames'),
    path('saveGroup/', views.saveGroup, name = 'saveGroup'),
    path('editGroup/', views.editGroup, name = 'editGroup'),
    path('saveEdit/', views.saveEdit, name = 'saveEdit'),
    path('usernameCheck/', views.usernameCheck, name = 'usernameCheck'),
    path('groupDetail/', views.groupDetail, name = 'groupDetail'),
    path('createExpense/', views.createExpense, name = 'createExpense'),
    path('saveExpense/', views.saveExpense, name = 'saveExpense'),
    path('expenseDetail/', views.expenseDetail, name = 'expenseDetail'),
    path('viewSettings/', views.viewSettings, name = 'viewSettings'),
    path('changePicture/', views.updateImage, name = "updateImage'"),
    path('saveSettings/', views.saveSettings, name = 'saveSettings'),
    path('addComment/', views.addComment, name = 'addComment'),
    path('createPayment/', views.createPayment, name = 'createPayment'),
    path('savePayment/', views.savePayment, name = 'savePayment'),
    path('viewExpense/', views.viewExpense, name = 'viewExpense'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('aboutUs/', views.aboutUs, name = 'aboutUs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
