from django import forms
from django.forms import ModelForm
from .models import Product, Order, Booking

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['Name', 'Category', 'Quantity', 'Price' ]


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['Name', 'Category', 'Quantity', 'Price' ]


class CreateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity']
        

class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'staff', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        staff = cleaned_data.get('staff')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError('Thời gian bắt đầu phải trước thời gian kết thúc.')

            overlapping_bookings = Booking.objects.filter(
                staff=staff,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if self.instance.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

            if overlapping_bookings.exists():
                raise forms.ValidationError('Nhân viên này đã có lịch trong khoảng thời gian này.')

        return cleaned_data

