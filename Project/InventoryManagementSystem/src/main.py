import streamlit as st
from helpers import read_inventory, write_inventory, add_order_record

def main():
    st.title("📦 Inventory & Order Management")

    # Load inventory into session_state so it persists across interactions
    if "inventory" not in st.session_state:
        st.session_state.inventory = read_inventory()

    inventory = st.session_state.inventory

    # Step 1: Choose genre
    st.header("Select a Genre")
    genres = list(inventory.keys())
    genre = st.selectbox("Available Genres", genres)

    # Step 2: Choose product
    if genre:
        st.header("Select a Product")
        products = list(inventory[genre].keys())
        product_choice = st.selectbox(
            "Available Products",
            products,
            format_func=lambda p: f"{p} (Stock: {inventory[genre][p]['availableStock']}, Price: {inventory[genre][p]['price']})"
        )

        # Step 3: Enter quantity and checkout form
        if product_choice:
            max_stock = inventory[genre][product_choice]["availableStock"]
            qty = st.number_input("Enter quantity", min_value=1, max_value=max_stock, step=1)

            with st.form("order_form"):
                st.subheader("Checkout")
                name = st.text_input("Your Name")
                payment_method = st.selectbox("Payment Method", ["Cash", "Card", "Online"])
                submit_btn = st.form_submit_button("Place Order")

                if submit_btn:
                    if qty <= max_stock:
                        # Update inventory
                        st.session_state.inventory[genre][product_choice]["availableStock"] -= qty
                        price = inventory[genre][product_choice]["price"] * qty

                        # Save changes
                        write_inventory(st.session_state.inventory)
                        add_order_record(name, product_choice, price, payment_method)

                        st.success(f"✅ Order placed successfully for {qty} {product_choice}(s). Total = {price}")
                    else:
                        st.error("❌ Invalid quantity entered.")

    # Show inventory status
    st.sidebar.header("📊 Current Inventory")
    for g, items in inventory.items():
        st.sidebar.write(f"**{g}**")
        for p, details in items.items():
            st.sidebar.write(f"- {p}: {details['availableStock']} left @ {details['price']}")

if __name__ == "__main__":
    main()
