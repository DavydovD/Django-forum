from django.shortcuts import render
from .coingate.client import CoinGateV2Client, CoinGateV2Order
from .models import Order
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def create_order(request):

    if request.method == "POST":
        client = CoinGateV2Client("3728", "czikeDU_RiX6y2M-npUPB4i9wJWbb5kxTZqkERU-")
        host = request.get_host()
        order = Order.objects.create()
        order.save()

        new_order = CoinGateV2Order.new(
            order.id,
            10.0,
            "USD",
            "USD",
            title='Premium subscription',
            callback_url='http://{}{}'.format(host, reverse('payments:notification')),
            cancel_url='http://{}{}'.format(host, reverse('forum:home')),
            success_url='http://{}{}'.format(host, reverse('forum:home')),
            token=order.token
        )

        placed_order = client.create_order(new_order)
        
        return HttpResponseRedirect(placed_order.payment_url)

    return render(request, 'payments/get_premium.html')


@csrf_exempt
def payment_notification(request):
    print('notification')

    if request.method == 'POST':
        token = request.GET.get('token', '')
        order = Order.objects.get(token=token)
        print(token)

    return render(request, 'payments/get_premium.html')
