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
        product_data={"name": "Payment for courses"},
    )
    return price.id

def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str) -> str:
    """Создает сессию оплаты и возвращает ссылку на оплату."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id, "quantity": 1}],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",)
    return session.url
    # return session.get("id"), session.get("url")


def retrieve_stripe_session(session_id: str):
    """Получает данные о сессии оплаты из Stripe."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session
