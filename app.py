import streamlit as st
from pydantic import BaseModel, AnyUrl, field_validator, model_validator, computed_field, ValidationError
from typing import List

# ==========================================
# 1. EXACT SAME PYDANTIC CODE
# ==========================================
class BrandInfo(BaseModel):
    name: str
    website: AnyUrl
    cruelty_free: bool

class SkincareProduct(BaseModel):
    sku: str
    name: str
    brand: BrandInfo  
    base_price: float
    discount_percentage: float = 0.0
    active_ingredients: List[str]

    @field_validator('base_price')
    @classmethod
    def validate_positive_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Base price must be greater than zero.")
        return value

    @field_validator('active_ingredients')
    @classmethod
    def validate_ingredients(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("Product must contain at least one active ingredient.")
        return [ingredient.title() for ingredient in value]

    @model_validator(mode='after')
    def validate_discount_logic(self):
        if self.discount_percentage < 0 or self.discount_percentage >= 100:
            raise ValueError("Discount percentage must be between 0 and 99.")
        return self

    @computed_field
    def final_price(self) -> float:
        discount_amount = self.base_price * (self.discount_percentage / 100)
        return round(self.base_price - discount_amount, 2)

    @computed_field
    def product_summary(self) -> str:
        return f"{self.brand.name} {self.name} - Featuring {', '.join(self.active_ingredients)}"

# ==========================================
# 2. STREAMLIT UI & LOGIC
# ==========================================
st.set_page_config(page_title="Product Validator", layout="centered")

st.title("🧴 Product Catalog Validator")
st.markdown("Enter the product details below. Pydantic will strictly validate the data upon submission.")

# Create a form to group inputs
with st.form("product_form"):
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        sku = st.text_input("SKU", value="SKU-1001")
    with col2:
        name = st.text_input("Product Name", value="Vitamin C Serum")

    st.subheader("Brand Details (Nested Model)")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        brand_name = st.text_input("Brand Name", value="GlowNaturals")
        cruelty_free = st.checkbox("Cruelty Free?", value=True)
    with b_col2:
        brand_website = st.text_input("Brand Website URL", value="https://www.glownaturals-example.com")

    st.subheader("Pricing & Ingredients")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        base_price = st.number_input("Base Price ($)", value=25.00, step=1.0)
    with p_col2:
        discount = st.number_input("Discount (%)", value=10.0, step=1.0)
        
    ingredients_raw = st.text_area(
        "Active Ingredients (Comma separated)", 
        value="vitamin c, hyaluronic acid"
    )

    # Submit button
    submitted = st.form_submit_button("Validate and Export")

# ==========================================
# 3. VALIDATION EXECUTION
# ==========================================
if submitted:
    # Process the raw comma-separated string into a list for Pydantic
    ingredient_list = [i.strip() for i in ingredients_raw.split(",") if i.strip()]

    # Construct the raw dictionary
    raw_payload = {
        "sku": sku,
        "name": name,
        "brand": {
            "name": brand_name,
            "website": brand_website,
            "cruelty_free": cruelty_free
        },
        "base_price": base_price,
        "discount_percentage": discount,
        "active_ingredients": ingredient_list
    }

    try:
        # Attempt to instantiate the Pydantic model
        product = SkincareProduct(**raw_payload)
        
        st.success("✅ Data Successfully Validated!")
        
        # Display the Computed Fields
        st.info(f"**Computed Summary:** {product.product_summary}")
        st.info(f"**Computed Final Price:** ${product.final_price}")
        
        # Display the exported JSON
        st.subheader("Exported JSON Payload")
        st.json(product.model_dump_json())

    except ValidationError as e:
        st.error("❌ Data Validation Failed!")
        # Loop through Pydantic errors and display them nicely
        for err in e.errors():
            field = " -> ".join([str(loc) for loc in err['loc']])
            st.warning(f"**Field `{field}`:** {err['msg']}")
