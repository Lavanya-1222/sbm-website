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
    
def contact(request):
    return render(request,"contact.html")