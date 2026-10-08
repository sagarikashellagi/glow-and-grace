"""
Views for Glow & Grace.

Each function handles one URL and returns one rendered template.
Data now comes from the database (Product, Category, etc.) instead of
hardcoded Python lists — the templates don't change.
"""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactForm, NewsletterForm
from .models import Category, Product


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def home(request):
    """
    Landing page: hero, categories, bestsellers, testimonials, newsletter.
    """
    categories = Category.objects.all()
    bestsellers = list(
        Product.objects.filter(is_active=True, bestseller=True)[:8]
    )
    # Fallback: if no bestsellers flagged yet, show newest products
    if not bestsellers:
        bestsellers = list(Product.objects.filter(is_active=True)[:8])

    new_in = list(
        Product.objects.filter(is_active=True).order_by("-created_at")[:3]
    )

    return render(request, "home.html", {
        "categories": categories,
        "bestsellers": bestsellers,
        "new_in": new_in,
        "meta_title": "Glow & Grace — Clean, Conscious Skincare",
        "meta_description": (
            "Clean, conscious skincare for everyday radiance. "
            "Vitamin C serums, rose face oil, hyaluronic acid and more. "
            "Cruelty-free, dermatologist tested."
        ),
    })


# ---------------------------------------------------------------------------
# Products list (with search + category filter + sort)
# ---------------------------------------------------------------------------
def products_list(request):
    """
    Product catalogue with optional search query, category filter, and sort.

    Query params:
      ?q=serum             → full-text search across name/tagline/description/ingredients
      ?category=serums     → filter to a single category slug
      ?sort=price-asc      → price-asc | price-desc | rating | newest
    """
    qs = Product.objects.filter(is_active=True).select_related("category")

    query = (request.GET.get("q") or "").strip()
    category_slug = (request.GET.get("category") or "").strip()
    sort = (request.GET.get("sort") or "").strip()

    if query:
        qs = qs.filter(
            Q(name__icontains=query)
            | Q(tagline__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
        )

    current_category = None
    if category_slug:
        current_category = Category.objects.filter(slug=category_slug).first()
        if current_category:
            qs = qs.filter(category=current_category)
        else:
            # Unknown category slug → return empty results
            qs = qs.none()

    if sort == "price-asc":
        qs = qs.order_by("price")
    elif sort == "price-desc":
        qs = qs.order_by("-price")
    elif sort == "rating":
        qs = qs.order_by("-rating")
    elif sort == "newest":
        qs = qs.order_by("-created_at")
    # else: leave the model's default ordering (order, -created_at)

    return render(request, "products.html", {
        "products": qs,
        "categories": Category.objects.all(),
        "current_category": current_category,
        "query": query,
        "sort": sort,
        "meta_title": (
            f"{current_category.name} — Glow & Grace"
            if current_category
            else "Shop All Products — Glow & Grace"
        ),
        "meta_description": (
            current_category.description
            if current_category and current_category.description
            else "Browse the full Glow & Grace skincare collection."
        ),
    })


# ---------------------------------------------------------------------------
# Product detail
# ---------------------------------------------------------------------------
def product_detail(request, slug):
    """
    Single product page: full copy, ingredients, how-to-use, related products.
    """
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
    )
    related = product.related_products(limit=4)

    return render(request, "product_detail.html", {
        "product": product,
        "related": related,
        "meta_title": f"{product.name} — Glow & Grace",
        "meta_description": (
            product.tagline or product.description[:150]
        ),
    })


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
def about(request):
    """
    Brand story, standards, team. Content is static for now —
    swap to a Page model later if you want it editable.
    """
    return render(request, "about.html", {
        "meta_title": "About — Glow & Grace",
        "meta_description": (
            "Our story, our standards and the science behind Glow & Grace skincare."
        ),
    })


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
def faq(request):
    """
    Static FAQ page with accordion. Content is hand-authored in the template.
    """
    return render(request, "faq.html", {
        "meta_title": "FAQ — Glow & Grace",
        "meta_description": (
            "Answers about ingredients, shipping, returns and routines."
        ),
    })


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def contact(request):
    """
    Contact form. On valid POST:
      • Saves a ContactMessage row
      • Emails the team (console in dev, SMTP in prod)
      • Shows a success flash message
    """
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        obj = form.save()

        # Best-effort email — we don't fail the request if mail errors
        try:
            send_mail(
                subject=f"[Glow & Grace] {obj.subject}",
                message=(
                    f"From: {obj.name} <{obj.email}>\n\n"
                    f"{obj.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(
            request,
            "Thank you — your message is on its way. "
            "We reply within one business day.",
        )
        return redirect(reverse("products:contact") + "#contact-form")

    return render(request, "contact.html", {
        "form": form,
        "meta_title": "Contact — Glow & Grace",
        "meta_description": "Get in touch with the Glow & Grace team.",
    })


# ---------------------------------------------------------------------------
# Newsletter subscribe
# ---------------------------------------------------------------------------
def newsletter_subscribe(request):
    """
    Handles the inline newsletter forms. Accepts POST only; returns
    the user to wherever they came from with a flash message.
    """
    if request.method != "POST":
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Welcome to the list — check your inbox for 10% off.",
        )
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                messages.error(request, err)

    return HttpResponseRedirect(
        request.POST.get("next")
        or request.META.get("HTTP_REFERER")
        or "/"
    )


# ---------------------------------------------------------------------------
# Privacy
# ---------------------------------------------------------------------------
def privacy(request):
    return render(request, "privacy.html", {
        "meta_title": "Privacy Policy — Glow & Grace",
        "meta_description": "How we collect, use and protect your personal data.",
    })


# ---------------------------------------------------------------------------
# Terms
# ---------------------------------------------------------------------------
def terms(request):
    return render(request, "terms.html", {
        "meta_title": "Terms & Conditions — Glow & Grace",
        "meta_description": "The terms that govern your use of glowandgrace.com.",
    })