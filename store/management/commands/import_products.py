import requests
from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = "Importa productos desde DummyJSON y los agrega a la base de datos"

    def handle(self, *args, **kwargs):
        url = "https://dummyjson.com/products"
        response = requests.get(url)
        data = response.json()

        for item in data.get("products", []):
            # Crear categoría si no existe
            category, _ = Category.objects.get_or_create(name=item["category"], slug=item["category"])
            
            # Crear producto
            Product.objects.get_or_create(
                title=item["title"],
                description=item["description"],
                price=item["price"],
                category=category,
                image=item.get("thumbnail", "")
            )

        self.stdout.write(self.style.SUCCESS("Productos importados correctamente"))
