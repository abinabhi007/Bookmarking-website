from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, BookmarkForm, ContactForm, CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Bookmark
from django.core.paginator import Paginator


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.username = form.cleaned_data['email']  # Set username as email
            user.save()

            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors above.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    search_query = request.GET.get('search', '')
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-added_time')
    
    # Filtering based on search query
    if search_query:
        bookmarks = bookmarks.filter(title__icontains=search_query) | bookmarks.filter(url__icontains=search_query)

    # Pagination
    paginator = Paginator(bookmarks, 2)  # Show 6 bookmarks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'bookmarks': page_obj,  # Use the paginated object
        'search_query': search_query
    })


@login_required
def edit_bookmark(request, bookmark_id):
    # Use get_object_or_404 to ensure the bookmark exists, or return a 404 error.
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)

    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bookmark updated successfully!')
            return redirect('my_collections')  # Redirect to my collections page
    else:
        form = BookmarkForm(instance=bookmark)

    return render(request, 'edit_bookmark.html', {'form': form, 'bookmark': bookmark})

@login_required
def delete_bookmark(request, id):
    # Get the bookmark and ensure it belongs to the user
    bookmark = get_object_or_404(Bookmark, id=id, user=request.user)

    if request.method == 'POST':
        # Delete the bookmark on POST request (form submission)
        bookmark.delete()
        return redirect('my_collections')  # Redirect after deletion
    
    # Render confirmation page for GET request
    return render(request, 'confirm_delete.html', {'bookmark': bookmark})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def about_us(request):
    return render(request, 'about_us.html')

@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()  # This will create a new ContactMessage instance
            # Optionally, you could send an email notification here
            return redirect('contact_us')  # Redirect to the same page or a success page
    else:
        form = ContactForm()  # Create a new empty form
    return render(request, 'contact_us.html', {'form': form})

@login_required
def my_collections(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            if bookmarks.count() >= 5:
                messages.error(request, 'You can only add up to 5 bookmarks.')
            else:
                bookmark = form.save(commit=False)
                bookmark.user = request.user
                bookmark.save()
                messages.success(request, 'Bookmark added successfully!')
                return redirect('my_collections')  # Redirect to the same page

    else:
        form = BookmarkForm()

    return render(request, 'my_collections.html', {
        'form': form,
        'bookmarks': bookmarks
    })



@login_required
def bookmark_list(request):
    search_query = request.GET.get('search', '')
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-added_time')
    
    # Filtering based on search query
    if search_query:
        bookmarks = bookmarks.filter(title__icontains=search_query) | bookmarks.filter(url__icontains=search_query)

    # Pagination
    paginator = Paginator(bookmarks, 2)  # Show 6 bookmarks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bookmark_list.html', {
        'bookmarks': page_obj,  # Use the paginated object
        'search_query': search_query
    })