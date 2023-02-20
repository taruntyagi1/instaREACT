from django.shortcuts import render, HttpResponse
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from product.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.backends.db import SessionStore
import json
from django.conf import settings
import stripe
# Create your views here.


class ProductView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class AddToCart(APIView):
    def post(self, request, product_id):
        # Retrieve the product and user
        product = Product.objects.get(id=product_id)
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)

        # Retrieve the user's cart
        cart, created = Cart.objects.get_or_create(user=user)

        # Iterate through the session cart data and add each item to the user's cart
        cart_item, created = CartItem.objects.get_or_create(
            product=product, cart=cart, user=user)
        if created:
                cart_item.quantity = 1
                cart_item.price = cart_item.product.price * cart_item.quantity
                cart_item.price = round(cart_item.price)
                cart_item.save()
                return JsonResponse({
                        'message': 'added to cart',

                    })
        else:
                return JsonResponse({
                        'message': 'already added to cart'
                    })


# class SessionCart(APIView):
#     def post(self, request):
#         user_id = request.data.get('user_id')
#         session_cart = request.data.get('cart')
#         user = User.objects.get(id=user_id)

#         # Check if the user has a cart already, if not create one
#         cart, created = Cart.objects.get_or_create(user=user)

#         for item in session_cart.values():
#             # Check if the item already exists in the user's cart
#             cart_item, created = CartItem.objects.get_or_create(
#                 product_id=item['id'], user=user, cart=cart)

#             # If the item already exists in the cart, update the quantity and price
#             if not created:
#                 cart_item.quantity += item['quantity']
#                 cart_item.price += item['price']
#             else:
#                 # If the item is not already in the cart, create a new cart item
#                 cart_item.quantity = item['quantity']
#                 cart_item.price = item['price']

#             cart_item.save()

#         return JsonResponse({'message': 'session products added to cart'})


class Session_cart_view(APIView):
    def post(self, request):
        print('session code is called')
        user_id = request.data.get('user_id')
        session_cart = request.data.get('cart')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'message': 'User not found'
            }, status=400)

        try:
            cart = Cart.objects.get(user=user)
            print('cart_id', cart.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
            print('cart_created', cart.id)

        for items in session_cart.values():
            product = Product.objects.get(id=items['id'])
            cart_item = CartItem.objects.filter(
                product=product, user=user, cart=cart).first()

            if cart_item:
                cart_item.quantity += items['quantity']
                cart_item.price += items['price']
                cart_item.price = round(cart_item.price)
            
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product, user=user, cart=cart, quantity=items['quantity'], price=items['price'])

        return JsonResponse({
            'message': 'added to cart'
        })


