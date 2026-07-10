from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm


def home(request):
    return render(
        request,
        "home.html",
        {
            "book_count": Book.objects.count(),
            "author_count": Author.objects.count(),
        },
    )


def book_list(request):
    books = Book.objects.select_related("author").all()

    q = request.GET.get("q")

    if q:
        books = books.filter(title__icontains=q)

    return render(request, "book_list.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "book_detail.html", {"book": book})



def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm()
    return render(
        request, "book_form.html", {"form": form, "title": "Add Book"}
    )


# ---------- BOOK: UPDATE ----------
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(
        request, "book_form.html", {"form": form, "title": "Edit Book"}
    )



def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "book_confirm_delete.html", {"book": book})


def book_borrow(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.copies_available > 0:
        book.copies_available -= 1
        book.save()
    return redirect("book_detail", pk=book.pk)


def book_return(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.copies_available < book.copies_total:
        book.copies_available += 1
        book.save()
    return redirect("book_detail", pk=book.pk)



def author_list(request):
    authors = Author.objects.all()
    return render(request, "author_list.html", {"authors": authors})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, "author_detail.html", {"author": author})


def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm()
    return render(
        request, "author_form.html", {"form": form, "title": "Add Author"}
    )


def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm(instance=author)
    return render(
        request, "author_form.html", {"form": form, "title": "Edit Author"}
    )


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect("author_list")
    return render(request, "author_confirm_delete.html", {"author": author})
