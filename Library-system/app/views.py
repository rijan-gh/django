from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Book 
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        data = []
        for b in books:
            data.append({
                "id": b.id,
                "name": b.name,
                "author": b.author,
                "publication": b.publication
            })
        return JsonResponse(data, safe=False)
    
    return render(request, 'book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_create.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_update.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})