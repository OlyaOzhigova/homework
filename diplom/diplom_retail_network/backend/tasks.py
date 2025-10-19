from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    #асинхронная отправка подтверждения заказа покупателю
    try:
        order = Order.objects.select_related('user', 'contact').prefetch_related(
            'ordered_items__product_info__product',
            'ordered_items__product_info__shop'
        ).get(id=order_id)
        
        subject = f'Подтверждение заказа #{order.id}'
        
        # красивый контент для письма
        context = {
            'order': order,
            'user': order.user,
            'items': order.ordered_items.all()
        }
        
        html_message = render_to_string('email/order_confirmation.html', context)
        plain_message = render_to_string('email/order_confirmation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Email sent to {order.user.email} for order #{order.id}"
    
    except Order.DoesNotExist:
        return f"Order #{order_id} not found"

@shared_task
def send_order_to_admin_email(order_id):
    
    #асинхронная отправка накладной администратору
    try:
        order = Order.objects.select_related('user', 'contact').prefetch_related(
            'ordered_items__product_info__product',
            'ordered_items__product_info__shop'
        ).get(id=order_id)
        
        subject = f'Новый заказ #{order.id} от {order.user.email}'
        
        context = {
            'order': order,
            'user': order.user,
            'contact': order.contact,
            'items': order.ordered_items.all()
        }
        
        html_message = render_to_string('email/order_to_admin.html', context)
        plain_message = render_to_string('email/order_to_admin.txt', context)
        
        # отправляем администратору
        admin_email = 'olya.ozhigova@gmail.com'
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Order notification sent to admin for order #{order.id}"
    
    except Order.DoesNotExist:
        return f"Order #{order_id} not found"
