from django.shortcuts import redirect, render
from django.views import View
from .models import MenuItem, Order
from django.core.mail import send_mail
from yenepay import Client, Item, Cart
from django.db.models import Q
from .models import MenuItem, Category, Order

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class OrderView(View):
    def get(self, request, *args, **kwargs):
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        main_courses = MenuItem.objects.filter(category__name__contains='Main Course')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        context = {
            'appetizers': appetizers,
            'main_courses': main_courses,
            'drinks': drinks,
            'desserts': desserts,
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        price = 0
        item_ids = []
        order_items = {
            'items': []
        }
        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        order = Order.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        # confirmation mail
        body = ("We've recived your Order. Your order will be delivered soon.\n"
                f"Total Price: {price}\n"
                "Thanks for using our services.\n"
                "Your order is on it's way!")
        send_mail(
            "Your order is on it's way!",
            body,
            'example@exam.com',
            [email],
            fail_silently=False
        )
        order.items.add(*item_ids)
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-conf', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        return render(request, 'customer/order_confirmation.html', context)


class OrderPayConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        MERCHANT_ID = "38017"
        client = Client(merchant_id=MERCHANT_ID)

        items = [Item(item.name, float(item.price), 1) for item in order.items.all()]
        cart = Cart(*items)

        cart_checkout = client.get_cart_checkout(items=cart)
        checkout_url = cart_checkout.get_url()
        return redirect(checkout_url)

    # need correction, it doesn't take the response and redirect
    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        client = Client(merchant_id="38017", token="abcd")
        merchant_order_id = "0000"
        transaction_id = "abcd"

        response = client.check_pdt_status(merchant_order_id, transaction_id)

        if response.result == "SUCCESS" and response.status == "Paid":
            order.is_paid = True
            return render(request, 'customer/order_pay_confirmation.html')
        else:
            return render(request, 'customer/payment_failure.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
