from django.db import models

# Create your models here.
from django.db import models

class Inventories(models.Model):

    CATEGORY_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Keyboard Mouse', 'Keyboard & Mouse'),
        ('Accessory', 'Accessory'),
        ('Software', 'Software'),
    ]

    SOFTWARE_CHOICES = [
        ('NPAV', 'NPAV'),
        ('QuickHeal', 'Quick Heal'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    item_name = models.CharField(
        max_length=100,
        help_text="Laptop brand or accessory name"
    )

    quantity = models.PositiveIntegerField(default=0)

    software_type = models.CharField(
        max_length=20,
        choices=SOFTWARE_CHOICES,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price per item"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at_date()} - {self.category} - {self.item_name} ({self.quantity})"
