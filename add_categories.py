#!/usr/bin/env python
"""
Script para agregar categorías al sistema
Ejecutar con: python manage.py shell < add_categories.py
"""

from events.models import Category

# Definir las categorías con sus slugs
categories = [
    {'name': 'Música', 'slug': 'musica'},
    {'name': 'Deportes', 'slug': 'deportes'},
    {'name': 'Tecnología', 'slug': 'tecnologia'},
    {'name': 'Gastronomía', 'slug': 'gastronomia'},
    {'name': 'Arte', 'slug': 'arte'},
    {'name': 'Cine', 'slug': 'cine'},
    {'name': 'Teatro', 'slug': 'teatro'},
    {'name': 'Educación', 'slug': 'educacion'},
    {'name': 'Negocios', 'slug': 'negocios'},
    {'name': 'Salud y Bienestar', 'slug': 'salud-bienestar'},
    {'name': 'Familia', 'slug': 'familia'},
    {'name': 'Moda', 'slug': 'moda'},
    {'name': 'Libros', 'slug': 'libros'},
    {'name': 'Juegos', 'slug': 'juegos'},
    {'name': 'Fotografía', 'slug': 'fotografia'},
    {'name': 'Viajes', 'slug': 'viajes'},
    {'name': 'Naturaleza', 'slug': 'naturaleza'},
    {'name': 'Social', 'slug': 'social'},
    {'name': 'Beneficencia', 'slug': 'beneficencia'},
    {'name': 'Otros', 'slug': 'otros'},
]

print("Agregando categorías...")
count = 0
for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name']}
    )
    if created:
        print(f"✓ Creada: {cat.name}")
        count += 1
    else:
        print(f"- Ya existe: {cat.name}")

print(f"\n{count} categorías creadas, {len(categories) - count} ya existían")
print(f"Total de categorías: {Category.objects.count()}")
