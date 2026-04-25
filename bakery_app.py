import streamlit as st
import re

st.set_page_config(page_title="Sweet Crust Bakery AI Assistant")

MENU = {
    "cupcakes": ["vanilla", "chocolate", "strawberry", "red velvet"],
    "brownies": ["chocolate", "vanilla"],
    "cakes": ["vanilla", "chocolate", "red velvet", "carrot"],
    "cookies": ["chocolate chip", "sugar", "oatmeal", "mint"]
}

HOURS = {
    "Monday":    "8:00 AM - 6:00 PM",
    "Tuesday":   "8:00 AM - 6:00 PM",
    "Wednesday": "8:00 AM - 6:00 PM",
    "Thursday":  "8:00 AM - 6:00 PM",
    "Friday":    "8:00 AM - 8:00 PM",
    "Saturday":  "9:00 AM - 5:00 PM",
    "Sunday":    "Closed",
}

CONTACT_PHONE = "123-456-7890"
CONTACT_EMAIL = "sweetcrust@bakery.com"
LOCATION = "123 Baker Street, Suite 1, Aurora, CO 80012"
MAPS_LINK = "https://maps.google.com/?q=123+Baker+Street+Aurora+CO"

def detect_intent(text):
    t = text.lower()
    if any(w in t for w in ["menu", "what do you have", "what do you sell", "what can i order", "options"]):
        return "menu"
    if any(w in t for w in ["hour", "open", "close", "schedule"]):
        return "hours"
    if any(w in t for w in ["agent", "human", "person", "staff", "contact", "call", "email", "speak to", "talk to", "reach"]):
        return "contact"
    if any(w in t for w in ["located", "location", "address", "where", "find you", "directions", "map"]):
        return "location"
    if any(w in t for w in ["change", "update", "switch", "different", "instead", "modify", "wrong", "actually"]):
        return "change"
    if any(w in t for w in ["hi", "hello", "hey", "good morning", "good afternoon"]):
        return "greeting"
    return "order"

def handle_intent(intent):
    if intent == "menu":
        lines = "\n".join(f"- **{k.title()}:** {', '.join(v)}" for k, v in MENU.items())
        return f"Here's our menu:\n\n{lines}\n\nWhat would you like to order? 😊"
    if intent == "hours":
        lines = "\n".join(f"- **{day}:** {hrs}" for day, hrs in HOURS.items())
        return f"Our opening hours are:\n\n{lines}\n\nIs there anything else I can help you with?"
    if intent == "contact":
        return (
            f"To speak with a team member, please reach out to us:\n\n"
            f"- Phone: {CONTACT_PHONE}\n"
            f"- Email: {CONTACT_EMAIL}\n\n"
            f"We're happy to help! Is there anything else I can assist you with?"
        )
    if intent == "location":
        return "We are located at 123 Baker Street!"
    if intent == "greeting":
        return "Hi there! Welcome to Sweet Crust Bakery 🎂 I can help you place an order, check our menu, or answer any questions. What can I do for you?"
    return None

