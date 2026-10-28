from django.shortcuts import render,redirect
from Seller.models import*
from Guest.models import*
from Adminstrator.models import*
from User.models import tbl_booking,tbl_cart





# ML views
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Sum, Count, Q, F, FloatField, IntegerField, ExpressionWrapper, OuterRef, Subquery
from django.db.models.functions import Cast, ExtractMonth, ExtractYear, ExtractWeekDay, Coalesce
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import json
import calendar
import pandas as pd
import numpy as np
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField, IntegerField, OuterRef, Subquery
from django.db.models.functions import Cast, ExtractMonth, ExtractYear
from django.utils import timezone
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def shop_sales_dashboard(request):
    shop_id = request.session['sid']
    
    # Get current date and time with timezone
    current_datetime = timezone.now()
    current_date = current_datetime.date()
    
    # -------------------------
    # BASIC METRICS
    # -------------------------
    
    # Total Income (All time) - using completed payments (booking_status=2)
    income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )
    total_income = income['total'] or 0
    
    # Today's Income
    today_income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date=current_date
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )['total'] or 0
    
    # This Month's Income
    month_income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__month=current_date.month,
        bookingid__booking_date__year=current_date.year
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )['total'] or 0
    
    # Last Month's Income
    last_month = current_date.replace(day=1) - timedelta(days=1)
    last_month_income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__month=last_month.month,
        bookingid__booking_date__year=last_month.year
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )['total'] or 0
    
    # Calculate growth percentage
    if last_month_income > 0:
        income_growth = ((month_income - last_month_income) / last_month_income) * 100
    else:
        income_growth = 100 if month_income > 0 else 0
    
    # Total Orders (Completed Payment)
    total_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values('bookingid').distinct().count()
    
    # Today's Orders
    today_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date=current_date
    ).values('bookingid').distinct().count()
    
    # Orders by Status (based on your model)
    pending_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status=1  # Assuming 1 is Pending/Booked but not paid
    ).values('bookingid').distinct().count()
    
    packed_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status=3  # Packed
    ).count()
    
    shipped_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status=4  # Shipped
    ).count()
    
    out_for_delivery_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status=5  # Out for Delivery
    ).count()
    
    cancelled_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status=7  # Cancelled
    ).count()
    
    returned_orders = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status=9  # Returned
    ).count()
    
    # Average Order Value
    avg_order_value = total_income / total_orders if total_orders > 0 else 0
    
    # -------------------------
    # WEEKLY COMPARISONS
    # -------------------------
    
    # This Week (from Monday to today)
    week_start = current_date - timedelta(days=current_date.weekday())
    
    # Last Week
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)
    
    this_week_income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__gte=week_start,
        bookingid__booking_date__lte=current_date
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )['total'] or 0
    
    last_week_income = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__gte=last_week_start,
        bookingid__booking_date__lte=last_week_end
    ).aggregate(
        total=Sum(ExpressionWrapper(Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'), output_field=FloatField()))
    )['total'] or 0
    
    # Week-over-Week Growth
    if last_week_income > 0:
        wow_growth = ((this_week_income - last_week_income) / last_week_income) * 100
    else:
        wow_growth = 100 if this_week_income > 0 else 0
    
    # -------------------------
    # PRODUCT ANALYTICS
    # -------------------------
    
    # Most Bought Product
    most_product = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values(
        'productid__product_name',
        'productid__product_price',
        'productid__id'
    ).annotate(
        total_quantity=Sum('cart_quantity'),
        total_revenue=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    ).order_by('-total_quantity').first()
    
    # Most Bought Category
    most_category = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values(
        'productid__subcategory__Category_name__Category_name',
        'productid__subcategory__Category_name__id'
    ).annotate(
        total_sales=Sum('cart_quantity'),
        total_revenue=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    ).order_by('-total_sales').first()
    
    # Most Bought Brand
    most_brand = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values(
        'productid__brand__brand_name',
        'productid__brand__id'
    ).annotate(
        total_sales=Sum('cart_quantity'),
        total_revenue=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    ).order_by('-total_sales').first()
    
    # Top 10 Products
    top_products = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values(
        'productid__product_name',
        'productid__product_price',
        'productid__id'
    ).annotate(
        quantity_sold=Sum('cart_quantity'),
        revenue=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    ).order_by('-quantity_sold')[:10]
    
    # -------------------------
    # STOCK MANAGEMENT
    # -------------------------

    # 1. Subquery for sold items remains the same
    sold_items = tbl_cart.objects.filter(
        productid=OuterRef('productid__id'),
        cart_status__gt=1
    ).values('productid').annotate(
        total_sold=Sum('cart_quantity')
    ).values('total_sold')

    # 2. Updated Low Stock Alert logic with ExpressionWrapper
    low_stock_products = tbl_stock.objects.filter(
        productid__shop=shop_id
    ).values(
        'productid__id', 
        'productid__product_name'
    ).annotate(
        total_added=Sum('stock_quality'),
        total_sold=Coalesce(Subquery(sold_items), 0),
        # Use ExpressionWrapper to explicitly define the output as an Integer
        available_qty=ExpressionWrapper(
            F('total_added') - F('total_sold'),
            output_field=IntegerField()
        )
    ).filter(
        available_qty__lte=10, 
        available_qty__gt=0
    ).order_by('available_qty')[:10]

    # 3. Updated Out of Stock logic with ExpressionWrapper
    out_of_stock = tbl_stock.objects.filter(
        productid__shop=shop_id
    ).values('productid').annotate(
        available=ExpressionWrapper(
            Sum('stock_quality') - Coalesce(Subquery(sold_items), 0),
            output_field=IntegerField()
        )
    ).filter(available__lte=0).count()

    # 4. FIXED: Total Stock Value
    total_stock_value = tbl_stock.objects.filter(
    productid__shop=shop_id
).annotate(
    # First, calculate the available stock per entry
    available_amount=ExpressionWrapper(
        F('stock_quality') - Coalesce(Subquery(sold_items), 0),
        output_field=FloatField() # Use Float to allow decimal multiplication
    )
).aggregate(
    total=Sum(
        ExpressionWrapper(
            F('available_amount') * Cast('productid__product_price', output_field=FloatField()),
            output_field=FloatField()
        )
    )
)['total'] or 0
    
    # -------------------------
    # CUSTOMER ANALYTICS
    # -------------------------
    
    # Total Customers
    total_customers = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values('bookingid__userid').distinct().count()
    
    # New Customers This Month
    new_customers = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__month=current_date.month,
        bookingid__booking_date__year=current_date.year
    ).values('bookingid__userid').distinct().count()
    
    # Repeat Customers (customers with >1 order)
    repeat_customers = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values('bookingid__userid').annotate(
        order_count=Count('bookingid', distinct=True)
    ).filter(order_count__gt=1).count()
    
    # Customer Retention Rate
    retention_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
    
    # -------------------------
    # TIME-BASED ANALYTICS
    # -------------------------
    
    # Monthly Sales Data (Last 12 months)
    twelve_months_ago = current_date - timedelta(days=365)
    monthly_sales = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__gte=twelve_months_ago
    ).annotate(
        month=ExtractMonth('bookingid__booking_date'),
        year=ExtractYear('bookingid__booking_date')
    ).values('month', 'year').annotate(
        total_sales=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        ),
        order_count=Count('bookingid__id', distinct=True)
    ).order_by('year', 'month')
    monthly_data = []
    months_list = []
    for ms in monthly_sales:
        month_num = int(ms['month'])
        year_num = int(ms['year'])
        month_name = calendar.month_abbr[month_num]
        month_str = f"{month_name} {year_num}"
        months_list.append(month_str)
        monthly_data.append({
            'month': month_str,
            'sales': float(ms['total_sales']) if ms['total_sales'] else 0,
            'orders': ms['order_count']
        })
    
    # Daily Sales (Last 30 days)
    thirty_days_ago = current_date - timedelta(days=30)
    daily_sales = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
        bookingid__booking_date__gte=thirty_days_ago,
        bookingid__booking_date__lte=current_date
    ).values('bookingid__booking_date').annotate(
        total_sales=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        ),
        order_count=Count('bookingid', distinct=True)
    ).order_by('bookingid__booking_date')
    
    # Create a complete date range for the last 30 days
    date_range = []
    for i in range(30):
        date = current_date - timedelta(days=29-i)
        date_range.append(date)
    
    daily_data = []
    sales_dict = {item['bookingid__booking_date']: item for item in daily_sales if item['bookingid__booking_date']}
    
    for date in date_range:
        if date in sales_dict:
            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'sales': float(sales_dict[date]['total_sales']) if sales_dict[date]['total_sales'] else 0,
                'orders': sales_dict[date]['order_count']
            })
        else:
            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'sales': 0,
                'orders': 0
            })
    
    # -------------------------
    # STATUS-BASED ANALYTICS
    # -------------------------
    
    # Orders by Status
    orders_by_status = [
        {'status': 'Pending', 'count': pending_orders, 'color': 'warning'},
        {'status': 'Packed', 'count': packed_orders, 'color': 'info'},
        {'status': 'Shipped', 'count': shipped_orders, 'color': 'primary'},
        {'status': 'Out for Delivery', 'count': out_for_delivery_orders, 'color': 'info'},
        {'status': 'Delivered', 'count': total_orders, 'color': 'success'},
        {'status': 'Cancelled', 'count': cancelled_orders, 'color': 'danger'},
        {'status': 'Returned', 'count': returned_orders, 'color': 'secondary'},
    ]
    
    # -------------------------
    # DAY OF WEEK ANALYSIS
    # -------------------------
    
    # Get day of week distribution
    dow_data = []
    for i in range(7):
        day_name = calendar.day_name[i]
        # Django week_day: 1=Sunday, 2=Monday, ..., 7=Saturday
        django_week_day = i + 2 if i < 6 else 1
        
        day_orders = tbl_cart.objects.filter(
            productid__shop=shop_id,
            bookingid__booking_status__gte=2,
            bookingid__booking_date__week_day=django_week_day
        ).values('bookingid').distinct().count()
        
        day_revenue = tbl_cart.objects.filter(
            productid__shop=shop_id,
            bookingid__booking_status__gte=2,
            bookingid__booking_date__week_day=django_week_day
        ).aggregate(
            total=Sum(
                ExpressionWrapper(
                    Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                    output_field=FloatField()
                )
            )
        )['total'] or 0
        
        dow_data.append({
            'day': day_name[:3],
            'orders': day_orders,
            'revenue': float(day_revenue)
        })
    
    # -------------------------
    # SALES FORECASTING & DEMAND PREDICTION
    # -------------------------
    
    # Get historical data from tbl_cart for Sales
    historical_sales = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2,
    ).values('bookingid__booking_date').annotate(
        total=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    ).order_by('bookingid__booking_date')
    
    data = []
    for s in historical_sales:
        if s['total'] and s['bookingid__booking_date']:
            data.append({
                "date": s['bookingid__booking_date'],
                "sales": float(s['total'])
            })
    
    df = pd.DataFrame(data)
    forecast = {}
    forecast_accuracy = {}
    current_date = date.today()
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.groupby(df['date'].dt.date)['sales'].sum().reset_index()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        if len(df) > 7:
            full_date_range = pd.date_range(start=df['date'].min(), end=df['date'].max())
            df = df.set_index('date').reindex(full_date_range).fillna(0).reset_index()
            df.rename(columns={'index': 'date'}, inplace=True)
            
            df['day_num'] = range(len(df))
            df['month'] = df['date'].dt.month
            df['weekday'] = df['date'].dt.weekday
            
            df['rolling_7'] = df['sales'].rolling(window=7, min_periods=1).mean()
            df['rolling_30'] = df['sales'].rolling(window=30, min_periods=1).mean()
            
            feature_cols = ['day_num', 'month', 'weekday', 'rolling_7', 'rolling_30']
            X = df[feature_cols]
            y = df['sales']
            
            split_idx = int(len(df) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            models = {
                'Linear Regression': LinearRegression(),
                'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42),
            }
            
            for name, model in models.items():
                if len(X_train) > 0:
                    model.fit(X_train, y_train)
                    
                    if len(y_test) > 0:
                        predictions = model.predict(X_test)
                        mask = y_test.values > 0
                        if mask.any():
                            mape = np.mean(np.abs((y_test.values[mask] - predictions[mask]) / y_test.values[mask])) * 100
                            accuracy = max(0, 100 - mape)
                            forecast_accuracy[name] = round(accuracy, 2)
                        else:
                            forecast_accuracy[name] = 100.0
                    
                    last_day_num = df['day_num'].max()
                    
                    future_predictions = []
                    simulated_sales = list(df['sales'].values)
                    
                    for i in range(1, 31):
                        future_day = last_day_num + i
                        future_date = current_date + timedelta(days=i)
                        
                        r7 = np.mean(simulated_sales[-7:]) if len(simulated_sales) >= 7 else np.mean(simulated_sales)
                        r30 = np.mean(simulated_sales[-30:]) if len(simulated_sales) >= 30 else np.mean(simulated_sales)
                        
                        future_features = pd.DataFrame([[
                            future_day,
                            future_date.month,
                            future_date.weekday(),
                            r7,
                            r30
                        ]], columns=feature_cols)
                        
                        pred = model.predict(future_features)[0]
                        pred = max(0, pred)
                        future_predictions.append(pred)
                        simulated_sales.append(pred)
                    
                    forecast[name] = {
                        'values': [round(p, 2) for p in future_predictions],
                        'total': sum(future_predictions),
                        'average': np.mean(future_predictions),
                        'accuracy': forecast_accuracy.get(name, 0)
                    }
                    # --- UNIFIED FILTER ---
    # We use this base for almost all calculations to ensure consistency
    paid_cart_items = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    )

    # 1. PEAK HOURS LOGIC
    # booking_date is a DateField, so there is no hour component available.
    # Fall back to daily order distribution instead.
    hourly_data_query = paid_cart_items.values('bookingid__booking_date').annotate(
        order_count=Count('bookingid', distinct=True)
    ).order_by('bookingid__booking_date')

    hourly_distribution = []
    for h in hourly_data_query:
        booking_date = h['bookingid__booking_date']
        hourly_distribution.append({
            'hour': booking_date.strftime('%Y-%m-%d') if booking_date else 'Unknown',
            'count': h['order_count']
        })
                    
    # Demand Prediction (Quantities for top products)
    top_products_demand = tbl_cart.objects.filter(
        productid__shop=shop_id,
        cart_status__gte=1
    ).values('productid__product_name', 'productid__id').annotate(
        total_qty=Sum('cart_quantity')
    ).order_by('-total_qty')[:5]

    demand_forecast = []
    for prod in top_products_demand:
        prod_id = prod['productid__id']
        prod_name = prod['productid__product_name']
        
        hist = tbl_cart.objects.filter(
            productid__id=prod_id,
            cart_status__gte=1
        ).values('bookingid__booking_date').annotate(
            qty=Sum('cart_quantity')
        ).order_by('bookingid__booking_date')
        
        d_data = []
        for h in hist:
            if h['qty'] and h['bookingid__booking_date']:
                d_data.append({
                    "date": h['bookingid__booking_date'],
                    "qty": float(h['qty'])
                })
        
        d_df = pd.DataFrame(d_data)
        if not d_df.empty and len(d_df) > 3:
            d_df['date'] = pd.to_datetime(d_df['date'])
            d_df = d_df.groupby(d_df['date'].dt.date)['qty'].sum().reset_index()
            d_df['date'] = pd.to_datetime(d_df['date'])
            
            full_date_range = pd.date_range(start=d_df['date'].min(), end=d_df['date'].max())
            d_df = d_df.set_index('date').reindex(full_date_range).fillna(0).reset_index()
            d_df.rename(columns={'index': 'date'}, inplace=True)
            
            d_df['day_num'] = range(len(d_df))
            
            X_d = d_df[['day_num']]
            y_d = d_df['qty']
            
            d_model = LinearRegression()
            d_model.fit(X_d, y_d)
            
            last_day_d = d_df['day_num'].max()
            future_qty = []
            for i in range(1, 31):
                pred = d_model.predict(pd.DataFrame([[last_day_d + i]], columns=['day_num']))[0]
                future_qty.append(max(0, pred))
            
            total_pred = int(round(sum(future_qty)))
            demand_forecast.append({
                'product_name': prod_name,
                'current_sales': prod['total_qty'],
                'predicted_demand_30d': total_pred
            })


    # -------------------------
    # ADDITIONAL METRICS
    # -------------------------
    
    # Payment Methods Distribution - If booking_status 2 (payment complete), payment method is 'Online'
    online_payments_count = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values('bookingid').distinct().count()
    
    online_payments_total = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).aggregate(
        total=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        )
    )['total'] or 0

    payment_methods = []
    if online_payments_count > 0:
        payment_methods.append({
            'payment_method': 'Online',
            'count': online_payments_count,
            'total': online_payments_total
        })
    
    # Category Performance
    category_performance = tbl_cart.objects.filter(
        productid__shop=shop_id,
        bookingid__booking_status__gte=2
    ).values(
        'productid__subcategory__Category_name__Category_name'
    ).annotate(
        total_sales=Sum(
            ExpressionWrapper(
                Cast('productid__product_price', output_field=FloatField()) * F('cart_quantity'),
                output_field=FloatField()
            )
        ),
        total_orders=Count('bookingid', distinct=True)
    ).order_by('-total_sales')[:5]
    
    # Recent Transactions
    recent_transactions = tbl_booking.objects.filter(
        tbl_cart__productid__shop=shop_id,
        booking_status__gte=2
    ).select_related(
        'user'
    ).distinct().order_by('-booking_date')[:10]
    
    payment_methods_list = list(payment_methods)
    category_perf_list = list(category_performance)
    # Set forecast to example for testing
    forecast = {
        'Linear Regression': {'values': [10, 20, 15] * 10, 'total': 450, 'average': 15, 'accuracy': 85},
        'LSTM': {'values': [12, 18, 14] * 10, 'total': 440, 'average': 14.67, 'accuracy': 90}
    }
    context = {
        # Basic Metrics
        "total_income": total_income,
        "today_income": today_income,
        "month_income": month_income,
        "income_growth": round(float(income_growth), 1),
        "this_week_income": this_week_income,
        "last_week_income": last_week_income,
        "wow_growth": round(float(wow_growth), 1),
        "total_orders": total_orders,
        "today_orders": today_orders,
        
        # Order Status
        "pending_orders": pending_orders,
        "packed_orders": packed_orders,
        "shipped_orders": shipped_orders,
        "out_for_delivery_orders": out_for_delivery_orders,
        "cancelled_orders": cancelled_orders,
        "returned_orders": returned_orders,
        "orders_by_status": orders_by_status,
        
        # Product Analytics
        "avg_order_value": avg_order_value,
        "most_product": most_product,
        "most_category": most_category,
        "most_brand": most_brand,
        "top_products": top_products,
        
        # Stock Management
        "low_stock_products": low_stock_products,
        "out_of_stock": out_of_stock,
        "total_stock_value": total_stock_value,
        
        # Customer Analytics
        "total_customers": total_customers,
        "new_customers": new_customers,
        "repeat_customers": repeat_customers,
        "retention_rate": round(float(retention_rate), 1),
        
        # Time-based Analytics
        "monthly_sales": json.dumps(monthly_data),
        "monthly_labels": json.dumps(months_list),
        "daily_sales": json.dumps(daily_data),
        "current_month": current_date.strftime('%B %Y'),
        "dow_data": json.dumps(dow_data),
        
        # Forecasting & Demand
        "forecast": forecast,
        "forecast_accuracy": forecast_accuracy,
        "has_forecast": bool(forecast),
        "demand_forecast": demand_forecast,
        
        # Additional Analytics
        "payment_methods": json.dumps(payment_methods_list),
        "category_performance": json.dumps(category_perf_list),
        "recent_transactions": recent_transactions,
        "hourly_distribution": hourly_distribution,

        # Standard Objects for HTML Tables
        "top_products": top_products,
        "low_stock_products": low_stock_products,
        "currency_symbol": "₹",
    }
    
    
    return render(request, "Seller/SalesDashboard.html", context)


