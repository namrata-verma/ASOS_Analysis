# asos.py - ASOS Product Analysis Engine 

## What `asos.py` Does

- Loads `products_asos.csv` with robust CSV parsing
- Cleans `price` using `pd.to_numeric(..., errors='coerce')`
- Drops rows with missing price values
- Extracts brands from ASOS product URLs
- Applies a brand standardization map for known variations
- Computes secondary brand extraction methods for validation
- Generates summary statistics and saves the results
- Creates two polished PNG visualizations

## Library Dependencies

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## Data Loading

```python
df = pd.read_csv("products_asos.csv", on_bad_lines="skip")
```
- Loads the CSV while skipping malformed lines
- Prints the first 5 rows for a quick sanity check
- Reports the cleaned record count after price conversion

## Price Cleaning

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df = df.dropna(subset=["price"])
```
- Converts price strings to numeric values
- Removes rows with invalid or missing prices

## Brand Extraction

### Primary Extraction

```python
def extract_brand_from_url(url):
    try:
        return url.split("asos.com/")[1].split("/")[0].replace("-", " ").title()
    except IndexError:
        return "Unknown"
```
- Parses the brand directly from the ASOS URL path
- Uses title casing and hyphen replacement for readability
- Falls back to `Unknown` for malformed URLs

### Standardization Map

```python
brand_map = {
    "Asos Design": "ASOS DESIGN",
    "Pull Bear": "Pull&Bear",
    "New Look": "New Look",
    "River Island": "River Island",
    "Stradivarius": "Stradivarius",
    "Topshop": "Topshop"
}

df["Brand"] = df["Brand"].replace(brand_map)
```
- Normalizes brand names for consistent grouping
- Prevents duplicate brand labels where URL formatting varies

## Secondary Validation Methods

### Description-Based Extraction

```python
def get_brand(text):
    if "by" in text:
        try:
            return text.split("by")[1].split()[0]
        except IndexError:
            return "Unknown"
    return "Unknown"

df["brand_from_description"] = df["description"].astype(str).apply(get_brand)
```
- Extracts a candidate brand from the description field
- Helps compare URL-based extraction against other heuristics

### Name-Based Extraction

```python
def extract_brand_from_name(name):
    words = str(name).split()
    return " ".join(words[:2])

df["brand_from_name"] = df["name"].apply(extract_brand_from_name)
```
- Uses the first two words of the product name as a fallback brand heuristic
- Used only for comparison, not to overwrite the main `Brand`

## Quality Check

```python
df["brand_mismatch"] = df["Brand"] != df["brand_from_name"]
df["brand_mismatch"].value_counts()
```
- Tracks mismatches between URL-derived and name-derived brand values
- Outputs the first 10 mismatch examples for review

## Price Statistics

```python
brand_stats = df.groupby('Brand')['price'].agg(['count', 'mean', 'median', 'std']).round(2)
```
- Computes count, mean, median, and standard deviation by brand
- Sorts brands by product count for top-brand insight

## Visualizations

### Price Distribution Chart
- Produces `asos_price_distribution.png`
- Uses a styled histogram with KDE curve
- Draws mean and median reference lines
- Adds total product count annotation

### Brand Count Chart
- Produces `asos_brand_distribution.png`
- Creates a horizontal bar chart of the top 10 brands
- Shows product counts directly on the bars

## Output Files

The script saves:
- `processed_asos_data.csv` — cleaned dataset with brand fields
- `brand_price_statistics.csv` — summary statistics by brand
- `asos_price_distribution.png` — price distribution visualization
- `asos_brand_distribution.png` — top brand count visualization

## Notes

- `matplotlib` and `seaborn` are used for plotting styles
- `plt.show()` is disabled to avoid hanging in non-interactive runs
- The script is currently a single-file analysis engine, so it runs directly from `asos.py`