def extract_order(text):
    text_lower = text.lower()
    items = ["cupcakes", "cupcake", "brownies", "brownie", "cakes", "cake", "cookies", "cookie"]
    flavors = ["vanilla", "chocolate", "strawberry", "red velvet", "carrot", "sugar", "oatmeal", "chocolate chip"]
    dates = ["today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    item = next((x for x in items if x in text_lower), None)
    flavor = next((x for x in flavors if x in text_lower), None)
    pickup_date = next((x for x in dates if x in text_lower), None)

    quantity = None
    if "half a dozen" in text_lower or "half dozen" in text_lower:
        quantity = "6"
    elif "two dozen" in text_lower:
        quantity = "24"
    elif "dozen" in text_lower:
        quantity = "12"
    else:
        match = re.search(r"\b\d+\b", text_lower)
        if match:
            quantity = match.group()

    time_match = re.search(r"\b\d{1,2}(:\d{2})?\s?(am|pm)\b", text_lower)
    pickup_time = time_match.group() if time_match else None

    return {"item": item, "flavor": flavor, "quantity": quantity, "pickup_date": pickup_date, "pickup_time": pickup_time}

def merge_order(existing, new_extract, overwrite=False):
    merged = existing.copy()
    for key in ["item", "flavor", "quantity", "pickup_date", "pickup_time"]:
        if new_extract.get(key):
            if overwrite or not merged.get(key):
                merged[key] = new_extract[key]
    return merged

def get_missing(order):
    missing = []
    if not order.get("item"):        missing.append("item (e.g. cupcakes, cookies)")
    if not order.get("flavor"):      missing.append("flavor (e.g. chocolate, vanilla)")
    if not order.get("quantity"):    missing.append("quantity (e.g. 12, half a dozen)")
    if not order.get("pickup_date"): missing.append("pickup day (e.g. tomorrow, friday)")
    if not order.get("pickup_time"): missing.append("pickup time (e.g. 2 pm)")
    return missing

def generate_order_response(order):
    missing = get_missing(order)
    if missing:
        if len(missing) == 1:
            return f"Almost there! I just need one more thing: **{missing[0]}**."
        return "Got it! I still need a few more details:\n\n" + "\n".join(f"- {m}" for m in missing)

    suggestion = ""
    item = order.get("item", "")
    if item in ["cupcake", "cupcakes"]:
        suggestion = "\n\n> Our chocolate cupcakes are a customer favorite!"
    elif item in ["brownie", "brownies"]:
        suggestion = "\n\n> Brownies pair great with our chocolate chip cookies."
    elif item in ["cake", "cakes"]:
        suggestion = "\n\n> For cakes, we recommend ordering at least 24 hours ahead."

    return (
        f"Here's your order summary:\n\n"
        f"- **Item:** {order['flavor']} {order['item']}\n"
        f"- **Quantity:** {order['quantity']}\n"
        f"- **Pickup:** {order['pickup_date']} at {order['pickup_time']}\n\n"
        f"Type **yes** to confirm, or let me know if anything needs changing.{suggestion}"
    )

def confirm_order():
    return "Your order has been confirmed! Thank you for choosing Sweet Crust Bakery! 🎂"

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🎂 Sweet Crust Bakery")
st.caption("Place an order, check our menu, or ask us anything!")

with st.expander("📋 View our menu"):
    for category, flavors in MENU.items():
        st.markdown(f"**{category.title()}:** {', '.join(flavors)}")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_order" not in st.session_state:
    st.session_state.current_order = {}
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
if "in_order_flow" not in st.session_state:
    st.session_state.in_order_flow = False

user_input = st.chat_input("How can we help you today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    if st.session_state.confirmed:
        st.session_state.current_order = {}
        st.session_state.confirmed = False
        st.session_state.in_order_flow = False

    confirm_words = ["yes", "confirm", "yes please", "that's correct", "correct", "yep", "yeah", "sure"]
    if user_input.strip().lower() in confirm_words:
        if st.session_state.in_order_flow:
            missing = get_missing(st.session_state.current_order)
            if missing:
                response = "I can't confirm just yet — I still need:\n\n" + "\n".join(f"- {m}" for m in missing)
            else:
                response = confirm_order()
                st.session_state.confirmed = True
                st.session_state.in_order_flow = False
        else:
            response = "It looks like you haven't started an order yet! What would you like to order? 😊"
    else:
        intent = detect_intent(user_input)

        # Handle change request mid-order
        if intent == "change" and st.session_state.in_order_flow:
            new_data = extract_order(user_input)
            has_new_info = any(v for v in new_data.values())
            if has_new_info:
                st.session_state.current_order = merge_order(st.session_state.current_order, new_data, overwrite=True)
                response = "Got it, I've updated your order!\n\n" + generate_order_response(st.session_state.current_order)
            else:
                fields = ["item (e.g. cakes)", "flavor (e.g. vanilla)", "quantity (e.g. 6)", "pickup day (e.g. monday)", "pickup time (e.g. 3 pm)"]
                response = "Sure! What would you like to change?\n\n" + "\n".join(f"- {f}" for f in fields)

        else:
            faq_response = handle_intent(intent)

            if faq_response and not st.session_state.in_order_flow:
                response = faq_response
            elif faq_response and st.session_state.in_order_flow and intent not in ["order", "change"]:
                missing = get_missing(st.session_state.current_order)
                nudge = (f"\n\n---\nBy the way, I'm still working on your order! I still need: "
                         f"{', '.join(missing)}.") if missing else ""
                response = faq_response + nudge
            else:
                st.session_state.in_order_flow = True
                new_data = extract_order(user_input)
                st.session_state.current_order = merge_order(st.session_state.current_order, new_data)
                response = generate_order_response(st.session_state.current_order)

    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.current_order and not st.session_state.confirmed:
    with st.sidebar:
        st.subheader("🧾 Current Order")
        fields = {
            "Item": st.session_state.current_order.get("item"),
            "Flavor": st.session_state.current_order.get("flavor"),
            "Quantity": st.session_state.current_order.get("quantity"),
            "Pickup Date": st.session_state.current_order.get("pickup_date"),
            "Pickup Time": st.session_state.current_order.get("pickup_time"),
        }
        for label, val in fields.items():
            if val:
                st.markdown(f"✅ **{label}:** {val}")
            else:
                st.markdown(f"⬜ **{label}:** *needed*")
        missing = get_missing(st.session_state.current_order)
        st.caption(f"{5 - len(missing)}/5 fields collected")
        if not missing:
            st.success("Ready! Type 'yes' to confirm.")

st.divider()
st.subheader("🧪 Evaluation — test case results")
st.caption("Shows how the order extractor handles different inputs.")

test_cases = [
    "I want 12 chocolate cupcakes tomorrow at 2 pm",
    "Give me half a dozen vanilla cookies friday at 10 am",
    "I need brownies for saturday at 1 pm",
    "I want a dozen red velvet cakes tomorrow at 3 pm",
]

for case in test_cases:
    result = extract_order(case)
    missing = get_missing(result)
    label = "Complete" if not missing else f"Missing: {', '.join(missing)}"
    with st.expander(f"{label} -- \"{case}\""):
        st.json(result)
