"""
Management command: seed_products

Populates the database with 8 categories and 12 products.

Usage:
    python manage.py seed_products
    python manage.py seed_products --fresh    # wipe existing first

Uses update_or_create keyed on slug, so it's idempotent — safe to
run repeatedly. Each product gets both an `image_url` (Unsplash) and
an empty `image` field (ImageField), so you can later upload a real
photo in admin and it will override the URL in templates.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Category, Product


CATEGORIES = [
    {
        "name": "Serums & Oils",
        "icon": "bi-droplet",
        "tint": "#F3C9A8",
        "description": "Concentrated treatments that target specific concerns.",
        "order": 1,
    },
    {
        "name": "Moisturisers",
        "icon": "bi-moisture",
        "tint": "#E8B4B8",
        "description": "Creams and gels that lock in hydration and support the barrier.",
        "order": 2,
    },
    {
        "name": "Cleansers",
        "icon": "bi-brightness-high",
        "tint": "#BFD8D2",
        "description": "Gentle daily cleansers that lift dirt without stripping.",
        "order": 3,
    },
    {
        "name": "Sun Care",
        "icon": "bi-sun",
        "tint": "#F7E1A0",
        "description": "Broad-spectrum SPF that disappears into every skin tone.",
        "order": 4,
    },
    {
        "name": "Body Care",
        "icon": "bi-flower3",
        "tint": "#E7D3C6",
        "description": "Scrubs and butters for soft, velvety body skin.",
        "order": 5,
    },
    {
        "name": "Hair Care",
        "icon": "bi-stars",
        "tint": "#D9C7E8",
        "description": "Serums and oils for shine, smoothness and strength.",
        "order": 6,
    },
    {
        "name": "Makeup",
        "icon": "bi-palette",
        "tint": "#F0C0C8",
        "description": "Skin-loving colour that cares while it wears.",
        "order": 7,
    },
    {
        "name": "Masks & Mists",
        "icon": "bi-moon-stars",
        "tint": "#C9E0E8",
        "description": "Weekly treatments and refreshing mists for instant pick-me-ups.",
        "order": 8,
    },
]


PRODUCTS = [
    # 1
    {
        "name": "Vitamin C Serum",
        "category": "Serums & Oils",
        "tagline": "Brightening 15% Vitamin C + Ferulic",
        "description": (
            "A stabilised 15% L-ascorbic acid serum boosted with ferulic acid "
            "and vitamin E to visibly brighten, even tone and defend against "
            "daily environmental stress. The lightweight, fast-absorbing texture "
            "layers cleanly under sunscreen and makeup."
        ),
        "ingredients": (
            "Aqua, L-Ascorbic Acid 15%, Propanediol, Ferulic Acid, Tocopherol, "
            "Sodium Hyaluronate, Glycerin, Panthenol"
        ),
        "benefits": (
            "Visibly brightens dull, uneven skin\n"
            "Fades the look of dark spots over 8 weeks\n"
            "Antioxidant defence against pollution\n"
            "Lightweight, non-sticky finish"
        ),
        "how_to_use": (
            "In the morning, apply 3–4 drops to clean, dry skin before "
            "moisturiser. Follow with SPF. Introduce gradually: every other day "
            "for the first week."
        ),
        "price": "48.00",
        "compare_at_price": "60.00",
        "rating": "4.90",
        "reviews_count": 412,
        "size": "30 ml",
        "skin_type": "all",
        "accent_color": "#F3C9A8",
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": True,
        "order": 1,
    },
    # 2
    {
        "name": "Rose Face Oil",
        "category": "Serums & Oils",
        "tagline": "Damask rose & squalane overnight elixir",
        "description": (
            "A silky, fast-absorbing facial oil blending cold-pressed damask "
            "rose with olive-derived squalane and rosehip. Melts into skin to "
            "restore suppleness overnight, leaving a soft, dewy finish by morning."
        ),
        "ingredients": (
            "Squalane, Rosa Damascena Flower Oil, Rosa Canina Seed Oil, "
            "Jojoba Esters, Bisabolol, Tocopherol"
        ),
        "benefits": (
            "Deeply nourishes without clogging pores\n"
            "Supports the skin barrier overnight\n"
            "Softens the look of fine lines\n"
            "Calming natural rose aroma"
        ),
        "how_to_use": (
            "Warm 3–5 drops between palms and press into skin as the last step "
            "of your evening routine. Can be mixed into moisturiser for extra comfort."
        ),
        "price": "52.00",
        "compare_at_price": None,
        "rating": "4.80",
        "reviews_count": 287,
        "size": "30 ml",
        "skin_type": "dry",
        "accent_color": "#E8B4B8",
        "image_url": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": True,
        "order": 2,
    },
    # 3
    {
        "name": "Hyaluronic Acid Serum",
        "category": "Serums & Oils",
        "tagline": "Multi-weight hydration + B5",
        "description": (
            "Three molecular weights of hyaluronic acid plus panthenol hydrate "
            "at different depths for immediate plumping and lasting moisture. "
            "A must-have for tight, dehydrated or travel-stressed skin."
        ),
        "ingredients": (
            "Aqua, Sodium Hyaluronate (3 weights), Panthenol, Glycerin, "
            "Betaine, Allantoin, Sodium PCA"
        ),
        "benefits": (
            "Instantly plumps and smooths\n"
            "Up to 72 hours of continuous hydration\n"
            "Fragrance-free and suitable for reactive skin\n"
            "Layers under any moisturiser"
        ),
        "how_to_use": (
            "Apply 2–3 drops to damp skin morning and evening, then seal with "
            "moisturiser or oil."
        ),
        "price": "42.00",
        "compare_at_price": None,
        "rating": "4.90",
        "reviews_count": 356,
        "size": "30 ml",
        "skin_type": "all",
        "accent_color": "#BFD8D2",
        "image_url": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": False,
        "order": 3,
    },
    # 4
    {
        "name": "Gentle Cream Cleanser",
        "category": "Cleansers",
        "tagline": "Soap-free daily cleanser with oat & ceramides",
        "description": (
            "A creamy, low-foam cleanser that lifts makeup and impurities "
            "without stripping. Colloidal oat and ceramides leave the barrier "
            "calm, comfortable and ready for the rest of your routine."
        ),
        "ingredients": (
            "Aqua, Glycerin, Colloidal Oatmeal, Ceramide NP, Coco-Glucoside, "
            "Panthenol, Allantoin"
        ),
        "benefits": (
            "Removes makeup and SPF in one step\n"
            "pH-balanced and soap-free\n"
            "Leaves skin soft, never tight\n"
            "Suitable for rosacea-prone skin"
        ),
        "how_to_use": (
            "Massage a pump onto damp skin morning and evening, then rinse with "
            "lukewarm water and pat dry."
        ),
        "price": "32.00",
        "compare_at_price": None,
        "rating": "4.80",
        "reviews_count": 298,
        "size": "150 ml",
        "skin_type": "sensitive",
        "accent_color": "#BFD8D2",
        "image_url": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 4,
    },
    # 5
    {
        "name": "Hydra Rich Face Cream",
        "category": "Moisturisers",
        "tagline": "Ceramides, peptides & shea for 24h comfort",
        "description": (
            "A cushiony, fragrance-free cream that strengthens the moisture "
            "barrier with ceramides and peptides. Rich enough for dry skin, "
            "yet light enough to wear under makeup."
        ),
        "ingredients": (
            "Aqua, Glycerin, Shea Butter, Ceramide NP, Ceramide AP, "
            "Palmitoyl Tripeptide-1, Squalane, Niacinamide"
        ),
        "benefits": (
            "24-hour barrier-supporting hydration\n"
            "Smooths the look of fine lines\n"
            "Fragrance-free and non-comedogenic\n"
            "Works day and night"
        ),
        "how_to_use": (
            "Warm a pea-sized amount and press into face and neck morning and "
            "evening after serum."
        ),
        "price": "46.00",
        "compare_at_price": None,
        "rating": "4.90",
        "reviews_count": 241,
        "size": "50 ml",
        "skin_type": "dry",
        "accent_color": "#E8B4B8",
        "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": False,
        "order": 5,
    },
    # 6
    {
        "name": "Daily Glow Sunscreen SPF 50",
        "category": "Sun Care",
        "tagline": "Invisible, weightless, no white cast",
        "description": (
            "A weightless broad-spectrum SPF 50 that disappears into every "
            "skin tone. Niacinamide and vitamin E care for skin while you're "
            "protected — no pilling, no white cast, no greasy after-feel."
        ),
        "ingredients": (
            "Aqua, Homosalate, Octocrylene, Niacinamide, Tocopherol, "
            "Glycerin, Sodium Hyaluronate"
        ),
        "benefits": (
            "Broad-spectrum UVA / UVB protection\n"
            "Invisible on all skin tones\n"
            "Layer-friendly under makeup\n"
            "Reef-friendly filters"
        ),
        "how_to_use": (
            "Apply generously as the last step of your morning routine, 15 minutes "
            "before sun exposure. Reapply every two hours."
        ),
        "price": "38.00",
        "compare_at_price": None,
        "rating": "4.90",
        "reviews_count": 521,
        "size": "50 ml",
        "skin_type": "all",
        "accent_color": "#F7E1A0",
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": True,
        "order": 6,
    },
    # 7
    {
        "name": "Whipped Shea Body Butter",
        "category": "Body Care",
        "tagline": "48-hour body moisture with shea & cocoa",
        "description": (
            "An airy, whipped butter that melts on contact and keeps skin "
            "velvet-soft for up to 48 hours. Raw shea, cocoa butter and "
            "squalane restore elbows, knees and everywhere in between."
        ),
        "ingredients": (
            "Shea Butter, Cocoa Seed Butter, Squalane, Glycerin, "
            "Vitamin E, Vanilla Planifolia Fruit Extract"
        ),
        "benefits": (
            "48-hour body hydration\n"
            "Softens rough elbows, knees and heels\n"
            "Absorbs quickly — no greasy film\n"
            "Warm vanilla-shea scent"
        ),
        "how_to_use": (
            "Massage into clean, slightly damp skin after showering, focusing "
            "on dry areas. Use daily."
        ),
        "price": "34.00",
        "compare_at_price": None,
        "rating": "4.80",
        "reviews_count": 187,
        "size": "200 ml",
        "skin_type": "all",
        "accent_color": "#E7D3C6",
        "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 7,
    },
    # 8
    {
        "name": "Rose & Sugar Body Scrub",
        "category": "Body Care",
        "tagline": "Polishing brown sugar & rosehip",
        "description": (
            "Fine brown sugar crystals buff away dullness while rosehip and "
            "jojoba oils leave skin satin-smooth. Rinses clean without stripping."
        ),
        "ingredients": (
            "Sucrose, Jojoba Esters, Rosa Canina Seed Oil, Glycerin, "
            "Cocos Nucifera Oil, Vitamin E"
        ),
        "benefits": (
            "Smooths rough, dry body skin\n"
            "Prepares skin for self-tan and moisturiser\n"
            "Non-stripping oil-to-milk texture\n"
            "Subtle natural rose scent"
        ),
        "how_to_use": (
            "Once or twice a week, massage onto damp skin in the shower, then "
            "rinse. Follow with body butter."
        ),
        "price": "30.00",
        "compare_at_price": None,
        "rating": "4.70",
        "reviews_count": 203,
        "size": "250 g",
        "skin_type": "all",
        "accent_color": "#E7D3C6",
        "image_url": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 8,
    },
    # 9
    {
        "name": "Silk Repair Hair Serum",
        "category": "Hair Care",
        "tagline": "Argan, camellia & keratin for frizz control",
        "description": (
            "A weightless finishing serum that tames frizz, adds shine and "
            "protects against heat up to 220°C. Argan, camellia and hydrolysed "
            "keratin leave hair glassy-smooth without weighing it down."
        ),
        "ingredients": (
            "Cyclopentasiloxane, Argania Spinosa Kernel Oil, Camellia Oleifera "
            "Seed Oil, Hydrolysed Keratin, Panthenol"
        ),
        "benefits": (
            "Smooths frizz and flyaways instantly\n"
            "Heat protection up to 220°C\n"
            "Adds glass-like shine\n"
            "Safe for colour-treated hair"
        ),
        "how_to_use": (
            "Warm 1–2 pumps and smooth through damp or dry mid-lengths and ends. "
            "Style as usual."
        ),
        "price": "36.00",
        "compare_at_price": None,
        "rating": "4.80",
        "reviews_count": 164,
        "size": "50 ml",
        "skin_type": "all",
        "accent_color": "#D9C7E8",
        "image_url": "https://images.unsplash.com/photo-1522338242992-e1a54906a8da?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 9,
    },
    # 10
    {
        "name": "Rosewater Face Mist",
        "category": "Masks & Mists",
        "tagline": "Hydrating rose mist with aloe & panthenol",
        "description": (
            "A fine, refreshing mist of steam-distilled rosewater, aloe and "
            "panthenol that rehydrates on contact. Use it to set makeup, "
            "refresh midday or prep skin before serum."
        ),
        "ingredients": (
            "Rosa Damascena Flower Water, Aloe Barbadensis Leaf Juice, "
            "Panthenol, Glycerin, Allantoin"
        ),
        "benefits": (
            "Instantly hydrates and calms\n"
            "Refreshes makeup without smudging\n"
            "Preps skin for better serum absorption\n"
            "Travel-friendly fine mist"
        ),
        "how_to_use": (
            "Hold 15 cm from face and mist 2–3 times. Use morning, evening or "
            "whenever skin feels thirsty."
        ),
        "price": "26.00",
        "compare_at_price": None,
        "rating": "4.70",
        "reviews_count": 221,
        "size": "100 ml",
        "skin_type": "all",
        "accent_color": "#C9E0E8",
        "image_url": "https://images.unsplash.com/photo-1615397349754-cfa2066a298e?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 10,
    },
    # 11
    {
        "name": "Soft Blush Lip Tint",
        "category": "Makeup",
        "tagline": "Sheer buildable colour + shea butter",
        "description": (
            "A comfortable, balm-like tint that gives lips a soft, natural "
            "flush. Buildable from a whisper of colour to a full rose, with "
            "shea butter and vitamin E to keep lips soft all day."
        ),
        "ingredients": (
            "Shea Butter, Ricinus Communis Seed Oil, Candelilla Wax, "
            "Tocopherol, Mica, Titanium Dioxide"
        ),
        "benefits": (
            "Sheer, buildable natural colour\n"
            "Balm texture, no dry feel\n"
            "Softens and conditions lips\n"
            "Available in Rosewood & Nude"
        ),
        "how_to_use": "Swipe directly onto lips. Layer for a deeper flush.",
        "price": "24.00",
        "compare_at_price": None,
        "rating": "4.70",
        "reviews_count": 146,
        "size": "4 g",
        "skin_type": "all",
        "accent_color": "#F0C0C8",
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "bestseller": False,
        "order": 11,
    },
    # 12
    {
        "name": "Overnight Repair Mask",
        "category": "Masks & Mists",
        "tagline": "Peptides + ceramides sleeping treatment",
        "description": (
            "A rich overnight treatment that works while you sleep. Peptides, "
            "ceramides and bakuchiol support overnight renewal so you wake up "
            "with skin that looks rested, plump and even."
        ),
        "ingredients": (
            "Aqua, Glycerin, Ceramide NP, Palmitoyl Tripeptide-1, Bakuchiol, "
            "Squalane, Panthenol, Allantoin"
        ),
        "benefits": (
            "Wake up to plumper, more even skin\n"
            "Gentle bakuchiol — no retinol irritation\n"
            "Reinforces the barrier overnight\n"
            "Non-comedogenic and fragrance-free"
        ),
        "how_to_use": (
            "Two to three nights a week, apply a generous layer as the last step "
            "of your evening routine. Rinse in the morning."
        ),
        "price": "58.00",
        "compare_at_price": None,
        "rating": "4.90",
        "reviews_count": 198,
        "size": "50 ml",
        "skin_type": "all",
        "accent_color": "#C9E0E8",
        "image_url": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=800&q=80",
        "featured": True,
        "bestseller": True,
        "order": 12,
    },
]


class Command(BaseCommand):
    help = (
        "Seed the database with 8 categories and 12 sample Glow & Grace products."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete all existing Products and Categories before seeding.",
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing catalogue."))

        # --- Categories -------------------------------------------------
        cat_map = {}
        for entry in CATEGORIES:
            slug = slugify(entry["name"])
            category, created = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": entry["name"],
                    "icon": entry["icon"],
                    "tint": entry["tint"],
                    "description": entry.get("description", ""),
                    "order": entry["order"],
                },
            )
            cat_map[entry["name"]] = category

        self.stdout.write(
            self.style.SUCCESS(f"Categories ready: {len(cat_map)}")
        )

        # --- Products ---------------------------------------------------
        created_count = 0
        updated_count = 0

        for data in PRODUCTS:
            category = cat_map[data["category"]]
            slug = slugify(data["name"])

            defaults = {
                "name": data["name"],
                "category": category,
                "tagline": data.get("tagline", ""),
                "description": data["description"],
                "ingredients": data.get("ingredients", ""),
                "benefits": data.get("benefits", ""),
                "how_to_use": data.get("how_to_use", ""),
                "price": Decimal(data["price"]),
                "compare_at_price": (
                    Decimal(data["compare_at_price"])
                    if data.get("compare_at_price")
                    else None
                ),
                "rating": Decimal(data["rating"]),
                "reviews_count": data["reviews_count"],
                "size": data["size"],
                "skin_type": data["skin_type"],
                "accent_color": data["accent_color"],
                "image_url": data.get("image_url", ""),
                "featured": data.get("featured", False),
                "bestseller": data.get("bestseller", False),
                "is_active": True,
                "order": data.get("order", 0),
            }

            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Products ready: {created_count} created, "
                f"{updated_count} updated."
            )
        )
        self.stdout.write(
            self.style.SUCCESS("Done. Your storefront now has real data.")
        )