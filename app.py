import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Rajesh Mahale | Hyperlocal Delivery Engine",
    page_icon="🚚",
    layout="wide"
)

# Header Section
st.title("🚚 Rajesh Mahale's Hyperlocal Commerce Network")
st.caption("Community-Powered Delivery Platform: Local Stores • Direct Fulfillment • Crowdsourced Riders")
st.markdown("---")

# In-Memory Session State for Prototype Testing
if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": "ORD-101",
            "store": "Kisan Fresh Dairy",
            "category": "Dairy",
            "item": "Fresh Raw Cow Milk (1 Litre - Unpackaged)",
            "customer": "Customer A (Panchavati)",
            "status": "Pending Store Action",
            "assigned_to": "None",
            "delivery_fee": "₹25"
        },
        {
            "id": "ORD-102",
            "store": "Shree Ganesh Kirana",
            "category": "Kirana",
            "item": "Toor Dal (1kg), Basmati Rice (2kg), Garam Masala",
            "customer": "Customer B (Nandur Naka)",
            "status": "Broadcast to Community",
            "assigned_to": "None",
            "delivery_fee": "₹35"
        }
    ]

# Navigation / Role Switcher
role = st.sidebar.radio(
    "Choose Active Interface View:",
    ["1. Customer View (Place Order)", "2. Store Owner Portal", "3. Community Earning Mode", "4. Live Order Monitor"]
)

# -----------------------------------------------------------------------------
# 1. CUSTOMER VIEW
# -----------------------------------------------------------------------------
if role == "1. Customer View (Place Order)":
    st.subheader("🛒 Place an Order with a Local Store")
    
    col1, col2 = st.columns(2)
    with col1:
        store_type = st.selectbox("Store Category", ["Dairy", "Kirana / General", "Bakery", "Medical"])
        store_name = st.selectbox("Select Nearby Merchant", [
            "Kisan Fresh Dairy (400m away)",
            "Gokul Taza Milk Center (700m away)",
            "Shree Ganesh Kirana (350m away)",
            "Mahesh Provisions (1.1km away)"
        ])
    with col2:
        customer_area = st.text_input("Delivery Location", value="Panchavati, Nashik")
        items = st.text_area("Item Details (e.g., Fresh milk, spices, loose grains)", height=100)

    if st.button("Submit Order to Local Store"):
        if items.strip():
            new_id = f"ORD-{len(st.session_state.orders) + 101}"
            st.session_state.orders.append({
                "id": new_id,
                "store": store_name.split(" (")[0],
                "category": store_type,
                "item": items,
                "customer": f"Customer ({customer_area})",
                "status": "Pending Store Action",
                "assigned_to": "None",
                "delivery_fee": "₹30"
            })
            st.success(f"Order #{new_id} placed directly with {store_name}! Awaiting store confirmation.")
        else:
            st.warning("Please enter item details.")

# -----------------------------------------------------------------------------
# 2. STORE OWNER PORTAL
# -----------------------------------------------------------------------------
elif role == "2. Store Owner Portal":
    st.subheader("🏪 Merchant Dashboard: Direct Fulfillment")
    st.write("Stores receive orders first. You can deliver it yourself to pocket the delivery fee, or pass it to local community riders.")
    
    store_orders = [o for o in st.session_state.orders if o["status"] == "Pending Store Action"]
    
    if not store_orders:
        st.info("No incoming orders awaiting store action right now.")
    else:
        for order in store_orders:
            with st.container():
                st.markdown(f"### Order ID: `{order['id']}` — {order['store']}")
                st.write(f"**Items:** {order['item']}")
                st.write(f"**Customer:** {order['customer']}")
                st.write(f"**Delivery Earning:** {order['delivery_fee']}")
                
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button(f"Deliver Myself (Earn {order['delivery_fee']})", key=f"self_{order['id']}"):
                        order["status"] = "Out for Delivery (Store Owner)"
                        order["assigned_to"] = f"{order['store']} (Owner Self-Delivery)"
                        st.rerun()
                with b_col2:
                    if st.button("Pass to Community Riders", key=f"skip_{order['id']}"):
                        order["status"] = "Broadcast to Community"
                        st.rerun()
                st.markdown("---")

# -----------------------------------------------------------------------------
# 3. COMMUNITY EARNING MODE
# -----------------------------------------------------------------------------
elif role == "3. Community Earning Mode":
    st.subheader("🛵 Community Rider Network")
    st.write("Anyone nearby heading in the same direction can pick up skipped orders to earn extra income.")
    
    community_orders = [o for o in st.session_state.orders if o["status"] == "Broadcast to Community"]
    
    if not community_orders:
        st.info("No active community delivery requests nearby right now.")
    else:
        for order in community_orders:
            with st.container():
                st.markdown(f"### Pickup from: **{order['store']}**")
                st.write(f"**Dropoff:** {order['customer']}")
                st.write(f"**Item Summary:** {order['item']}")
                st.write(f"**Payout:** :green[{order['delivery_fee']}]")
                
                rider_name = st.text_input("Enter your name to claim delivery:", key=f"rider_{order['id']}")
                if st.button("Accept & Pick Up Order", key=f"claim_{order['id']}"):
                    if rider_name.strip():
                        order["status"] = "Out for Delivery (Community Rider)"
                        order["assigned_to"] = f"Community Member: {rider_name}"
                        st.rerun()
                    else:
                        st.warning("Please enter your name first.")
                st.markdown("---")

# -----------------------------------------------------------------------------
# 4. LIVE ORDER MONITOR
# -----------------------------------------------------------------------------
elif role == "4. Live Order Monitor":
    st.subheader("📊 Live Network Activity")
    df = pd.DataFrame(st.session_state.orders)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.markdown("**Platform Status:** All services operational.")