import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker("en_IN")

np.random.seed(42)

# ==========================================
# CONFIG
# ==========================================

NUM_RECORDS = 15000

# ==========================================
# PRODUCTS
# ==========================================

products = {
    "Electronics": {
        "Laptop": (40000, 90000),
        "Smartphone": (10000, 70000),
        "Tablet": (12000, 50000),
        "Smartwatch": (2000, 20000),
        "Headphones": (1000, 10000),
        "Monitor": (5000, 30000),
        "Keyboard": (500, 5000),
        "Mouse": (300, 3000)
    },

    "Fashion": {
        "T-Shirt": (300, 1500),
        "Jeans": (800, 3000),
        "Jacket": (1200, 6000),
        "Shoes": (1000, 7000),
        "Kurti": (500, 3000),
        "Handbag": (700, 5000)
    },

    "Home": {
        "Sofa": (15000, 70000),
        "Bed": (10000, 50000),
        "Chair": (1000, 8000),
        "Lamp": (500, 4000),
        "Dining Table": (5000, 30000)
    },

    "Beauty": {
        "Face Wash": (150, 500),
        "Serum": (300, 1500),
        "Sunscreen": (200, 1000),
        "Moisturizer": (250, 1200),
        "Perfume": (500, 5000)
    },

    "Grocery": {
        "Rice": (200, 1200),
        "Tea": (150, 700),
        "Coffee": (250, 1200),
        "Cooking Oil": (100, 900),
        "Sugar": (50, 300)
    }
}

# ==========================================
# CATEGORY WEIGHTS
# ==========================================

categories = list(products.keys())

category_weights = [
    0.35,  # Electronics
    0.25,  # Fashion
    0.15,  # Home
    0.10,  # Beauty
    0.15   # Grocery
]

# ==========================================
# REGIONS
# ==========================================

regions = {
    "North": {
        "Uttar Pradesh": ["Lucknow", "Kanpur"],
        "Delhi": ["New Delhi", "Dwarka"],
        "Punjab": ["Ludhiana", "Amritsar"]
    },

    "South": {
        "Karnataka": ["Bangalore", "Mysore"],
        "Tamil Nadu": ["Chennai", "Coimbatore"],
        "Telangana": ["Hyderabad", "Warangal"]
    },

    "East": {
        "West Bengal": ["Kolkata", "Siliguri"],
        "Bihar": ["Patna", "Gaya"],
        "Odisha": ["Bhubaneswar", "Cuttack"]
    },

    "West": {
        "Maharashtra": ["Mumbai", "Pune"],
        "Gujarat": ["Ahmedabad", "Surat"],
        "Rajasthan": ["Jaipur", "Jodhpur"]
    }
}

region_weights = [0.30, 0.28, 0.17, 0.25]

# ==========================================
# CUSTOMER POOL
# ==========================================

customer_pool = [
    f"CUST{i:05d}"
    for i in range(1, 2501)
]

customer_segments = [
    "Consumer",
    "Corporate",
    "Home Office"
]

segment_weights = [
    0.60,
    0.25,
    0.15
]

# ==========================================
# PAYMENT
# ==========================================

payment_modes = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash"
]

payment_weights = [
    0.45,
    0.25,
    0.20,
    0.10
]

# ==========================================
# CHANNELS
# ==========================================

sales_channels = [
    "Online",
    "Offline"
]

channel_weights = [
    0.65,
    0.35
]

# ==========================================
# GENERATE DATA
# ==========================================

rows = []

for i in range(NUM_RECORDS):

    order_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    month = order_date.month

    if month in [10, 11]:
        seasonal_multiplier = 1.40
        festival = "Diwali Season"

    elif month == 12:
        seasonal_multiplier = 1.25
        festival = "Year End Sale"

    else:
        seasonal_multiplier = 1.00
        festival = "Regular"

    category = np.random.choice(
        categories,
        p=category_weights
    )

    product = np.random.choice(
        list(products[category].keys())
    )

    price_low, price_high = products[category][product]

    region = np.random.choice(
        list(regions.keys()),
        p=region_weights
    )

    state = np.random.choice(
        list(regions[region].keys())
    )

    city = np.random.choice(
        regions[region][state]
    )

    customer_id = np.random.choice(customer_pool)

    quantity = np.random.randint(1, 6)

    unit_price = np.random.randint(
        price_low,
        price_high
    )

    discount = np.random.choice(
        [0, 5, 10, 15, 20, 25, 30],
        p=[0.20, 0.20, 0.20, 0.15, 0.10, 0.10, 0.05]
    )

    sales = (
        quantity *
        unit_price *
        (1 - discount/100) *
        seasonal_multiplier
    )

    shipping_cost = sales * np.random.uniform(
        0.02,
        0.08
    )

    if discount >= 25:

        profit_margin = np.random.uniform(
            -0.05,
            0.08
        )

    else:

        profit_margin = np.random.uniform(
            0.12,
            0.35
        )

    profit = sales * profit_margin

    cost = sales - profit

    rating = round(
        np.clip(
            np.random.normal(4.2, 0.5),
            1,
            5
        ),
        1
    )

    status = np.random.choice(
        ["Delivered", "Returned"],
        p=[0.94, 0.06]
    )

    delivery_days = np.random.randint(
        1,
        10
    )

    customer_type = np.random.choice(
        ["New", "Returning"],
        p=[0.25, 0.75]
    )

    rows.append([
        f"ORD{i+1:06d}",
        order_date,
        customer_id,
        customer_type,
        np.random.choice(
            customer_segments,
            p=segment_weights
        ),
        region,
        state,
        city,
        category,
        product,
        quantity,
        unit_price,
        discount,
        round(sales, 2),
        round(cost, 2),
        round(profit, 2),
        round(shipping_cost, 2),
        np.random.choice(
            payment_modes,
            p=payment_weights
        ),
        np.random.choice(
            sales_channels,
            p=channel_weights
        ),
        status,
        delivery_days,
        rating,
        order_date.month,
        order_date.strftime("%B"),
        ((order_date.month - 1) // 3) + 1,
        festival
    ])

# ==========================================
# DATAFRAME
# ==========================================

columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Customer_Type",
    "Customer_Segment",
    "Region",
    "State",
    "City",
    "Category",
    "Product_Name",
    "Quantity",
    "Unit_Price",
    "Discount_Percent",
    "Sales",
    "Cost",
    "Profit",
    "Shipping_Cost",
    "Payment_Mode",
    "Sales_Channel",
    "Order_Status",
    "Delivery_Days",
    "Product_Rating",
    "Month",
    "Month_Name",
    "Quarter",
    "Festival_Season"
]

df = pd.DataFrame(
    rows,
    columns=columns
)
df = df.sort_values("Order_Date")

# ==========================================
# SAVE
# ==========================================


# Save dataset inside Data folder
df.to_csv(
    os.path.join("Data", "retail_sales_15000.csv"),
    index=False
)
print("\nDataset Created Successfully!")
print(df.head())
print("\nShape:", df.shape)