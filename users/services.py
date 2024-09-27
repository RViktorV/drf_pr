import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=name)
    return product.id

def create_stripe_price(product_id: str, amount: int) -> str:
    """Создает цену для продукта в Stripe и возвращает ID цены."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,
        currency="rub",
    )
    return price.id

def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """Создает сессию оплаты в Stripe и возвращает ID и URL сессии."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return {
        "id": session.id,  # session_id
        "url": session.url  # ссылка на оплату
    }

def retrieve_stripe_session(session_id: str) -> stripe.checkout.Session:
    """Возвращает информацию о сессии Stripe по session_id."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session