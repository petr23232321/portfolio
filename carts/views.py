from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from store.models import Products
from carts.models import Cart, CartItem

# adding cart

def _cart_id(request):   #_ is private
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart:cart')



def cart(request, total=0, quantity=0, cart_items=None ):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectNotExists:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }
    return render(request, 'carts/cart.html', context)