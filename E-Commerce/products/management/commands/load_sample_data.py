import os
import urllib.request
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import io
from products.models import Category, Product

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_or_fallback_image(url, fallback_title, fallback_color):
    """Attempts to download high-res real photo, falling back to local PIL generator if offline."""
    if url:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                return resp.read(), 'jpg'
        except Exception:
            pass

    # Offline PIL generator fallback
    size = (600, 450)
    img = Image.new('RGB', size, color=fallback_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(20, 20), (size[0]-20, size[1]-20)], outline=(255, 255, 255), width=3)
    draw.text((size[0]//2, size[1]//2), fallback_title[:25], fill=(255, 255, 255), anchor='mm')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue(), 'png'


class Command(BaseCommand):
    help = 'Seeds initial sample categories and products with real photos and Indian Rupee (INR) prices.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding sample categories and products with real photos...'))

        sample_categories = [
            {
                'name': 'Electronics',
                'description': 'High quality gadgets, audio gear, computing accessories, and peripherals.',
                'image_url': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80',
                'color': (41, 128, 185),
            },
            {
                'name': 'Fashion & Apparel',
                'description': 'Contemporary apparel, footwear, everyday casuals, and modern accessories.',
                'image_url': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=80',
                'color': (155, 89, 182),
            },
            {
                'name': 'Home & Living',
                'description': 'Essential modern home decor, kitchen appliances, and comfort furnishings.',
                'image_url': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80',
                'color': (39, 174, 96),
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Durable fitness equipment, workout gear, and athletic accessories.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&q=80',
                'color': (230, 126, 34),
            },
        ]

        cat_objects = {}
        for cat_info in sample_categories:
            category, created = Category.objects.get_or_create(
                name=cat_info['name'],
                defaults={'description': cat_info['description']}
            )
            # Ensure real image is attached
            img_data, ext = fetch_or_fallback_image(cat_info['image_url'], category.name, cat_info['color'])
            category.image.save(f"{category.slug}.{ext}", ContentFile(img_data), save=True)
            cat_objects[cat_info['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f"  + Created Category: {category.name}"))
            else:
                self.stdout.write(f"  * Category updated: {category.name}")

        sample_products = [
            # Electronics
            {
                'category': 'Electronics',
                'name': 'Wireless Noise-Cancelling Headphones',
                'sku': 'ELEC-WH-001',
                'price': Decimal('2499.00'),
                'stock': 25,
                'description': 'Premium over-ear wireless Bluetooth headphones with active noise cancellation and 30-hour battery life.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
                'color': (44, 62, 80),
            },
            {
                'category': 'Electronics',
                'name': 'Ultra-Slim Mechanical Keyboard',
                'sku': 'ELEC-KB-002',
                'price': Decimal('3299.00'),
                'stock': 18,
                'description': 'Compact mechanical keyboard with RGB backlighting, hot-swappable tactile switches, and dual USB-C/Bluetooth.',
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
                'color': (52, 73, 94),
            },
            {
                'category': 'Electronics',
                'name': '4K Ultra-HD Gaming Monitor 27"',
                'sku': 'ELEC-MN-003',
                'price': Decimal('18999.00'),
                'stock': 12,
                'description': '27-inch IPS 4K HDR display with 144Hz refresh rate, 1ms response time, and ultra-thin bezels for immersive gaming.',
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80',
                'color': (26, 82, 118),
            },
            {
                'category': 'Electronics',
                'name': 'Ergonomic Wireless Optical Mouse',
                'sku': 'ELEC-MS-004',
                'price': Decimal('899.00'),
                'stock': 40,
                'description': 'Comfortable contoured ergonomic mouse designed to reduce wrist strain, featuring silent clicks and long battery life.',
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80',
                'color': (33, 97, 140),
            },
            {
                'category': 'Electronics',
                'name': 'Smart Fitness Tracker Pro',
                'sku': 'ELEC-FT-005',
                'price': Decimal('1999.00'),
                'stock': 30,
                'description': 'Water-resistant fitness band with AMOLED touchscreen, SpO2 monitoring, 24/7 heart-rate tracking, and GPS.',
                'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80',
                'color': (21, 67, 96),
            },

            # Fashion
            {
                'category': 'Fashion & Apparel',
                'name': 'Classic Washed Denim Jacket',
                'sku': 'FASH-DJ-001',
                'price': Decimal('2199.00'),
                'stock': 15,
                'description': 'Timeless vintage wash denim jacket made from 100% premium cotton with button flap chest pockets and adjustable waist tabs.',
                'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&q=80',
                'color': (142, 68, 173),
            },
            {
                'category': 'Fashion & Apparel',
                'name': 'Minimalist Urban Leather Backpack',
                'sku': 'FASH-BP-002',
                'price': Decimal('1799.00'),
                'stock': 20,
                'description': 'Sleek vegan leather backpack featuring a padded 15.6-inch laptop compartment, water-resistant exterior, and hidden anti-theft pocket.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80',
                'color': (125, 60, 152),
            },
            {
                'category': 'Fashion & Apparel',
                'name': 'Breathable Lightweight Running Sneakers',
                'sku': 'FASH-SN-003',
                'price': Decimal('2499.00'),
                'stock': 22,
                'description': 'Engineered mesh sneakers with responsive cushioning foam midsole, anti-skid rubber grip, and breathable comfort upper.',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
                'color': (108, 52, 131),
            },
            {
                'category': 'Fashion & Apparel',
                'name': 'Vintage Polarized UV400 Sunglasses',
                'sku': 'FASH-SG-004',
                'price': Decimal('799.00'),
                'stock': 50,
                'description': 'Classic square-frame polarized sunglasses offering 100% UV400 protection with durable metal hinges and scratch-resistant lenses.',
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80',
                'color': (91, 44, 111),
            },

            # Home & Living
            {
                'category': 'Home & Living',
                'name': 'Ceramic Pour-Over Coffee Dripper Set',
                'sku': 'HOME-CF-001',
                'price': Decimal('1299.00'),
                'stock': 14,
                'description': 'Artisanal ceramic dripper with heat-resistant borosilicate glass carafe and reusable stainless steel mesh filter.',
                'image_url': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
                'color': (30, 132, 73),
            },
            {
                'category': 'Home & Living',
                'name': 'Aromatherapy Essential Oil Diffuser Lamp',
                'sku': 'HOME-DF-002',
                'price': Decimal('999.00'),
                'stock': 25,
                'description': 'Ultrasonic cool-mist diffuser with 7 ambient LED night light colors, auto-shutoff safety, and whisper-quiet ultrasonic operation.',
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&q=80',
                'color': (25, 111, 61),
            },
            {
                'category': 'Home & Living',
                'name': 'Ergonomic Memory Foam Contour Pillow',
                'sku': 'HOME-PL-003',
                'price': Decimal('1499.00'),
                'stock': 35,
                'description': 'Therapeutic cervical contour pillow offering targeted neck and spine support, encased in a washable bamboo fiber cover.',
                'image_url': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&q=80',
                'color': (20, 90, 50),
            },
            {
                'category': 'Home & Living',
                'name': 'Double-Wall Insulated Steel Tumbler 750ml',
                'sku': 'HOME-TM-004',
                'price': Decimal('699.00'),
                'stock': 60,
                'description': 'Vacuum insulated food-grade 18/8 stainless steel tumbler that keeps cold drinks chilled for 24 hours and hot coffee hot for 12 hours.',
                'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80',
                'color': (17, 120, 100),
            },

            # Sports & Fitness
            {
                'category': 'Sports & Fitness',
                'name': 'High-Density Non-Slip Yoga Mat',
                'sku': 'SPRT-YM-001',
                'price': Decimal('899.00'),
                'stock': 30,
                'description': 'Eco-friendly TPE 6mm extra-thick yoga and exercise mat with textured dual-sided grip and carrying strap included.',
                'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&q=80',
                'color': (211, 84, 0),
            },
            {
                'category': 'Sports & Fitness',
                'name': 'Adjustable Quick-Select Dumbbell (Pair)',
                'sku': 'SPRT-DB-002',
                'price': Decimal('4999.00'),
                'stock': 8,
                'description': 'Space-saving adjustable dumbbell pair with rapid dial weight selection from 5 lbs up to 52.5 lbs per hand.',
                'image_url': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?w=800&q=80',
                'color': (186, 74, 0),
            },
            {
                'category': 'Sports & Fitness',
                'name': 'Speed Jump Rope with Digital Counter',
                'sku': 'SPRT-JR-003',
                'price': Decimal('399.00'),
                'stock': 50,
                'description': 'Tangle-free steel cable jump rope with smooth 360-degree ball bearings and LCD display tracking jumps and calorie burn.',
                'image_url': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=800&q=80',
                'color': (160, 64, 0),
            },
        ]

        created_count = 0
        for p in sample_products:
            category = cat_objects[p['category']]
            product, created = Product.objects.get_or_create(
                sku=p['sku'],
                defaults={
                    'category': category,
                    'name': p['name'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'description': p['description'],
                    'is_active': True,
                }
            )
            # Update price and ensure real image is saved locally
            product.price = p['price']
            img_data, ext = fetch_or_fallback_image(p['image_url'], product.name, p['color'])
            product.image.save(f"{product.sku}.{ext}", ContentFile(img_data), save=True)

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + Added Product: {product.name} (Rs. {product.price})"))
            else:
                self.stdout.write(f"  * Updated Product: {product.name} (Rs. {product.price})")

        self.stdout.write(self.style.SUCCESS(
            f"\nSample data loading complete! Successfully loaded {len(sample_categories)} categories and {len(sample_products)} products with real images."
        ))
