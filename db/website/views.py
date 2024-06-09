import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, Booking
from .forms import AddProductForm, ProductUpdateForm, CreateOrderForm, BookingForm
from django_pandas.io import read_frame
import plotly
import plotly.express as px

#Product functions
@login_required
def product_list(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "themes/product_list.html", context= context)


@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddProductForm(data=request.POST)
        if add_form.is_valid():
            new_product = add_form.save(commit=False)
            new_product.save()
            messages.success(request, 'Success.')
            return redirect("/themes/")
    else: 
        add_form = AddProductForm

    return render(request, "themes/product_add.html", {"form": add_form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect("/themes/")


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        update_form = ProductUpdateForm(data=request.POST)
        if update_form.is_valid():
            product.Name = update_form.data['Name']
            product.Category = update_form.data['Category']
            product.Quantity = update_form.data['Quantity']
            product.Price = update_form.data['Price']
            product.save()
            return redirect(f"/themes/")
    else:
        update_form = ProductUpdateForm(instance=product)
    context = {"form": update_form}
    return render(request, "themes/product_update.html", context=context)



#Order Funtions
@login_required
def order_list(request):
    orders = Order.objects.all()
    context = {
        "orders": orders
    }
    return render(request, "themes/order_list.html", context= context)


@login_required
def create_order(request):
    if request.method == "POST":
        order_form = CreateOrderForm(data=request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.total_price = order.product.Price * order.quantity
            order.save()
            messages.success(request, 'Success.')
            return redirect('/themes/order_list')  
    else:
        order_form = CreateOrderForm()

    return render(request, "themes/create_order.html", {"form": order_form})


@login_required
def delete_order(request,pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, 'Success.')
    return redirect("/themes/order_list")


# Booking functions
@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings
    }
    return render(request, "themes/booking_list.html", context= context)


@login_required
def create_booking(request):
    if request.method == 'POST':
        booking_form = BookingForm(data=request.POST)
        if booking_form.is_valid():
            booking_form.save()
            messages.success(request, 'Đặt lịch thành công.')
            return redirect('/themes/booking_list')
        else:
            messages.error(request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.')
    else:
        booking_form = BookingForm()

    return render(request, 'themes/create_booking.html', {'form': booking_form})


@login_required
def dashboard(request):
    products = Product.objects.all()
    dp = read_frame(products)

    orders = Order.objects.all()
    df = read_frame(orders)
    

    #sale graph
    sale_graph = df.groupby(by="date", as_index=False, sort=False)['quantity'].sum()
    sale_graph = px.line(sale_graph, x = sale_graph.date, y = sale_graph.quantity, title="Sales Trend")
    sale_graph = json.dumps(sale_graph, cls=plotly.utils.PlotlyJSONEncoder)

    #best performing product
    best_performing_product_dp = dp.groupby(by="Name").sum().sort_values(by="Sold")
    best_performing_product = px.bar(best_performing_product_dp, 
                                    x = best_performing_product_dp.index, 
                                    y = best_performing_product_dp.Sold, 
                                    title="Best Performing Product"
                                )
    best_performing_product = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)


    context = {
            "sale_graph": sale_graph,
            "best_performing_product": best_performing_product
        }
    return render(request, 'themes/dashboard.html', context=context)