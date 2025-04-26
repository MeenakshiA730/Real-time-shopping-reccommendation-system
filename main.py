import gradio as gr
import pandas as pd

# Load the dataset
df = pd.read_csv("processed_customer_shopping_data.csv")

# Helper: Age bins
def age_group(age):
    if age < 20:
        return "<20"
    elif age < 30:
        return "20-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    else:
        return "60+"

df["age_group"] = df["age"].apply(age_group)

def recommend(gender, age_range, category, mall, price_min, price_max, quantity):
    # Filter data
    filtered = df[
        (df["gender"] == gender) &
        (df["age_group"] == age_range) &
        (df["category"] == category) &
        (df["shopping_mall"] == mall) &
        (df["price"] >= price_min) &
        (df["price"] <= price_max) &
        (df["quantity"] >= quantity)
    ]

    if filtered.empty:
        return "No matching products found. Try adjusting filters."

    top = filtered.sort_values(by="total_price", ascending=False).head(3)
    recommendations = ""
    for i, row in top.iterrows():
        recommendations += f"\n🛍️ **Item {i+1}**\n"
        recommendations += f"Category: {row['category']}\n"
        recommendations += f"Price: {row['price']}\n"
        recommendations += f"Quantity: {row['quantity']}\n"
        recommendations += f"Shopping Mall: {row['shopping_mall']}\n"
        recommendations += f"Date: {row['invoice_date']}\n"
        recommendations += f"Payment: {row['payment_method']}\n"
        recommendations += f"---\n"
    return recommendations

# Interface
gender_opts = df["gender"].unique().tolist()
age_opts = sorted(df["age_group"].unique())
category_opts = df["category"].unique().tolist()
mall_opts = df["shopping_mall"].unique().tolist()

with gr.Blocks() as demo:
    gr.Markdown("# 🛒 Real-Time Shopping Recommendation System")
    
    with gr.Row():
        gender = gr.Dropdown(label="Gender", choices=gender_opts)
        age_group_input = gr.Dropdown(label="Age Group", choices=age_opts)
        category = gr.Dropdown(label="Category", choices=category_opts)
        mall = gr.Dropdown(label="Shopping Mall", choices=mall_opts)

    with gr.Row():
        price_slider = gr.Slider(label="Price Range (Min)", minimum=0, maximum=5000, step=50, value=100)
        price_slider_max = gr.Slider(label="Price Range (Max)", minimum=0, maximum=10000, step=50, value=3000)
        quantity = gr.Number(label="Minimum Quantity", value=1, precision=0)

    output = gr.Textbox(label="Recommendations", lines=10)
    btn = gr.Button("Get Recommendations")

    btn.click(fn=recommend, inputs=[gender, age_group_input, category, mall, price_slider, price_slider_max, quantity], outputs=output)

# For Hugging Face Spaces
demo.launch()
