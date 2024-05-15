import streamlit as st

# Dictionary containing item prices
item_prices = {
    'Item A': 10,
    'Item B': 20,
    'Item C': 30
}

def generate_invoice(customer_name, items):
    total_amount = sum(item['price'] * item['quantity'] for item in items)
    return f"Invoice for: {customer_name}\nTotal amount: ${total_amount:.2f}"

def main():
    st.title('Billing App')

    customer_name = st.text_input('Customer Name')

    # Initialize items as an empty list
    if 'items' not in st.session_state:
        st.session_state['items'] = []

    item_name = st.selectbox('Select Item', list(item_prices.keys()))
    quantity = st.number_input('Quantity', min_value=1, value=1)

    add_item_button = st.button('Add Item')
    if add_item_button:
        items = st.session_state['items']  # Retrieve items from session state
        items.append({'name': item_name, 'quantity': quantity, 'price': item_prices[item_name]})
        st.session_state['items'] = items  # Update session state with new items

    if st.button('Generate Invoice'):
        invoice_text = generate_invoice(customer_name, st.session_state['items'])
        st.text_area('Invoice', invoice_text)

if __name__ == "__main__":
    main()
