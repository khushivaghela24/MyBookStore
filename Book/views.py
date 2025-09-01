from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review, Borrow
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    general_books = Book.objects.filter(category='General')
    story_books = Book.objects.filter(category='Story')
    study_books = Book.objects.filter(category='Study')

    return render(request, 'home.html', {
        'general_books': general_books,
        'story_books': story_books,
        'study_books': study_books,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

def search_books(request):
    query = request.GET.get('q')
    if query:
        exact_match = Book.objects.filter(title__iexact=query).first()
        if exact_match:
            return redirect('book_detail', book_id=exact_match.id)
        matches = Book.objects.filter(Q(title__icontains=query))
        return render(request, 'search_result.html', {'query': query, 'matches': matches})
    return redirect('home')

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        duration = request.POST.get('duration')
        Borrow.objects.create(book=book, user=request.user, duration=duration)
        messages.success(request, "Book borrowed successfully!")
        return redirect('book_detail', book_id=book.id)
    return render(request, 'borrow_form.html', {'book': book})

@login_required
def borrow_history(request):
    borrowed_books = Borrow.objects.filter(user=request.user).select_related('book').order_by('-borrowed_at')
    return render(request, 'borrow_history.html', {'borrowed_books': borrowed_books})

def category_books(request, category):
    books = Book.objects.filter(category=category.capitalize())
    return render(request, 'category_books.html', {
        'books': books,
        'category': category.capitalize()
    })

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Review.objects.create(book=book, user=request.user, content=content)
        return redirect('book_detail', book_id=book.id)
    return redirect('book_detail', book_id=book.id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        review.content = content
        review.save()
        return redirect('book_detail', book_id=review.book.id)
    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    review.delete()
    return redirect('book_detail', book_id=book_id)

@login_required
def notification(request):
    today = timezone.now().date()
    alerts = []
    borrows = Borrow.objects.filter(user=request.user)
    for borrow in borrows:
        if borrow.duration == '1 Week':
            due_date = borrow.borrowed_at.date() + timedelta(days=7)
        else:
            due_date = borrow.borrowed_at.date() + timedelta(days=15)

        if 0 <= (due_date - today).days <= 3:
            alerts.append({
                'book': borrow.book,
                'due_date': due_date,
                'days_left': (due_date - today).days
            })

    return render(request, 'notification.html', {'alerts': alerts})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def books_by_category(request, category):
    books = Book.objects.filter(category__iexact=category)
    return render(request, 'books_by_category.html', {
        'category': category.title(),
        'books': books
    })