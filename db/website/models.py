from django.db import models
from django.forms import ValidationError


class Product(models.Model):
    Name = models.CharField(max_length=255, null=False, blank=False)
    Category = models.CharField(max_length=100, null=False, blank=False)
    Quantity = models.IntegerField(null=False, blank=False)
    Price = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    Sold = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self) -> str:
        return self.Name
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=False, blank=False)


    def save(self, *args, **kwargs):
        self.total_price = self.product.Price * self.quantity
        if self.pk is None:
            # Order is being created for the first time
            product = self.product
            if product.Quantity >= self.quantity:
                product.Quantity -= self.quantity
                product.Sold += self.quantity
                product.save()
            else:
                raise ValueError('Not enough quantity available in stock')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        product = self.product
        product.Quantity += self.quantity
        product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Order - {str(self.id)}'
    

class Staff(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name



class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Booking(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Check before save
        if self.start_time >= self.end_time:
            raise ValidationError('Thời gian bắt đầu phải trước thời gian kết thúc.')

        overlapping_bookings = Booking.objects.filter(
            staff=self.staff,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id) # Exclude current booking if updating

        if overlapping_bookings.exists():
            raise ValidationError('Nhân viên này đã có lịch trong khoảng thời gian này.')

        super().save(*args, **kwargs)