class CartView(APIView):
    def get(self, request):
        cart = CartItem.objects.get(user=request.user.id)
        serializers = cartserializer(cart).data
        return Response(serializers, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user:

                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,
                                     'email': user.email,
                                     'id': user.id,
                                     'username': user.username}, status=status.HTTP_200_OK)
                else:
                    content = {'detail': _('User account not active.')}
                    return Response(content,
                                    status=status.HTTP_401_UNAUTHORIZED)

            else:
                content = {'detail':
                           _('Unable to login with provided credentials.')}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    def post(self, request):
        userID = request.data.get('userID')
        user = User.objects.get(id=userID)
        cartitem = CartItem.objects.filter(user=user)
        total_price = 0
        if cartitem:
            for item in cartitem:
                total_price += item.price
            serializer = CartItemSerializer(cartitem, many=True).data
            return JsonResponse({'cart_items': serializer, 'total_price': total_price, 'price': item.price}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST',])
def increase_cart(request):
    user_id = request.data.get('userID')
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    # product = Product.objects.get(id = product_id)
    cart_item = CartItem.objects.get(product=product, user=user)
    cart_item.quantity += 1
    cart_item.price = cart_item.product.price * cart_item.quantity
    
    if cart_item.quantity > 4:
        return Response({
            'message': 'you can only buy 4 items'
        })
    cart_item.save()
    return JsonResponse({
        'message': cart_item.quantity,
        'price': cart_item.price,
        'cart' : cart_item,
    })


@csrf_exempt
@api_view(['POST',])
def decrease_cart(request):
    user_id = request.data.get('userID')
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    cart_item = CartItem.objects.get(product=product, user=user)
    cart_item.quantity -= 1
    cart_item.price = round(cart_item.product.price - cart_item.quantity)
    
    if cart_item.quantity < 1:
        cart_item.delete()
        return Response({
            'message': 'cart item deleted'
        })
    cart_item.save()
    return JsonResponse({
        'message': cart_item.quantity,
        'price' : cart_item.price,
        'cart' : cart_item,
        
    })


class CountView(APIView):
    def post(self, request):
        userID = request.data.get('userID')
        try:
            user = User.objects.get(id=userID)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        count_cart = CartItem.objects.filter(user=user)
        count = 0
        for items in count_cart:
            count += items.quantity

        return JsonResponse({'message': count})


class Cart_item_count(APIView):
    def get(self, request):
        user_id = request.GET.get('userID')
        try:
            user = User.objects.get(id=user_id)
            cart_item = CartItem.objects.filter(user=user)
            count = 0
            count = cart_item.count()
            return JsonResponse({
                'message': count
            })
        except User.DoesNotExist:
            return JsonResponse({
                'message': 'user does not exists'
            })


class User_address(APIView):

    def get(self, request):
        address = UserAddress.objects.all()
        serializer = AdressSerializer(address, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class User_register(APIView):

    def get(self, request):
        user = User.objects.all()
        serializer = Userserializer(user, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        username = request.data.get('username')
        phone = request.data.get('phone_number')
        password = request.data.get('password')
        repeat_password = request.data.get('repeat_password')
        if password == repeat_password:
            password = make_password(password)
        else:
            return JsonResponse({
                'invalid': 'password not match'
            })
        user = User.objects.create(first_name=first_name, last_name=last_name,
                                   email=email, username=username, phone_number=phone, password=password)
        serialzier = Userserializer(user).data
        return Response(serialzier, status=status.HTTP_200_OK)


class AddressView(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        print(user_id)
        user = User.objects.get(id=user_id)
        address = UserAddress.objects.filter(user=user)
        full_name = user.first_name + "  " + user.last_name
        serializer = AdressSerializer(address, many=True).data
        return Response({'address': serializer, 'name': full_name})

    def post(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        address = request.data.get('address')
        default_address = request.data.get('default_address')
        if UserAddress.objects.filter(user=user).exists():
            return JsonResponse({
                'message': 'user address is already exists'
            })
        else:

            is_default = False
            if address == default_address:
                is_default = True
            else:
                is_default = False

            user_address = UserAddress.objects.create(
                user=user,
                address=address,
                default_address=is_default
            )
            serializer = AdressSerializer(user_address).data
            return Response(serializer, status=status.HTTP_201_CREATED)


class CArtCount(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        cart = Cart.objects.filter(user=user)
        return Response({
            'message': 'cart is found'
        })


class RemoveItem(APIView):
    def post(self, request):
        user_id = request.data.get('userID')
        product_id = request.data.get('product_id')
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(
            product=product, user=user, cart=cart)
        if cart_item:
            cart_item.delete()
            return JsonResponse({
                'message': 'item deleted succesfully',
                'cart' : cart_item
            })
        return JsonResponse({
            'message': 'cart item does not found'
        })


class VoucherView(APIView):

    def get(self, request):
        voucher = Voucher.objects.filter(is_active=True)
        serializer = VoucherSerializer(voucher, many=True).data
        return Response(serializer, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        voucher_code = request.data.get('voucher_code')
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
        product = Product.objects.get(id=product_id)
        try:
            voucher = Voucher.objects.get(code=voucher_code, is_active=True)
        except Voucher.DoesNotExist:
            return JsonResponse({
                'message' : 'voucher is not found'
            })
        cart_item = CartItem.objects.get(product = product,user = user,cart = cart) 
        if cart_item.price < voucher.discount_value:
            return JsonResponse({
                'message' : f'min spend value is {voucher.discount_value}'
            })
        if voucher and voucher.discount_type ==2:
            cart_item.discount_amount = voucher.discount_value
            if cart_item.discount_amount > voucher.max_discount:
                cart_item.discount_amount = voucher.max_discount
            cart_item.price = cart_item.price - cart_item.discount_amount
            cart_item.price = round(cart_item.price)
            cart_item.save()
            cart_item.save()
            voucher.is_active = False
            voucher.save()
            
            return JsonResponse({
                'message' : f'coupon is applied {cart_item.discount_amount}'
            })
        if voucher and voucher.discount_type ==1:
            cart_item.discount_amount = voucher.discount_value
            if cart_item.discount_amount > voucher.max_discount:
                cart_item.discount_amount = voucher.max_discount
            cart_item.price = cart_item.price - (cart_item.discount_amount/100)
            cart_item.price = round(cart_item.price)
            cart_item.save()
            voucher.is_active = False
            voucher.save()
            return JsonResponse({
                'message' : f'coupon is applied {cart_item.discount_amount}'
            })
        else:
            return JsonResponse({
                'message' : 'voucher not found'
            })
       
        
        

class CreateCheckout(APIView):
    def post(self,request):
        user_id = request.data.get('user_id')
        user = User.objects.get(user = user)
        cart = Cart.objects.get(user  = user)
        product_id = request.data.get('product_id')
        product = Product.objects.get(id = product_id)
        cart_items = CartItem.objects.get(cart = cart,user = user)
        stripe.api_key = settings.STRIPE_KEY
        checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'INR',
                    'product_data': {
                    'name': product.title,
                    },
                    'unit_amount': int(cart_items.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
      
    )


    
        
            
        
            

