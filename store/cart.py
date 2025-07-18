class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {
                "name": product.name,
                "price": str(product.price),
                "quantity": quantity,
                "image": product.image.url if product.image else "",
            }
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def get_total(self):
        return sum(float(item["price"]) * item["quantity"] for item in self.cart.values())