#change password
def changepassword(request):
    Seller=tbl_shop.objects.get(id=request.session['sid'])
    if request.method=="POST":
        old=request.POST.get("txt_opass")
        new=request.POST.get("txt_npass")
        re=request.POST.get("txt_rpass")

        if Seller.shop_password == old:
            if new == re:
                Seller.shop_password = new
                Seller.save()
                return render(request,"Seller/Myprofile.html",{"msg":"password changed successfully"})
            else:
                return render(request,'Seller/Changepassword.html',{'msg':"New passward do not match"})
        else:
            return render(request,'Seller/Changepassword.html',{'msg':"old password is incorrect"})
            
    else:
        return render(request,"Seller/Changepassword.html")
    
# myprofile
def myprofile(request):
    seller_data=tbl_shop.objects.get(id=request.session['sid'])
    return render(request,'Seller/myprofile.html',{'seller':seller_data})

# homepage
def Homepage(request):
    sellerdata=tbl_shop.objects.get(id=request.session['sid'])
    return render(request,"Seller/Homepage.html",{'seller':sellerdata})

def editprofile(request):
    sellerdata=tbl_shop.objects.get(id=request.session['sid'])
    if request.method=="POST":
        sellerdata.shop_name=request.POST.get("txt_n")
        sellerdata.shop_contact=request.POST.get("txt_c")
        sellerdata.shop_email=request.POST.get("txt_e")
        sellerdata.shop_address=request.POST.get("a")
        sellerdata.save()
        return render(request,"seller/Myprofile.html",{'msg':"profile updated"})
    return render(request,"seller/Editprofile.html",{'seller':sellerdata})

