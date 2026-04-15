import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("products_asos.csv", on_bad_lines="skip")
print(df.head())

# Clean price column
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df = df.dropna(subset=["price"])

print(f"Data Loaded: {len(df)} rows")

# -----------------------------
# PRIMARY BRAND EXTRACTION (BEST METHOD)
# -----------------------------
def extract_brand_from_url(url):
    try:
        return url.split("asos.com/")[1].split("/")[0].replace("-", " ").title()
    except IndexError:
        return "Unknown"

df["Brand"] = df["url"].apply(extract_brand_from_url)

# Optional standardization (small improvement)
brand_map = {
    "Asos Design": "ASOS DESIGN",
    "Pull Bear": "Pull&Bear",
    "New Look": "New Look",
    "River Island": "River Island",
    "Stradivarius": "Stradivarius",
    "Topshop": "Topshop"
}

df["Brand"] = df["Brand"].replace(brand_map)

# -----------------------------
# SECONDARY BRAND EXTRACTIONS (FOR LEARNING ONLY)
# -----------------------------
# These columns help you understand alternative methods
# but DO NOT overwrite the main Brand column

df["description"] = df["description"].astype(str)

def get_brand(text):
    if "by" in text:
        try:
            return text.split("by")[1].split()[0]
        except IndexError:
            return "Unknown"
    return "Unknown"

df["brand_from_description"] = df["description"].apply(get_brand)

def extract_brand_from_name(name):
    words = str(name).split()
    return " ".join(words[:2])

df["brand_from_name"] = df["name"].apply(extract_brand_from_name)

print(df[["name", "Brand", "brand_from_name", "brand_from_description", "price"]].head())
df["brand_mismatch"] = df["Brand"] != df["brand_from_name"]
df["brand_mismatch"].value_counts()


df[df["brand_mismatch"]][["name", "Brand", "brand_from_name", "price"]].head(10)


df.shape





# --------------------------------------------------------------------------------------------------



# Price statistics by brand
brand_stats = df.groupby('Brand')['price'].agg(['count', 'mean', 'median', 'std']).round(2)
brand_stats = brand_stats.sort_values('count', ascending=False)
print("Brand Price Statistics:")
print(brand_stats.head(10))

# Price ranges
print(f"\nPrice Range Analysis:")
print(f"Min Price: £{df['price'].min():.2f}")
print(f"Max Price: £{df['price'].max():.2f}")
print(f"Average Price: £{df['price'].mean():.2f}")
print(f"Median Price: £{df['price'].median():.2f}")

# Enhanced Price Distribution Visualization
plt.figure(figsize=(14, 8))
plt.style.use('seaborn-v0_8')

# Create the histogram with custom styling
ax = sns.histplot(data=df, x='price', bins=60, kde=True, 
                  color="#2EAB86", alpha=0.7, edgecolor='white', linewidth=0.5)

# Add vertical lines for mean and median
mean_price = df['price'].mean()
median_price = df['price'].median()

plt.axvline(mean_price, color='#F24236', linestyle='--', linewidth=2, 
            label=f'Mean: £{mean_price:.2f}')
plt.axvline(median_price, color='#F5A623', linestyle='-', linewidth=2, 
            label=f'Median: £{median_price:.2f}')

# Customize the plot
plt.title('ASOS Product Price Distribution', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Price (£)', fontsize=12, fontweight='semibold')
plt.ylabel('Number of Products', fontsize=12, fontweight='semibold')

# Add grid for better readability
plt.grid(True, alpha=0.3, linestyle='--')

# Customize ticks
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Add legend
plt.legend(fontsize=11, loc='upper right')

# Add text annotations
plt.text(0.02, 0.98, f'Total Products: {len(df):,}', 
         transform=ax.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Tight layout and save
plt.tight_layout()
plt.savefig('asos_price_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()  # Commented out to prevent hanging in non-interactive environments

# Enhanced Brand Distribution Visualization
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-v0_8')

brand_counts = df['Brand'].value_counts().head(10)

# Create horizontal bar plot for better readability
colors = sns.color_palette('viridis', len(brand_counts))
bars = plt.barh(brand_counts.index, brand_counts.values, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)

# Add value labels on bars
for bar, value in zip(bars, brand_counts.values):
    plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
             f'{value:,}', ha='left', va='center', fontsize=10, fontweight='semibold')

# Customize the plot
plt.title('Top 10 Brands by Product Count on ASOS', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Products', fontsize=12, fontweight='semibold')
plt.ylabel('Brand', fontsize=12, fontweight='semibold')

# Add grid for better readability
plt.grid(True, alpha=0.3, linestyle='--', axis='x')

# Customize ticks
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Add text annotation
plt.text(0.02, 0.98, f'Top 10 of {df["Brand"].nunique()} total brands', 
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Tight layout and save
plt.tight_layout()
plt.savefig('asos_brand_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()  # Commented out to prevent hanging in non-interactive environments

# Save processed data and statistics
print("\n💾 Saving results...")
df.to_csv('processed_asos_data.csv', index=False)
brand_stats.to_csv('brand_price_statistics.csv', index=False)
print("✅ Processed data saved to 'processed_asos_data.csv'")
print("✅ Brand statistics saved to 'brand_price_statistics.csv'")
print("✅ Visualizations saved as PNG files")

print(f"\n🎉 Analysis complete! Processed {len(df)} products from {df['Brand'].nunique()} brands.")


