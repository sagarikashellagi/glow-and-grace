"""
Admin configuration for Glow & Grace.
Includes custom bulk actions for editing multiple products / categories.
"""
from decimal import Decimal
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Category, Product, ContactMessage, NewsletterSubscriber


# ---------------------------------------------------------------------------
# Category admin
# ---------------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count", "tint_swatch", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    ordering = ("order", "name")
    actions = ["increase_order", "decrease_order"]

    fieldsets = (
        ("Identity", {
            "fields": ("name", "slug", "description"),
        }),
        ("Appearance", {
            "fields": ("icon", "tint", "order"),
            "description": (
                "Icon uses Bootstrap Icons class names. "
                "Tint is a hex color for the tile gradient."
            ),
        }),
    )

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()

    @admin.display(description="Tint")
    def tint_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block;width:22px;height:22px;'
            'border-radius:6px;border:1px solid #ddd;background:{}"></span>',
            obj.tint,
        )

    @admin.action(description="Increase order of selected by 1")
    def increase_order(self, request, queryset):
        updated = 0
        for cat in queryset:
            cat.order = cat.order + 1
            cat.save()
            updated += 1
        self.message_user(
            request,
            f"Pushed {updated} categories down (order +1).",
            messages.SUCCESS,
        )

    @admin.action(description="Decrease order of selected by 1")
    def decrease_order(self, request, queryset):
        updated = 0
        for cat in queryset:
            cat.order = max(0, cat.order - 1)
            cat.save()
            updated += 1
        self.message_user(
            request,
            f"Pulled {updated} categories up (order -1).",
            messages.SUCCESS,
        )


# ---------------------------------------------------------------------------
# Product admin
# ---------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail", "name", "category", "price_display", "rating",
        "featured", "bestseller", "is_active", "order",
    )
    list_display_links = ("thumbnail", "name")
    list_editable = ("featured", "bestseller", "is_active", "order")
    list_filter = ("category", "featured", "bestseller", "is_active", "skin_type")
    search_fields = ("name", "tagline", "description", "ingredients")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")
    save_on_top = True
    list_per_page = 25
    ordering = ("order", "name")

    fieldsets = (
        ("Identity", {
            "fields": ("name", "slug", "category", "tagline"),
        }),
        ("Copy", {
            "fields": ("description", "benefits", "ingredients", "how_to_use"),
            "description": (
                "Benefits: one per line. "
                "Ingredients: comma-separated INCI list."
            ),
        }),
        ("Commerce", {
            "fields": (
                "price", "compare_at_price", "rating", "reviews_count",
            ),
        }),
        ("Attributes", {
            "fields": ("size", "skin_type"),
        }),
        ("Imagery", {
            "fields": ("image", "image_url", "image_preview", "accent_color"),
            "description": (
                "Upload a real photo, or paste an external image URL, "
                "or leave both blank to use the generated SVG placeholder."
            ),
        }),
        ("Merchandising", {
            "fields": ("featured", "bestseller", "is_active", "order"),
        }),
        ("Meta", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = [
        "mark_featured",
        "unmark_featured",
        "mark_bestseller",
        "unmark_bestseller",
        "activate_products",
        "deactivate_products",
        "increase_price_10",
        "decrease_price_10",
    ]

    @admin.action(description="Mark selected as featured")
    def mark_featured(self, request, queryset):
        n = queryset.update(featured=True)
        self.message_user(request, f"{n} products marked featured.", messages.SUCCESS)

    @admin.action(description="Unmark selected as featured")
    def unmark_featured(self, request, queryset):
        n = queryset.update(featured=False)
        self.message_user(request, f"{n} products unmarked as featured.", messages.SUCCESS)

    @admin.action(description="Mark selected as bestseller")
    def mark_bestseller(self, request, queryset):
        n = queryset.update(bestseller=True)
        self.message_user(request, f"{n} products marked bestseller.", messages.SUCCESS)

    @admin.action(description="Unmark selected as bestseller")
    def unmark_bestseller(self, request, queryset):
        n = queryset.update(bestseller=False)
        self.message_user(request, f"{n} products unmarked as bestseller.", messages.SUCCESS)

    @admin.action(description="Activate selected products")
    def activate_products(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} products activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected products")
    def deactivate_products(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} products deactivated.", messages.SUCCESS)

    @admin.action(description="Increase price of selected by 10 percent")
    def increase_price_10(self, request, queryset):
        count = 0
        for p in queryset:
            p.price = (p.price * Decimal("1.10")).quantize(Decimal("0.01"))
            p.save()
            count += 1
        self.message_user(
            request,
            f"{count} products price increased by 10%.",
            messages.SUCCESS,
        )

    @admin.action(description="Decrease price of selected by 10 percent")
    def decrease_price_10(self, request, queryset):
        count = 0
        for p in queryset:
            p.price = (p.price * Decimal("0.90")).quantize(Decimal("0.01"))
            p.save()
            count += 1
        self.message_user(
            request,
            f"{count} products price decreased by 10%.",
            messages.SUCCESS,
        )

    @admin.display(description="")
    def thumbnail(self, obj):
        src = obj.display_image
        if not src:
            return format_html(
                '<span style="display:inline-block;width:46px;height:46px;'
                'border-radius:8px;background:{}"></span>',
                obj.accent_color,
            )
        return format_html(
            '<img src="{}" alt="" style="width:46px;height:46px;'
            'object-fit:cover;border-radius:8px;border:1px solid #eee">',
            src,
        )

    @admin.display(description="Price")
    def price_display(self, obj):
        if obj.compare_at_price and obj.compare_at_price > obj.price:
            return format_html(
                '<strong>${}</strong> <s style="color:#999">${}</s>',
                obj.price, obj.compare_at_price,
            )
        return f"${obj.price}"

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if not obj or not obj.pk:
            return "Save the product first to see a preview."
        src = obj.display_image
        if not src:
            return "No image — SVG placeholder will be used."
        return format_html(
            '<img src="{}" alt="" style="max-width:260px;max-height:260px;'
            'border-radius:12px;border:1px solid #eee">',
            src,
        )


# ---------------------------------------------------------------------------
# Contact messages
# ---------------------------------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False


# ---------------------------------------------------------------------------
# Newsletter subscribers
# ---------------------------------------------------------------------------
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("email",)
    list_editable = ("is_active",)
    readonly_fields = ("email", "created_at")
    date_hierarchy = "created_at"


# ---------------------------------------------------------------------------
# Global admin branding
# ---------------------------------------------------------------------------
admin.site.site_header = "Glow & Grace Administration"
admin.site.site_title = "Glow & Grace Admin"
admin.site.index_title = "Manage your store"