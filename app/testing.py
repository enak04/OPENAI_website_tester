from rapidfuzz import process

categories = [
  "Pharmacy",
  "General Store",
  "Fruits & Vegetables",
  "Meat Shop",
  "Bakery Shop",
  "Mobile Store",
  "Electronics Shop",
  "Restaurant",
  "Book Shop",
  "Beauty Store",
  "Clothing Store",
  "Gift Shop",
  "Hardware Shop",
  "Service & Repair",
  "Saloon Shop",
  "Computer & Accessories Shop",
  "Home & Kitchen Appliance",
  "Photostat & Telecom",
  "Watch Store",
  "Fashion"
]



def resolve_category(user_input, categories, threshold=80):

    normalized_map = {cat.lower(): cat for cat in categories}
    normalized_categories = list(normalized_map.keys())

    # Convert to lowercase for consistent matching
    user_input = user_input.lower().strip()
    match, score, _ = process.extractOne(user_input, normalized_categories)
    return normalized_map[match] if score >= threshold else None

input_category = "Beauty and Wellness"
fuzzymatchedbusiness_category = resolve_category( input_category, categories)
print(fuzzymatchedbusiness_category)