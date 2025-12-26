import os
import django

# ----------------------------------------
# 1. Cargar entorno Django
# ----------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from products.models import Category, Product

# ----------------------------------------
# 2. Crear categoría si no existe
# ----------------------------------------
categoria, creada = Category.objects.get_or_create(name="Moda")
print(f"Categoría usada: {categoria.name}")

# ----------------------------------------
# 3. Lista de productos de prueba
# ----------------------------------------
productos = [
    ("Camiseta Premium", 19.99),
    ("Pantalón Vaquero", 39.99),
    ("Chaqueta Deportiva", 49.99),
    ("Sudadera Oversize", 29.99),
    ("Zapatillas Running", 59.99),
    ("Gorra Urbana", 14.99),
    ("Cinturón de Piel", 24.99),
    ("Calcetines Deportivos (3 pack)", 9.99),
    ("Camisa Formal", 34.99),
    ("Reloj Minimalista", 89.99),
]

# ----------------------------------------
# 4. Crear productos evitando duplicados
# ----------------------------------------
for nombre, precio in productos:

    producto, creado = Product.objects.get_or_create(
        name=nombre,
        defaults={
            "description": "Producto autogenerado para pruebas.",
            "price": precio,
            "stock": 50,               # Stock inicial
            "category": categoria
        }
    )

    if creado:
        print(f"✔ Producto creado: {nombre}")
    else:
        print(f"ℹ Producto ya existía: {nombre}")

print("\n✔️ Finalizado correctamente: productos cargados.\n")