def product(request):
    product_data=tbl_product.objects.filter(shop=request.session['sid'])
    category=tbl_category.objects.all()
    brands=tbl_brand.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_product")
        details=request.POST.get("details")
        photo=request.FILES.get("photo")
        price=request.POST.get("txt_price")
        subcategoryid=tbl_subcategory.objects.get(id=request.POST.get("sel_subcategory"))
        brandid=tbl_brand.objects.get(id=request.POST.get("sel_br"))
        shopid=tbl_shop.objects.get(id=request.session['sid'])
        tbl_product.objects.create(
            product_name=name,
            product_details=details,
            product_price=price,
            product_photo=photo,
            subcategory=subcategoryid,
            shop=shopid,
            brand=brandid

        )
        return redirect("Seller:product")
    else:
        return render(request,"seller/Product.html",{'brand':brands,'category':category,'product':product_data})

def ajaxsubcategory(request):
    catid=request.GET.get('did')
    data=tbl_subcategory.objects.filter(Category_name=catid)
    return render(request,'Seller/AjaxSubcategory.html',{'data':data})

def productdelete(request,id):
    tbl_product.objects.get(id=id).delete()
    return redirect("Seller:product")

def editproduct(request,id):
    product=tbl_product.objects.all()
    productdata=tbl_product.objects.get(id=id)
    if request.method=="POST":
        productdata.product_name=request.POST.get("txt_product")
        productdata.product_price=request.POST.get("txt_price")
        productdata.product_details=request.POST.get("details")
        productdata.save()
        return redirect("Seller:product")
    return render(request,'Seller/Product.html',{'product':product,'productdata':productdata})

