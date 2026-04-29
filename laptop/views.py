from django.shortcuts import render, redirect
from .form import InventoryForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, F
from datetime import date
import calendar

from .models import Inventories
from .form import InventoryForm


def inventory_view(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    selected_date = request.GET.get("date")

    # ---------- SAVE FORM ----------
    form = InventoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory added successfully")
            return redirect("inventory")

    # ---------- CALENDAR DATA ----------
    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    qs = (
        Inventories.objects
        .filter(created_at__year=year, created_at__month=month)
        .values("created_at__date", "category")
        .annotate(
            qty=Sum("quantity"),
            value=Sum(F("quantity") * F("price"))
        )
    )

    inventory_map = {}
    for r in qs:
        d = r["created_at__date"]
        if d not in inventory_map:
            inventory_map[d] = {"categories": {}, "value": 0}

        inventory_map[d]["categories"][r["category"]] = r["qty"]
        inventory_map[d]["value"] += float(r["value"] or 0)

    calendar_data = []
    for week in month_days:
        week_days = []
        for d in week:
            if d.month == month:
                data = inventory_map.get(d)
                week_days.append({
                    "date": d,
                    "day": d.day,
                    "categories": data["categories"] if data else {},
                    "value": round(data["value"], 2) if data else 0
                })
            else:
                week_days.append(None)
        calendar_data.append(week_days)

    # ---------- TABLE DATA (ON DATE CLICK) ----------
    day_entries = None
    if selected_date:
        day_entries = Inventories.objects.filter(
            created_at__date=selected_date
        )

    return render(request, "inventories/inventory_form.html", {
        "calendar": calendar_data,
        "form": form,
        "day_entries": day_entries,
        "selected_date": selected_date,
        "month": month,
        "year": year
    })

def home(request):
    return render(request,"home.html")

def service(request):
    return render(request,"service.html")
def about(request):
    return render(request,"about.html")

from .form import InventoryForm
from django.contrib import messages
from django.db.models import Sum, F
from datetime import date
import calendar
from .models import Inventories
from .form import InventoryForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def inventory_view(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    selected_date = request.GET.get("date")

    # ---------- SAVE FORM ----------
    form = InventoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory added successfully")
            return redirect("inventory")

    # ---------- CALENDAR DATA ----------
    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    qs = (
        Inventories.objects
        .filter(created_at__year=year, created_at__month=month)
        .values("created_at__date", "category")
        .annotate(
            qty=Sum("quantity"),
            value=Sum(F("quantity") * F("price"))
        )
    )

    inventory_map = {}
    for r in qs:
        d = r["created_at__date"]
        if d not in inventory_map:
            inventory_map[d] = {"categories": {}, "value": 0}

        inventory_map[d]["categories"][r["category"]] = r["qty"]
        inventory_map[d]["value"] += float(r["value"] or 0)

    calendar_data = []
    for week in month_days:
        week_days = []
        for d in week:
            if d.month == month:
                data = inventory_map.get(d)
                week_days.append({
                    "date": d,
                    "day": d.day,
                    "categories": data["categories"] if data else {},
                    "value": round(data["value"], 2) if data else 0
                })
            else:
                week_days.append(None)
        calendar_data.append(week_days)

    # ---------- TABLE DATA (ON DATE CLICK) ----------
    day_entries = None
    if selected_date:
        day_entries = Inventories.objects.filter(
            created_at__date=selected_date
        )

    return render(request, "inventories/inventory_form.html", {
        "calendar": calendar_data,
        "form": form,
        "day_entries": day_entries,
        "selected_date": selected_date,
        "month": month,
        "year": year
    })


def home(request):
    return render(request, "home.html")


def service(request):
    return render(request, "service.html")


def about(request):
    return render(request, "about.html")


def sales(request):
    return render(request, "sales.html")


from django.shortcuts import render, redirect
from .form import InventoryForm
from django.contrib import messages
from django.db.models import Sum, F
from datetime import date
import calendar
from .models import Inventories
from .form import InventoryForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def inventory_view(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    selected_date = request.GET.get("date")

    form = InventoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory added successfully")
            return redirect("inventory")

    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    qs = (
        Inventories.objects
        .filter(created_at__year=year, created_at__month=month)
        .values("created_at__date", "category")
        .annotate(
            qty=Sum("quantity"),
            value=Sum(F("quantity") * F("price"))
        )
    )

    inventory_map = {}
    for r in qs:
        d = r["created_at__date"]
        if d not in inventory_map:
            inventory_map[d] = {"categories": {}, "value": 0}

        inventory_map[d]["categories"][r["category"]] = r["qty"]
        inventory_map[d]["value"] += float(r["value"] or 0)

    calendar_data = []
    for week in month_days:
        week_days = []
        for d in week:
            if d.month == month:
                data = inventory_map.get(d)
                week_days.append({
                    "date": d,
                    "day": d.day,
                    "categories": data["categories"] if data else {},
                    "value": round(data["value"], 2) if data else 0
                })
            else:
                week_days.append(None)
        calendar_data.append(week_days)

    day_entries = None
    if selected_date:
        day_entries = Inventories.objects.filter(
            created_at__date=selected_date
        )

    return render(request, "inventories/inventory_form.html", {
        "calendar": calendar_data,
        "form": form,
        "day_entries": day_entries,
        "selected_date": selected_date,
        "month": month,
        "year": year
    })


def home(request):
    return render(request, "home.html")


def service(request):
    return render(request, "service.html")


def about(request):
    return render(request, "about.html")


def sales(request):
    return render(request, "sales.html")


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        # Store all data first (even if email fails)
        response_data = {'success': False}
        
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            device = request.POST.get('device', '').strip()
            service = request.POST.get('service', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Validate required fields
            if not name or not email:
                return JsonResponse({'success': False, 'error': 'Name and Email are required'}, status=400)
            
            current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")
            
            # Get logo URL
            try:
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http'
                domain = current_site.domain
                logo_url = f"{protocol}://{domain}/static/images/logo1.png"
            except:
                logo_url = "http://127.0.0.1:8000/static/images/logo1.png"
            
            # ============================================================
            # FIRST SEND EMAIL TO ADMIN (ALWAYS TRY THIS FIRST)
            # ============================================================
            admin_html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>New Contact Request - SBM</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f5f0e8;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: #ffffff;
                        border-radius: 20px;
                        overflow: hidden;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    }}
                    .email-header {{
                        background: linear-gradient(135deg, #0e1117, #151b25);
                        padding: 30px 20px;
                        text-align: center;
                        border-bottom: 3px solid #c9a227;
                    }}
                    .logo-img-header {{
                        width: 70px;
                        height: 70px;
                        object-fit: contain;
                        margin-bottom: 10px;
                        border-radius: 12px;
                    }}
                    .email-header h1 {{
                        color: #c9a227;
                        font-size: 24px;
                        margin: 10px 0 0;
                    }}
                    .email-header p {{
                        color: rgba(245,240,232,0.7);
                        font-size: 12px;
                        margin: 5px 0 0;
                    }}
                    .email-body {{
                        padding: 30px;
                    }}
                    .alert-badge {{
                        background: #dc3545;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 30px;
                        font-size: 12px;
                        font-weight: bold;
                        display: inline-block;
                        margin-bottom: 20px;
                    }}
                    .greeting {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #1e1a14;
                        margin-bottom: 20px;
                        border-left: 4px solid #c9a227;
                        padding-left: 15px;
                    }}
                    .info-card {{
                        background: #f8f6f2;
                        border-radius: 12px;
                        padding: 15px;
                        margin-bottom: 20px;
                        border: 1px solid #e0d6c2;
                    }}
                    .info-row {{
                        display: flex;
                        margin-bottom: 12px;
                        padding-bottom: 12px;
                        border-bottom: 1px solid #e0d6c2;
                    }}
                    .info-row:last-child {{
                        border-bottom: none;
                    }}
                    .info-label {{
                        width: 120px;
                        font-weight: 700;
                        color: #c9a227;
                        font-size: 13px;
                        text-transform: uppercase;
                    }}
                    .info-value {{
                        flex: 1;
                        color: #1e1a14;
                        font-size: 14px;
                    }}
                    .message-box {{
                        background: #fffcf5;
                        border: 1px solid #c9a227;
                        border-radius: 12px;
                        padding: 15px;
                        margin-top: 10px;
                    }}
                    .message-text {{
                        color: #555;
                        line-height: 1.6;
                        margin: 10px 0 0 0;
                    }}
                    .timestamp {{
                        font-size: 11px;
                        color: #999;
                        text-align: right;
                        margin-top: 15px;
                        padding-top: 10px;
                        border-top: 1px solid #e0d6c2;
                    }}
                    .cta-buttons {{
                        display: flex;
                        gap: 15px;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 10px 20px;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 13px;
                        font-weight: bold;
                    }}
                    .btn-gold {{
                        background: linear-gradient(135deg, #c9a227, #8a6e0f);
                        color: #1a1a1a;
                    }}
                    .btn-outline {{
                        border: 1px solid #c9a227;
                        color: #c9a227;
                        background: transparent;
                    }}
                    .email-footer {{
                        background: #0e1117;
                        padding: 20px;
                        text-align: center;
                        border-top: 1px solid rgba(201,162,39,0.2);
                    }}
                    .email-footer p {{
                        color: rgba(245,240,232,0.6);
                        font-size: 11px;
                        margin: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <img src="{logo_url}" alt="SBM Logo" class="logo-img-header">
                        <h1>SBM Sales & Services</h1>
                        <p>Solapur's Most Trusted Repair Specialists</p>
                    </div>
                    <div class="email-body">
                        <div class="alert-badge">🔔 NEW LEAD RECEIVED</div>
                        <div class="greeting">New contact form submission from {name}!</div>
                        <div class="info-card">
                            <div class="info-row"><div class="info-label">📛 Name:</div><div class="info-value"><strong>{name}</strong></div></div>
                            <div class="info-row"><div class="info-label">📧 Email:</div><div class="info-value">{email}</div></div>
                            <div class="info-row"><div class="info-label">📱 Phone:</div><div class="info-value">{phone if phone else 'Not provided'}</div></div>
                            <div class="info-row"><div class="info-label">💻 Device:</div><div class="info-value">{device if device else 'Not specified'}</div></div>
                            <div class="info-row"><div class="info-label">🔧 Service:</div><div class="info-value">{service if service else 'Not specified'}</div></div>
                        </div>
                        <div class="message-box"><strong>📝 Message:</strong><p class="message-text">{message if message else 'No message provided'}</p></div>
                        <div class="cta-buttons">
                            <a href="mailto:{email}" class="btn btn-gold">📧 Reply to Client</a>
                            <a href="tel:{phone if phone else '8087594890'}" class="btn btn-outline">📞 Call Client</a>
                        </div>
                        <div class="timestamp">Submitted on: {current_time}</div>
                    </div>
                    <div class="email-footer">
                        <p>© 2026 SBM Sales & Services | 📞 8087594890 | 📧 sbmsolutions@gmail.com</p>
                    </div>
                </div>
            </body>
            </html>
            '''
            
            admin_text_content = f"""
            NEW LEAD: {name}
            Name: {name}
            Email: {email}
            Phone: {phone}
            Device: {device}
            Service: {service}
            Message: {message}
            Time: {current_time}
            """
            
            # SEND TO ADMIN - THIS MUST WORK
            admin_email = EmailMultiAlternatives(
                subject=f'🔔 NEW LEAD: {name} - SBM Services',
                body=admin_text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['sbmsolutions@gmail.com', 'lavanyan1222@gmail.com'],
                reply_to=[email],
            )
            admin_email.attach_alternative(admin_html_content, "text/html")
            admin_email.send(fail_silently=False)
            
            # ============================================================
            # THEN TRY TO SEND AUTO-REPLY TO CUSTOMER (DON'T FAIL IF WRONG EMAIL)
            # ============================================================
            customer_email_sent = False
            try:
                customer_html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Thank You - SBM</title>
                    <style>
                        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f0e8; }}
                        .email-container {{ max-width: 550px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                        .email-header {{ background: linear-gradient(135deg, #0e1117, #151b25); padding: 30px 20px; text-align: center; border-bottom: 3px solid #c9a227; }}
                        .logo-img-header {{ width: 70px; height: 70px; object-fit: contain; margin-bottom: 10px; border-radius: 12px; }}
                        .email-header h1 {{ color: #c9a227; font-size: 22px; margin: 10px 0 0; }}
                        .email-body {{ padding: 30px; }}
                        .thankyou {{ font-size: 24px; font-weight: bold; color: #1e1a14; text-align: center; margin-bottom: 20px; }}
                        .info-summary {{ background: #fffcf5; border: 1px solid #e0d6c2; border-radius: 12px; padding: 15px; margin: 15px 0; }}
                        .contact-details {{ background: linear-gradient(135deg, #faf1df, #fff3e0); border-radius: 12px; padding: 15px; text-align: center; margin: 20px 0; }}
                        .phone-number {{ font-size: 20px; font-weight: bold; color: #c9a227; text-decoration: none; }}
                        .email-footer {{ background: #0e1117; padding: 20px; text-align: center; }}
                        .email-footer p {{ color: rgba(245,240,232,0.6); font-size: 11px; }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="email-header">
                            <img src="{logo_url}" alt="SBM Logo" class="logo-img-header">
                            <h1>SBM Sales & Services</h1>
                        </div>
                        <div class="email-body">
                            <div class="thankyou">Thank You, {name}! 🙏</div>
                            <p>We have received your inquiry and will get back to you within 30 minutes (11 AM - 10 PM).</p>
                            <div class="info-summary">
                                <strong>📋 Your Request:</strong><br>
                                • Device: {device if device else 'Not specified'}<br>
                                • Service: {service if service else 'Not specified'}
                            </div>
                            <div class="contact-details">
                                <strong>📞 Need Immediate Assistance?</strong><br>
                                <a href="tel:+918087594890" class="phone-number">+91 80875 94890</a>
                            </div>
                            <p style="color:#888;font-size:12px;text-align:center;">Visit: Ashok Chowk, Shop No.- 8, Ghanate Complex, Solapur</p>
                        </div>
                        <div class="email-footer">
                            <p>© 2026 SBM Sales & Services — Solapur's Most Trusted Repair Specialists</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
                
                customer_email = EmailMultiAlternatives(
                    subject=f'Thank you for contacting SBM - {name}',
                    body=f"Thank you {name}! We'll contact you soon.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                customer_email.attach_alternative(customer_html_content, "text/html")
                customer_email.send(fail_silently=True)
                customer_email_sent = True
                
            except Exception as e:
                # Customer email failed (wrong email address) - BUT YOU STILL HAVE THE LEAD!
                print(f"Customer email failed (wrong email?): {e}")
            
            # ============================================================
            # RETURN SUCCESS ALWAYS - BECAUSE YOU GOT THE LEAD
            # ============================================================
            return JsonResponse({
                'success': True,
                'customer_email_sent': customer_email_sent,
                'message': 'Your request has been submitted. We will contact you soon!'
            })
            
        except Exception as e:
            print(f"Critical Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False, 
                'error': 'Failed to send message. Please call us directly at +91 80875 94890'
            }, status=500)
    
    return render(request, "contact.html")

def sales(request):
    return render(request,"sales.html")