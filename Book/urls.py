from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('borrow-history/', views.borrow_history, name='borrow_history'),
    path('add_review/<int:book_id>/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('notification/', views.notification, name='notification'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('category/<str:category>/', views.books_by_category, name='books_by_category'),
    
]