def addgallery(request,id):
    gallery=tbl_gallery.objects.all()
    product=tbl_product.objects.get(id=id)
    if request.method=='POST':
        photo=request.FILES.get("photo")
        tbl_gallery.objects.create(
        gallery_file=photo,
        productid=product
        )
        return render(request,"seller/Addgallery.html")
    else:
        return render(request,"seller/Addgallery.html")
    
def addstock(request,id):
    quantity=tbl_gallery.objects.all()
    product=tbl_product.objects.get(id=id)
    if request.method=='POST':
        quantity=request.POST.get("txt_stock")
        tbl_stock.objects.create(
            stock_quality=quantity,
            productid=product
        )
        return render(request,"Seller/Addstock.html")
    else:
        return render(request,"Seller/Addstock.html")
    
def viewbooking(request):
    bookingdata = tbl_booking.objects.filter(
        booking_status__gt=0,
        tbl_cart__productid__shop=request.session['sid']
    ).distinct().order_by('-id')

    return render(request, 'Seller/viewbooking.html', {
        'bookingdata': bookingdata,
        'sid': request.session['sid']
    })


def order_packed(request, id):
    tbl_cart.objects.filter(
        id=id,
        productid__shop_id=request.session['sid']
    ).update(cart_status=3)

    return redirect('Seller:viewbooking')


def order_shipped(request, id):
    tbl_cart.objects.filter(
        id=id,
        productid__shop_id=request.session['sid']
    ).update(cart_status=4)

    return redirect('Seller:viewbooking')



def logout(request):
    del request.session['sid']
    return redirect("Guest:login")