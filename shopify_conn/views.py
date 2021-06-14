import os
import binascii

from django.shortcuts import render, redirect

import shopify
from shopify import Session as ShopifySession

API_KEY    = ''
API_SECRET = ''

# Create your views here.
def index(request, *args, **kwargs):
    # reference: https://github.com/Shopify/shopify_python_api
    
    if request.method == 'GET':
        try:
            # hmac, #tstamp
            hmac   = request.GET['hmac']
            tstamp = request.GET['timestamp']

            ShopifySession.setup(api_key=API_KEY, secret=API_SECRET)
            shop_url = "aa-sells-stuff.myshopify.com"
            api_version = "2020-10"
            state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            redirect_uri = "http://localhost:8000/shopify/redirected"
            scopes = ['read_products', 'read_orders']

            newSession = ShopifySession(shop_url, api_version)
            auth_url = newSession.create_permission_url(scopes, redirect_uri)
            print("AUTH URL", auth_url)

            print("REDIRECTING")
            return redirect(auth_url)
            #access_token = ShopifySession(shop_url, api_version).request_token({"hmac": hmac, })
        except KeyError as ke:
            print("KeyError", ke)
            

    return render(request, 'shopify_conn/index.html')


def redirected(request, *args, **kwargs):
    print("REDIRECTED REQUEST",request)
    print("REDIRECTED KWARGS", args)
    print("REDIRECTED ARGS", kwargs)
    request_params = request.GET.copy()

    print("REQUEST PARAMS", request_params)

    shop_url = "aa-sells-stuff.myshopify.com"
    api_version = "2020-10"

    session = ShopifySession(shop_url, api_version)
    access_token = session.request_token(request_params)

    print("ACCESS TOKEN", access_token)

    newSession = ShopifySession(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(newSession)

    shop = shopify.Shop.current()
    product = shopify.Product.find()
    print(product)


    return render(request, 'shopify_conn/redirected.html')