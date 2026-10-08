"""
Database models for Glow & Grace.

Four models:

  Category              – product groupings (Serums & Oils, Cleansers, …)
  Product               – the products themselves, with images and copy
  ContactMessage        – submissions from the Contact page
  NewsletterSubscriber  – emails from the newsletter form

Field naming is deliberately chosen so templates render the same
`{{ product.name }}` / `{{ product.price }}` they did in the static
prototype — swapping the data source from Python lists to database
rows is invisible to the HTML.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=40,
        default="bi-droplet",
        help_text="Bootstrap Icons class, e.g. bi-droplet, bi-sun",
    )
    tint = models.CharField(
        max_length=9,
        default="#F3C9A8",
        help_text="Hex color used for tile gradients, e.g. #F3C9A8",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('products:list')}?category={self.slug}"


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------
class Product(models.Model):
    SKIN_TYPE_CHOICES = [
        ("all", "All skin types"),
        ("dry", "Dry"),
        ("oily", "Oily"),
        ("combination", "Combination"),
        ("sensitive", "Sensitive"),
        ("normal", "Normal"),
        ("mature", "Mature"),
    ]

    # Identity
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    tagline = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short one-liner shown on product cards.",
    )

    # Copy
    description = models.TextField()
    ingredients = models.TextField(
        blank=True,
        help_text="Comma-separated INCI list.",
    )
    benefits = models.TextField(
        blank=True,
        help_text="One benefit per line. Rendered as a bullet list.",
    )
    how_to_use = models.TextField(blank=True)

    # Commerce
    price = models.DecimalField(max_digits=8, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional 'was' price to show a discount.",
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.8)
    reviews_count = models.PositiveIntegerField(default=0)

    # Attributes
    size = models.CharField(max_length=60, default="30 ml")
    skin_type = models.CharField(
        max_length=20,
        choices=SKIN_TYPE_CHOICES,
        default="all",
    )

    # Imagery
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Upload a product photo. If blank, image_url is used.",
    )
    image_url = models.URLField(
        blank=True,
        help_text="Optional external image URL (used as a fallback).",
    )
    accent_color = models.CharField(
        max_length=9,
        default="#F3C9A8",
        help_text="Hex color for generated SVG placeholders.",
    )

    # Merchandising
    featured = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from the storefront.",
    )
    order = models.PositiveIntegerField(default=0)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["is_active", "order"]),
            models.Index(fields=["category", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    # -- Template helpers -------------------------------------------------
    @property
    def benefit_list(self):
        return [b.strip() for b in self.benefits.splitlines() if b.strip()]

    @property
    def ingredient_list(self):
        return [i.strip() for i in self.ingredients.split(",") if i.strip()]

    @property
    def discount_percent(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            pct = (self.compare_at_price - self.price) / self.compare_at_price * 100
            return int(round(pct))
        return 0

    @property
    def star_fill_width(self):
        try:
            return float(self.rating) / 5 * 100
        except (TypeError, ValueError):
            return 96.0

    @property
    def display_image(self):
        """Return the best available image URL for templates."""
        if self.image:
            return self.image.url
        return self.image_url or ""

    def related_products(self, limit=4):
        """Products in the same category, filling in from other categories if needed."""
        same = list(
            Product.objects.filter(
                category=self.category, is_active=True
            ).exclude(pk=self.pk)[:limit]
        )
        if len(same) < limit:
            extra = Product.objects.filter(is_active=True).exclude(
                pk=self.pk
            ).exclude(category=self.category)[: limit - len(same)]
            same.extend(extra)
        return same


# ---------------------------------------------------------------------------
# ContactMessage
# ---------------------------------------------------------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        return f"{self.name} — {self.subject}"


# ---------------------------------------------------------------------------
# NewsletterSubscriber
# ---------------------------------------------------------------------------
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter subscriber"
        verbose_name_plural = "Newsletter subscribers"

    def __str__(self):
        return self.email