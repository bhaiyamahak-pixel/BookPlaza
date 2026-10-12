from django.shortcuts import render,redirect
from .models import Book,Customer, CartOrder, CartOrderItem
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

@login_required(login_url='login')
def your_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).select_related('book').order_by('-order_date')

    return render(request, 'your_orders.html', {
        'orders': orders
    })

def home_view(request):
    all_books = Book.objects.all()
    context={ 
        'books':all_books
    }
    return render(request, "home.html",context)

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        Book.objects.create(
            title=title,
            author=author,
            price=price,
            image=image,
            category=category,
        )
        return redirect('home')

    return render(request, 'add.html')

def edit_book(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.category = request.POST.get('category')
        book.stock = request.POST.get('stock') or book.stock
        book.description = request.POST.get('description')
        image = request.FILES.get('image')
        if image:
            book.image = image
        book.save()
        return redirect('home')

    return render(request, 'edit.html', {'book': book})

def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('home')
from .models import Customer, CartOrder, CartOrderItem

def register_view(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=phone).exists():
            messages.error(
                request,
                'This phone number is already registered. Please login.'
            )
            return redirect('login')

        user = User.objects.create_user(
            username=phone,
            email=email,
            first_name=name,
            password=password
        )

        customer = Customer.objects.create(
            name=name,
            phone=phone,
            email=email
        )

        request.session['customer_id'] = customer.id
        request.session['customer_name'] = customer.name

        login(request, user)

        next_url = request.GET.get('next')

        if next_url:
            return redirect(next_url)

        return redirect('home')

    # This is required when opening /register/ normally
    return render(request, 'register.html')
        
        
def add_to_cart(request, pk):

    book = get_object_or_404(Book, pk=pk)

    # Get existing cart from session
    cart = request.session.get('cart', {})

    # Add book to cart
    cart[str(pk)] = cart.get(str(pk), 0) + 1

    # Save cart in session
    request.session['cart'] = cart
    request.session.modified = True

    # Return to the page from where the book was added
    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)

    return redirect('view_cart')

@login_required(login_url='login')
def direct_place_order(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')

        quantity = int(request.POST.get('quantity', 1))

        if not customer_name or not phone or not address or not city or not pin_code:
            messages.error(request, 'Please fill all the required details.')

            return render(request, 'direct_order.html', {
                'book': book
            })

        if quantity > book.stock:

            messages.error(
                request,
                'Not enough stock available.'
            )

            return render(request, 'direct_order.html', {
                'book': book
            })


        order = Order.objects.create(

            user=request.user,

            customer_name=customer_name,

            phone=phone,

            address=address,

            city=city,

            pin_code=pin_code,

            book=book,

            quantity=quantity

        )


        # Reduce stock

        book.stock -= quantity
        book.save()


        return render(request, 'order_success.html', {
            'order': order
        })


    return render(request, 'direct_order.html', {
        'book': book
    })

def view_cart(request):

    cart = request.session.get('cart', {})

    books = Book.objects.filter(pk__in=cart.keys())

    cart_items = []
    total = 0

    for book in books:

        quantity = cart[str(book.pk)]

        subtotal = book.price * quantity

        total += subtotal

        cart_items.append({
            'book': book,
            'qty': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, pk):

    cart = request.session.get('cart', {})

    cart.pop(str(pk), None)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')

def place_order(request):
    cart = request.session.get('cart', {})
    customer_id = request.session.get('customer_id')
    if not cart or not customer_id:
        return redirect('home')
    customer = Customer.objects.get(pk=customer_id)
    order = CartOrder.objects.create(customer=customer)
    for book in Book.objects.filter(pk__in=cart.keys()):
        CartOrderItem.objects.create(order=order, book=book, quantity=cart[str(book.pk)])
    request.session['cart'] = {}
    return render(request, 'order_success.html', {'order': order})

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'book_detail.html', {'book': book})

def home(request):
    featured_books = Book.objects.all()[:4]
    return render(request, 'home.html', {
        'featured_books': featured_books
    })


def categories(request):
    categories = [
        ("fiction", "📖 Fiction"),
        ("non_fiction", "📚 Non-Fiction"),
        ("science", "🔬 Science"),
        ("history", "📜 History"),
        ("technology", "💻 Technology"),
        ("children", "👶 Children"),
        ("biography", "👤 Biography"),
        ("self_help", "🧠 Self Help"),
    ]
    return render(request, "categories.html", {
        "categories": categories
    })


def category_books(request, category):
    books = Book.objects.filter(category=category)

    return render(
        request,
        "category_books.html",
        {
            "books": books,
            "category": category
        }
    )
def user_login(request):

    if request.method == 'POST':

        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=phone,
            password=password
        )

        if user is not None:

            login(request, user)

            # Find the BookPlaza Customer
            customer = Customer.objects.filter(phone=phone).first()

            if customer:
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('home')

        messages.error(request, 'Invalid phone number or password.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def about_us(request):
    return render(request, 'about_us.html')

def search_books(request):
    query = request.GET.get('q', '').strip()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
    else:
        books = Book.objects.none()

    return render(request, 'search_results.html', {
        'books': books,
        'query': query,
    })
@login_required(login_url='login')
def cart_place_order(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('view_cart')

    books = Book.objects.filter(pk__in=cart.keys())

    cart_items = []
    total = 0

    for book in books:

        quantity = cart[str(book.pk)]

        subtotal = book.price * quantity

        total += subtotal

        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')

        if not customer_name or not phone or not address or not city or not pin_code:

            messages.error(
                request,
                'Please fill all the delivery details.'
            )

            return render(request, 'cart_checkout.html', {
                'cart_items': cart_items,
                'total': total
            })

        # Check stock first

        for book in books:

            quantity = cart[str(book.pk)]

            if quantity > book.stock:

                messages.error(
                    request,
                    f'Not enough stock available for {book.title}.'
                )

                return redirect('view_cart')


        # Create an Order for every book

        for book in books:

            quantity = cart[str(book.pk)]

            Order.objects.create(
                user=request.user,
                customer_name=customer_name,
                phone=phone,
                address=address,
                city=city,
                pin_code=pin_code,
                book=book,
                quantity=quantity
            )

            # Reduce stock

            book.stock -= quantity
            book.save()


        # Clear cart after successful order

        request.session['cart'] = {}
        request.session.modified = True


        return redirect('your_orders')


    return render(request, 'cart_checkout.html', {
        'cart_items': cart_items,
        'total': total
    })