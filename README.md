# 🧴 Personal Care Product Catalog Validator

A robust data pipeline and interactive web interface built with **Pydantic V2** and **Streamlit**. This project demonstrates advanced data validation, nested models, dynamic computed fields, and JSON exporting.

---

## ❓ Why This Project?

In modern web development and AI applications, **data integrity is paramount**. Raw user inputs from frontend forms or uncontrolled web scrapers are notorious for being messy, incomplete, or fundamentally broken. 

Building complex `if/else` logic blocks to manually check every incoming variable is tedious, prone to human error, and doesn't scale. This project serves as a lightweight, industrial-grade blueprint showing how to offload structural validation entirely to **Pydantic**, leaving your application logic clean and deterministic.

---

## 🛠️ Problem It Solves

When running software applications (such as a product catalog or an inventory management pipeline), you constantly face structural and logical inconsistencies. This project directly solves the following problems:

*   **The "Dirty Data" Problem:** Slips like typing string characters into a price field or submitting structurally invalid URLs (`glownaturals-example.com` instead of `https://glownaturals-example.com`) are caught instantly before hitting your database.
*   **The "Silent Logic Fail" Problem:** A discount value of `-15%` or `150%` passes generic number validations but wrecks your financial logic. Pydantic's model-level validators catch cross-field logical contradictions before they cause business logic issues.
*   **The "Stale Derivations" Problem:** Manually updating calculated fields (like a combined product summary or a discounted selling price) everywhere in your code creates desync issues. **Computed fields** guarantee that derivations always adapt dynamically to the source data.
*   **Frontend-Backend Disconnect:** Instead of writing complex form validation on the client side and repeating it on the server, your Pydantic schemas serve as a single, immutable source of truth for both structural constraints and real-time frontend UI feedback via Streamlit.

---

## ✨ Features

*   **Strict Type Validation:** Ensures incoming data matches exact types (e.g., `float` for prices, `bool` for flags).
*   **Nested Models:** Uses a nested `BrandInfo` model within the main `SkincareProduct` schema for a clean, relational hierarchy.
*   **Custom Field Validators:** Prevents zero/negative pricing and ensures active ingredient lists aren't empty.
*   **Model Validators:** Enforces cross-field logical rules (e.g., discounts must be between 0 and 99%).
*   **Computed Fields:** Dynamically calculates the final selling price and generates a product summary string at runtime.
*   **Interactive Web UI:** Provides a user-friendly form to input data and immediately see validation results or Pydantic errors via Streamlit.
*   **JSON Export:** Easily dumps validated models to standard JSON format, ready for storage or API consumption.

---

---

## 💻 Usage

To run the interactive Streamlit application:


