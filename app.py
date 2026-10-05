import streamlit as st
import requests
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

import base64

image_path = "assets/travel_banner.jpg.jpeg"

with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

from google import genai
import os

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------- BACKGROUND IMAGE ----------------

st.markdown(
    """
    <style>

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* Trip message input text */
.stChatInput textarea {
    color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000 !important;
}

/* Placeholder text */
.stChatInput textarea::placeholder {
    color: #555555 !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)

def get_ai_travel_response(user_message, trip_info=None):

    trip_info = trip_info or {}

    prompt = f"""
You are AI Travel Companion, a friendly and intelligent travel planning assistant.

User's current travel message:
{user_message}

Travel information already understood:
{trip_info}

Your job:
1. Understand what the user wants.
2. Give a helpful and personalized travel response.
3. If destination, number of days, budget, or travelers are known, use them.
4. Consider special needs such as children, senior citizens, wheelchair accessibility, or pets.
5. Suggest practical places, activities, food, transport, and travel tips when relevant.
6. If important information is missing, ask the user naturally for it.
7. Keep the response clear and easy to read.
8. Do not invent exact hotel availability or booking confirmations.
9. Be friendly and concise.

Respond as the user's AI Travel Companion.
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Travel Companion",
    page_icon="✈️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("---")

    st.markdown("### 🧭 Navigation")

# ==================================================
# HOTEL & ROOM BOOKING
# ==================================================

def get_hotel_recommendations(destination, budget, travelers, needs):

    hotel_data = {
        "ooty": [
            {
                "name": "Sterling Ooty Elk Hill",
                "location": "Ooty",
                "price": 4500,
                "room": "Deluxe Room",
                "rating": 4.3,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Gem Park Ooty",
                "location": "Ooty",
                "price": 5200,
                "room": "Deluxe Room",
                "rating": 4.2,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Fortune Resort Sullivan Court",
                "location": "Ooty",
                "price": 4800,
                "room": "Standard Room",
                "rating": 4.4,
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "madurai": [
            {
                "name": "Heritage Madurai",
                "location": "Madurai",
                "price": 6500,
                "room": "Garden Villa",
                "rating": 4.5,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Courtyard by Marriott Madurai",
                "location": "Madurai",
                "price": 5500,
                "room": "Deluxe Room",
                "rating": 4.4,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Hotel Temple View",
                "location": "Madurai",
                "price": 2800,
                "room": "Deluxe Room",
                "rating": 4.1,
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "kodaikanal": [
            {
                "name": "Sterling Kodai Lake",
                "location": "Kodaikanal",
                "price": 5000,
                "room": "Classic Room",
                "rating": 4.3,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "The Carlton",
                "location": "Kodaikanal",
                "price": 7500,
                "room": "Deluxe Room",
                "rating": 4.5,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Kodai Resort Hotel",
                "location": "Kodaikanal",
                "price": 4200,
                "room": "Garden Room",
                "rating": 4.2,
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "chennai": [
            {
                "name": "Taj Club House",
                "location": "Chennai",
                "price": 6000,
                "room": "Deluxe Room",
                "rating": 4.4,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "The Residency Towers",
                "location": "Chennai",
                "price": 5500,
                "room": "Executive Room",
                "rating": 4.3,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Holiday Inn Chennai OMR",
                "location": "Chennai",
                "price": 4500,
                "room": "Standard Room",
                "rating": 4.2,
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "coimbatore": [
            {
                "name": "Vivanta Coimbatore",
                "location": "Coimbatore",
                "price": 5200,
                "room": "Deluxe Room",
                "rating": 4.4,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Radisson Blu Coimbatore",
                "location": "Coimbatore",
                "price": 5800,
                "room": "Superior Room",
                "rating": 4.5,
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Welcomhotel by ITC Hotels",
                "location": "Coimbatore",
                "price": 4800,
                "room": "Deluxe Room",
                "rating": 4.3,
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ]
    }

    destination_key = destination.lower().strip()

    hotels = hotel_data.get(destination_key, [])

    recommended = []

    try:
        total_budget = int(
            str(budget)
            .replace(",", "")
            .replace("₹", "")
        )
    except:
        total_budget = 30000

    hotel_budget = max(total_budget * 0.40, 3000)

    for hotel in hotels:
        if hotel["price"] <= hotel_budget:
            recommended.append(hotel)

    if not recommended:
        recommended = hotels.copy()

    # Wheelchair requirement
    if "♿ Wheelchair accessibility" in needs:
        accessible = [
            hotel for hotel in recommended
            if hotel["accessibility"]
        ]

        if accessible:
            recommended = accessible

    # Pet requirement
    if "🐕 Pet-friendly planning" in needs:
        pet_hotels = [
            hotel for hotel in recommended
            if hotel["pet"]
        ]

        if pet_hotels:
            recommended = pet_hotels

    # Family / children requirement
    if "👶 Kid-friendly planning" in needs:
        family_hotels = [
            hotel for hotel in recommended
            if hotel["family"]
        ]

        if family_hotels:
            recommended = family_hotels

    recommended.sort(
        key=lambda hotel: hotel["rating"],
        reverse=True
    )

    return recommended


def show_hotel_booking():

    st.markdown("## 🏨 Hotel & Room Booking")

    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination")

    if not destination:
        st.info("📍 Please enter your destination first in Plan My Trip.")
        return

    st.markdown(
        f"### 🏨 Find a hotel in **{destination.title()}**"
    )

    # ---------------- DATES ----------------

    col1, col2 = st.columns(2)

    with col1:
        checkin = st.date_input(
            "📅 Check-in",
            key="hotel_checkin"
        )

    with col2:
        checkout = st.date_input(
            "📅 Check-out",
            key="hotel_checkout"
        )

    # ---------------- ROOMS & GUESTS ----------------

    col1, col2 = st.columns(2)

    with col1:
        rooms = st.number_input(
            "🛏️ Rooms",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            key="hotel_rooms"
        )

    with col2:
        guests = st.number_input(
            "👥 Guests",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
            key="hotel_guests"
        )

    # ---------------- FIND HOTELS ----------------

    if st.button(
        "🔎 Find Recommended Hotels",
        use_container_width=True,
        key="find_recommended_hotels"
    ):

        st.session_state["show_hotels"] = True

    # ---------------- RECOMMENDED HOTELS ----------------

    if st.session_state.get("show_hotels", False):

        st.markdown("---")
        st.subheader("🏨 Recommended Hotels")

        trip_info = st.session_state.get("trip_info", {})

        budget = trip_info.get("budget", 30000)
        travelers = trip_info.get("travelers", 2)
        needs = trip_info.get("special_needs", [])

        hotels = get_hotel_recommendations(
            destination,
            budget,
            travelers,
            needs
        )

        for hotel in hotels:

            st.markdown(
                f"""
                ### 🏨 {hotel["name"]}

                🛏️ **Room:** {hotel["room"]}

                ⭐ **Rating:** {hotel["rating"]}

                💰 **₹{hotel["price"]} / night**
                """
            )

            st.markdown("---")

        # ---------------- SELECT HOTEL ----------------

        hotel_names = [
            hotel["name"]
            for hotel in hotels
        ]

        selected_hotel = st.selectbox(
            "🏨 Select Hotel",
            hotel_names,
            key="selected_hotel"
        )

        st.markdown("---")

        # ---------------- GUEST DETAILS ----------------

        st.subheader("👤 Guest Details")

        guest_name = st.text_input(
            "Guest Name",
            key="booking_guest_name"
        )


        guest_phone = st.text_input(
            "Phone Number",
            key="booking_guest_phone"
        )

        # ---------------- CONFIRM ----------------

        if st.button(
            "✅ Confirm Hotel Booking",
            use_container_width=True,
            key="confirm_booking"
        ):

            guest_name_clean = (guest_name or "").strip()
            guest_phone_clean = (guest_phone or "").strip()

            if not guest_name_clean:

                st.error(
                    "❌ Please enter your full name."
                )

            elif not guest_phone_clean:

                st.error(
                    "❌ Please enter your phone number."
                )

            else:

                booking_id = (
                    "HTL-"
                    + destination.upper().replace(" ", "")
                    + "-001"
                )

                st.session_state["hotel_booking"] = {
                    "booking_id": booking_id,
                    "hotel": selected_hotel,
                    "guest": guest_name_clean,
                    "phone": guest_phone_clean,
                    "checkin": str(checkin),
                    "checkout": str(checkout),
                    "rooms": rooms,
                    "guests": guests
                }

                st.success(
                    "🎉 Hotel booking confirmed successfully!"
                )

                booking = st.session_state["hotel_booking"]

                st.markdown(
                    f"""
                    ### 🎫 Booking Confirmation

                    **Booking ID:** `{booking["booking_id"]}`

                    **Hotel:** {booking["hotel"]}

                    **Guest:** {booking["guest"]}

                    **Phone:** {booking["phone"]}

                    **Check-in:** {booking["checkin"]}

                    **Check-out:** {booking["checkout"]}

                    **Rooms:** {booking["rooms"]}

                    **Guests:** {booking["guests"]}
                    """
                )

                st.info(
                    "ℹ️ This is a demo hotel booking for the AI Travel Companion project."
                )


# ---------------- SIDEBAR NAVIGATION ----------------

with st.sidebar:

    st.markdown("## ✈️ AI Travel Companion")
    st.caption("Your journey, your way.")

    st.markdown("---")
    st.markdown("### 🧭 Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state["page"] = "Home"
        st.rerun()

    if st.button("🗺️ Plan My Trip", use_container_width=True):
        st.session_state["page"] = "Plan"
        st.rerun()

    if st.button("💰 Budget", use_container_width=True):
        st.session_state["page"] = "Budget"
        st.rerun()

    if st.button("🌦️ Weather", use_container_width=True):
        st.session_state["page"] = "Weather"
        st.rerun()

    if st.button("📍 Nearby Places", use_container_width=True):
        st.session_state["page"] = "Nearby"
        st.rerun()

    if st.button("🧳 Packing", use_container_width=True):
        st.session_state["page"] = "Packing"
        st.rerun()

    if st.button("🚆 Transport", use_container_width=True):
        st.session_state["page"] = "Transport"
        st.rerun()

    if st.button("🗺️ Route Map", use_container_width=True):
        st.session_state["page"] = "Map"
        st.rerun()  

    if st.button("🎫 Ticket Booking", use_container_width=True):
        st.session_state["page"] = "Tickets"
        st.rerun()      

    if st.button("🏨 Hotel & Room Booking", use_container_width=True):
        st.session_state["page"] = "Hotel"
        st.rerun()

    st.markdown("---")
    st.caption("✨ AI Travel Companion")


# ==================================================
# SIDEBAR PAGE ROUTING
# ==================================================

current_page = st.session_state.get("page", "Home")

# ---------------- BUDGET PAGE ----------------

if current_page == "Budget":

    st.markdown("---")
    st.markdown("## 💰 Trip Budget Planner")

    st.info(
        "Calculate your estimated trip cost based on "
        "your budget, duration and number of travelers."
    )

    trip_info = st.session_state.get("trip_info", {})

    budget_text = trip_info.get("budget")
    days = trip_info.get("days") or 3
    travelers = trip_info.get("travelers") or 1

    if budget_text:

        budget = int(
            str(budget_text)
            .replace(",", "")
            .replace("₹", "")
        )

        transport = 4500
        hotel_per_day = 2000
        food_per_day = 1000
        activities_per_day = 700
        emergency = 1500

        hotel = hotel_per_day * days
        food = food_per_day * days * travelers
        activities = activities_per_day * days * travelers

        estimated_total = (
            transport
            + hotel
            + food
            + activities
            + emergency
        )

        st.write(f"🎯 **Your Budget:** ₹{budget:,}")
        st.write(f"👥 **Travelers:** {travelers}")
        st.write(f"📅 **Duration:** {days} days")

        st.markdown("---")

        st.write(f"🚗 Transport: ₹{transport:,}")
        st.write(f"🏨 Stay: ₹{hotel:,}")
        st.write(f"🍛 Food: ₹{food:,}")
        st.write(f"🎟️ Activities: ₹{activities:,}")
        st.write(f"🆘 Emergency buffer: ₹{emergency:,}")

        st.markdown("---")

        st.write(
            f"💰 **Estimated Total: ₹{estimated_total:,}**"
        )

        remaining = budget - estimated_total

        if remaining >= 0:
            st.success(
                f"✅ You are within budget by ₹{remaining:,}"
            )
        else:
            st.warning(
                f"⚠️ You are ₹{abs(remaining):,} over budget."
            )

    else:

        st.warning(
            "💬 Please enter your budget in Plan My Trip first."
        )



# ---------------- WEATHER PAGE ----------------

elif current_page == "Weather":

    st.markdown("---")
    st.markdown("## 🌦️ Destination Weather")

    trip_info = st.session_state.get("trip_info", {})
    destination = trip_info.get("destination")

    if destination:

        st.info(
            f"📍 Checking current weather for {destination}..."
        )

        # Get coordinates
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

        geocode_params = {
            "name": destination,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geocode_response = requests.get(
            geocode_url,
            params=geocode_params
        )

        if geocode_response.status_code == 200:

            geocode_data = geocode_response.json()

            if geocode_data.get("results"):

                latitude = geocode_data["results"][0]["latitude"]
                longitude = geocode_data["results"][0]["longitude"]

                # Get weather
                weather_url = "https://api.open-meteo.com/v1/forecast"

                weather_params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,weather_code",
                    "timezone": "Asia/Kolkata"
                }

                weather_response = requests.get(
                    weather_url,
                    params=weather_params
                )

                if weather_response.status_code == 200:

                    weather_data = weather_response.json()

                    temperature = weather_data["current"]["temperature_2m"]

                    st.success(
                        f"🌡️ Current temperature in {destination}: {temperature}°C"
                    )

                else:

                    st.warning(
                        "🌦️ Weather information is currently unavailable."
                    )

            else:

                st.warning(
                    "🌦️ Could not find this destination."
                )

        else:

            st.warning(
                "🌦️ Could not connect to the weather service."
            )

    else:

        st.warning(
            "💬 Please enter your destination in Plan My Trip first."
        )


# ---------------- NEARBY PLACES PAGE ----------------

elif current_page == "Nearby":

    st.markdown("---")
    st.markdown("## 📍 Nearby Places Explorer")

    trip_info = st.session_state.get("trip_info", {})
    destination = trip_info.get("destination")

    if destination:

        st.info(
            f"📍 Exploring places around {destination}..."
        )

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": destination,
            "format": "json",
            "limit": 5
        }

        headers = {
            "User-Agent": "AI-Travel-Companion"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        if response.status_code == 200:

            places = response.json()

            if places:

                for place in places:

                    st.markdown(
                        f"### 📍 {place.get('display_name', 'Unknown place')}"
                    )

            else:

                st.warning(
                    "😕 No nearby places found."
                )

        else:

            st.warning(
                "📍 Nearby places information is currently unavailable."
            )

    else:

        st.warning(
            "💬 Please enter your destination in Plan My Trip first."
        )


# ---------------- PACKING PAGE ----------------

elif current_page == "Packing":

    st.markdown("---")
    st.markdown("## 🧳 Smart Packing Assistant")

    trip_info = st.session_state.get("trip_info", {})

    destination = (
        trip_info.get("destination")
        or "your destination"
    )

    days = trip_info.get("days") or 3
    needs = trip_info.get("needs", [])

    st.info(
        f"📍 Destination: {destination} | 📅 {days} days"
    )

    st.markdown("### 👕 Essentials")

    st.write("✓ 👕 Clothes")
    st.write(f"✓ 👕 Approximately {days + 1} sets of clothes")
    st.write("✓ 👟 Comfortable walking shoes")
    st.write("✓ 🧴 Personal toiletries")
    st.write("✓ 🔋 Phone charger & power bank")
    st.write("✓ 📄 ID and travel documents")

    if destination.lower() in ["ooty", "kodaikanal"]:

        st.markdown("### 🏔️ Hill Station Essentials")

        st.write("✓ 🧥 Warm jacket or sweater")
        st.write("✓ 🧣 Light shawl / scarf")
        st.write("✓ ☔ Umbrella or raincoat")
        st.write("✓ 🧦 Extra socks")

    if "👶 Kid-friendly planning" in needs:

        st.markdown("### 👶 Child Essentials")

        st.write("✓ 🧸 Child comfort items")
        st.write("✓ 👕 Extra clothes")
        st.write("✓ 🥤 Water bottle")
        st.write("✓ 🍪 Snacks")

    if "♿ Wheelchair accessibility" in needs:

        st.markdown("### ♿ Accessibility Essentials")

        st.write("✓ ♿ Mobility equipment")
        st.write("✓ 💊 Required medicines")
        st.write("✓ 🔋 Mobility-device charger if applicable")

    if "👵 Senior-friendly planning" in needs:

        st.markdown("### 👵 Senior Essentials")

        st.write("✓ 💊 Regular medicines")
        st.write("✓ 🪑 Comfortable support items")
        st.write("✓ 📄 Important medical information")

    if "🐕 Pet-friendly planning" in needs:

        st.markdown("### 🐕 Pet Essentials")

        st.write("✓ 🥣 Pet food & water")
        st.write("✓ 🦮 Leash")
        st.write("✓ 🧻 Cleaning supplies")

    st.success("✅ Packing checklist created!")


# ---------------- TRANSPORT PAGE ----------------

elif current_page == "Transport":

    st.markdown("---")
    st.markdown("## 🚆 Transport Planner")

    trip_info = st.session_state.get("trip_info", {})

    destination = (
        trip_info.get("destination")
        or "your destination"
    )

    travelers = trip_info.get("travelers") or 1
    needs = trip_info.get("needs", [])

    st.info(
        f"📍 Destination: {destination} | "
        f"👥 Travelers: {travelers}"
    )

    st.markdown("### 🚆 Travel Options")

    st.write(
        "🚆 **Train** — Comfortable option for longer journeys."
    )

    st.write(
        "🚌 **Bus** — Budget-friendly travel option."
    )

    st.write(
        "🚗 **Cab / Taxi** — Flexible door-to-door travel."
    )

    if "♿ Wheelchair accessibility" in needs:

        st.markdown("### ♿ Accessibility")

        st.warning(
            "⚠️ Confirm wheelchair space and boarding assistance before booking."
        )

    if "👶 Kid-friendly planning" in needs:

        st.info(
            "👶 Prefer comfortable seating and family-friendly travel times."
        )

    if "👵 Senior-friendly planning" in needs:

        st.info(
            "👵 Prefer comfortable transport with fewer transfers."
        )

    if "🐕 Pet-friendly planning" in needs:

        st.warning(
            "🐕 Confirm pet travel rules before booking."
        )

# ---------------- ROUTE MAP PAGE ----------------

elif current_page == "Map":

    st.markdown("---")
    st.markdown("## 🗺️ Route Map")

    trip_info = st.session_state.get("trip_info", {})

    origin = trip_info.get("origin") or trip_info.get("from")
    destination = trip_info.get("destination")

    if origin and destination:

        st.info(
            f"🚗 Route: {origin} → {destination}"
        )

        # -------- GET ORIGIN COORDINATES --------

        origin_url = "https://geocoding-api.open-meteo.com/v1/search"

        origin_params = {
            "name": origin,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        origin_response = requests.get(
            origin_url,
            params=origin_params
        )

        # -------- GET DESTINATION COORDINATES --------

        destination_params = {
            "name": destination,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        destination_response = requests.get(
            origin_url,
            params=destination_params
        )

        if (
            origin_response.status_code == 200
            and destination_response.status_code == 200
        ):

            origin_data = origin_response.json()
            destination_data = destination_response.json()

            if (
                origin_data.get("results")
                and destination_data.get("results")
            ):

                start_lat = origin_data["results"][0]["latitude"]
                start_lon = origin_data["results"][0]["longitude"]

                end_lat = destination_data["results"][0]["latitude"]
                end_lon = destination_data["results"][0]["longitude"]

                # -------- ROAD ROUTE --------

                route_url = (
                    f"https://router.project-osrm.org/route/v1/driving/"
                    f"{start_lon},{start_lat};{end_lon},{end_lat}"
                )

                route_params = {
                    "overview": "full",
                    "geometries": "geojson"
                }

                route_response = requests.get(
                    route_url,
                    params=route_params
                )

                if route_response.status_code == 200:

                    route_data = route_response.json()

                    if route_data.get("routes"):

                        route = route_data["routes"][0]

                        distance_km = route["distance"] / 1000
                        duration_hours = route["duration"] / 3600

                        st.success(
                            f"📍 {origin} → {destination}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "📏 Distance",
                                f"{distance_km:.1f} km"
                            )

                        with col2:
                            st.metric(
                                "⏱️ Travel Time",
                                f"{duration_hours:.1f} hours"
                            )

                        # -------- ROUTE MAP --------

                        coordinates = route["geometry"]["coordinates"]

                        map_points = []

                        for lon, lat in coordinates:
                            map_points.append(
                                {
                                    "lat": lat,
                                    "lon": lon
                                }
                            )

                        st.map(
                            map_points,
                            latitude="lat",
                            longitude="lon",
                            zoom=6
                        )

                        st.caption(
                            "🚗 Driving route shown between your starting point and destination."
                        )

                    else:

                        st.warning(
                            "🚗 Could not find a driving route."
                        )

                else:

                    st.warning(
                        "🗺️ Route service is currently unavailable."
                    )

            else:

                st.warning(
                    "📍 Could not find the origin or destination."
                )

        else:

            st.warning(
                "🌐 Could not connect to the map service."
            )

    else:

        st.warning(
            "💬 Please enter your starting location and destination in Plan My Trip first."
        )

# ---------------- TICKET BOOKING PAGE ----------------

elif current_page == "Tickets":

    st.markdown("---")
    st.markdown("## 🎫 Ticket Booking")

    trip_info = st.session_state.get("trip_info", {})

    origin = trip_info.get("origin")
    destination = trip_info.get("destination")
    travelers = trip_info.get("travelers", 1)

    if origin and destination:

        st.info(
            f"✈️ {origin} → {destination} | 👥 {travelers} Traveler(s)"
        )

        st.markdown("### 🚆 Choose Your Travel Option")

        option = st.selectbox(
            "Select transport",
            [
                "✈️ Flight",
                "🚆 Train",
                "🚌 Bus"
            ]
        )

        travel_date = st.date_input(
            "📅 Travel Date"
        )

        st.markdown("---")

        if option == "✈️ Flight":

            st.markdown("### ✈️ Flight Booking")

            st.success(
                f"Search flights from {origin} to {destination}"
            )

            st.link_button(
                "🔎 Search Flights",
                "https://www.google.com/travel/flights"
            )

        elif option == "🚆 Train":

            st.markdown("### 🚆 Train Booking")

            st.success(
                f"Search trains from {origin} to {destination}"
            )

            st.link_button(
                "🎫 Book Train Ticket",
                "https://www.irctc.co.in/"
            )

        else:

            st.markdown("### 🚌 Bus Booking")

            st.success(
                f"Search buses from {origin} to {destination}"
            )

            st.link_button(
                "🚌 Search Bus Tickets",
                "https://www.redbus.in/"
            )

        st.markdown("---")

        st.caption(
            "ℹ️ Booking will be completed through the official travel provider."
        )

    else:

        st.warning(
            "💬 Please enter your starting point and destination in Plan My Trip first."
        )

# ---------------- HOTEL PAGE ----------------

elif current_page == "Hotel":

    st.markdown("---")

    show_hotel_booking()






# ---------------- DEFAULT PAGE ----------------

if "page" not in st.session_state:
    st.session_state["page"] = "Home"
    
def understand_trip(message):

    if not message:
        return None

    message_lower = message.lower()

    result = {
        "origin": None,
        "destination": None,
        "days": None,
        "budget": None,
        "needs": [],
        "interests": [],
        "travelers": 1
    }

    # Detect starting point
    origin_match = re.search(
        r"\bfrom\s+([a-z]+)\s+to\b",
        message_lower
    )

    if origin_match:
        result["origin"] = origin_match.group(1).title()

    # Detect special needs
    if "wheelchair" in message_lower:
        result["needs"].append("♿ Wheelchair accessibility")

    if "child" in message_lower or "kid" in message_lower:
        result["needs"].append("👶 Kid-friendly planning")

    if (
        "senior" in message_lower
        or "elderly" in message_lower
        or "mother" in message_lower
        or "father" in message_lower
        or "grandmother" in message_lower
        or "grandfather" in message_lower
    ):
        result["needs"].append("👵 Senior-friendly planning")

    if "pet" in message_lower or "dog" in message_lower:
        result["needs"].append("🐕 Pet-friendly planning")

    # Detect food preference
    if "vegetarian" in message_lower or "veg" in message_lower:
        result["food_preference"] = "🥗 Vegetarian"
    elif "non-vegetarian" in message_lower or "non veg" in message_lower:
        result["food_preference"] = "🍗 Non-Vegetarian"
    else:
        result["food_preference"] = None

    # Detect interests
    if "nature" in message_lower:
        result["interests"].append("🌿 Nature")

    if "temple" in message_lower or "temples" in message_lower:
        result["interests"].append("🛕 Temples")

    if "food" in message_lower:
        result["interests"].append("🍛 Local Food")

    if "shopping" in message_lower:
        result["interests"].append("🛍️ Shopping")

    if "beach" in message_lower:
        result["interests"].append("🏖️ Beach")

    if "history" in message_lower or "historical" in message_lower:
        result["interests"].append("🏛️ History")

    # Detect days
    day_match = re.search(
        r"(\d+)\s*(day|days)",
        message_lower
    )

    if day_match:
        result["days"] = int(day_match.group(1))

    # Detect budget
    budget_match = re.search(
        r"(₹|rs\.?|inr)\s*([0-9,]+)",
        message_lower
    )

    if budget_match:
        result["budget"] = budget_match.group(2)

    # Detect destination
    known_places = [
        "ooty",
        "kodaikanal",
        "madurai",
        "chennai",
        "coimbatore",
        "bangalore",
        "kerala",
        "goa"
    ]

    for place in known_places:
        if place in message_lower:
            result["destination"] = place.title()

    # Detect travelers
    traveler_count = 1

    if "husband" in message_lower or "wife" in message_lower:
        traveler_count += 1

    child_match = re.search(
        r"(\d+)\s*(child|children|kid|kids)",
        message_lower
    )

    if child_match:
        traveler_count += int(child_match.group(1))
    elif "child" in message_lower or "kid" in message_lower:
        traveler_count += 1

    if "father" in message_lower or "mother" in message_lower:
        traveler_count += 1

    # Explicit number of people
    people_match = re.search(
        r"(\d+)\s*(people|persons|travelers|travellers)",
        message_lower
    )

    if people_match:
        traveler_count = int(people_match.group(1))

    result["travelers"] = traveler_count

    return result

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>

/* Travel Background Decorations */

.stApp::before {
    content: "✈️   🌍   🧳   🗺️   🏔️";
    position: fixed;
    top: 90px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 32px;
    letter-spacing: 28px;
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
}

/* Premium Typography */

.hero-title {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin-top: 10px;
}

.hero-subtitle {
    font-family: "Segoe UI", sans-serif;
    font-size: 21px;
    font-weight: 500;
    letter-spacing: 0.3px;
    margin-top: 8px;
}

h1 {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-weight: 800;
}

h2, h3 {
    font-family: "Segoe UI", sans-serif;
    font-weight: 700;
}

/* Animated travel icons */

.travel-icons {
    font-size: 48px;
    margin-bottom: 12px;
}

.travel-icons span {
    display: inline-block;
    margin: 0 10px;
    animation: floatIcon 3s ease-in-out infinite;
}

.travel-icons span:nth-child(2) {
    animation-delay: 0.5s;
}

.travel-icons span:nth-child(3) {
    animation-delay: 1s;
}

@keyframes floatIcon {
    0%, 100% {
        transform: translateY(0px) rotate(0deg);
    }

    50% {
        transform: translateY(-10px) rotate(4deg);
    }
}

/* Chat bubble */
.bot-message {
    background: linear-gradient(135deg, #ffffff, #eef7ff);
    padding: 20px 24px;
    border-radius: 20px 20px 20px 5px;
    margin: 15px 0;
    color: #40365f;
    font-size: 16px;
    line-height: 1.6;
    box-shadow: 0 8px 25px rgba(70,70,100,0.10);
    border: 1px solid rgba(150,150,200,0.15);
}

/* Feature cards */
.feature-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(70,70,100,0.08);
    min-height: 145px;
}

.stTextArea textarea {
    border-radius: 18px;
    border: 2px solid #e5ddff;
    padding: 16px;
    font-size: 16px;
    background: white;
}

.stTextArea textarea:focus {
    border-color: #a78bfa;
    box-shadow: 0 0 12px rgba(167, 139, 250, 0.25);
}

.feature-icon {
    font-size: 38px;
}

.feature-title {
    font-size: 17px;
    font-weight: 700;
    color: #51436f;
    margin-top: 8px;
}

.feature-text {
    color: #777;
    font-size: 13px;
    margin-top: 5px;
}


/* Button */
.stButton > button {
    width: 100%;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #ff4f9a, #ff8a65);
    color: white;
    font-weight: 700;
    font-size: 16px;
    padding: 12px;
}

.stButton > button:hover {
    box-shadow: 0 8px 20px rgba(255, 80, 150, 0.25);
    transform: scale(1.02);
}

/* Input */
.stTextInput input {
    border-radius: 14px;
    border: 2px solid #eadff5;
}
/* Floating Travel Icons */

.stMarkdown h2 {
    animation: travelFloat 3s ease-in-out infinite;
    text-align: center;
}

@keyframes travelFloat {
    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-8px);
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Make all text clearly visible over the background image */
.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp div,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #FFFFFF !important;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.90) !important;
}

/* Input text */
.stTextInput input,
.stTextArea textarea {
    color: #111111 !important;
    background-color: rgba(255, 255, 255, 0.92) !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #444444 !important;
}

/* Buttons */
.stButton button {
    color: #FFFFFF !important;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9) !important;
}

/* Markdown and normal text */
.stMarkdown {
    color: #FFFFFF !important;
}

/* Divider / horizontal lines */
hr {
    border-color: rgba(255, 255, 255, 0.85) !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.9) !important;
}

/* Selectbox / number input / other controls */
.stSelectbox div,
.stNumberInput input {
    color: #111111 !important;
}
</style>
""", unsafe_allow_html=True)



def get_coordinates(destination):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": destination,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        if data.get("results"):

            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]

            return latitude, longitude

    return None, None

def get_weather(destination):

    latitude, longitude = get_coordinates(destination)

    if latitude is None:
        return "🌦️ Could not find weather for this destination."

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        temperature = data["current"]["temperature_2m"]

        return f"🌡️ Current temperature in {destination}: {temperature}°C"

    else:

        return "🌦️ Weather information is currently unavailable."



    def get_nearby_places(destination):
         url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": destination,
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "AI-Travel-Companion"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        return data

    return []

def get_nearby_places(destination):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": destination,
        "format": "json",
        "limit": 5
    }

    headers = {
        "User-Agent": "AI-Travel-Companion"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        return data

    return []


# ---------------- HOTEL / ROOM BOOKING DATA ----------------

def get_hotel_recommendations(destination, budget, travelers, needs):
    """
    Destination-based hotel recommendation engine.
    """

    # ---------------- DESTINATION BASED HOTELS ----------------

    hotel_data = {

        "ooty": [
            {
                "name": "Sterling Ooty Elk Hill",
                "location": "Ooty",
                "room": "Deluxe Room",
                "price": 4500,
                "rating": 4.3,
                "amenities": ["WiFi", "Parking", "Restaurant"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Gem Park Ooty",
                "location": "Ooty",
                "room": "Deluxe Room",
                "price": 5200,
                "rating": 4.2,
                "amenities": ["WiFi", "Restaurant", "Parking"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Fortune Resort Sullivan Court",
                "location": "Ooty",
                "room": "Standard Room",
                "price": 4800,
                "rating": 4.4,
                "amenities": ["WiFi", "Restaurant", "Garden"],
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "madurai": [
            {
                "name": "Heritage Madurai",
                "location": "Madurai",
                "room": "Garden Villa",
                "price": 6500,
                "rating": 4.5,
                "amenities": ["Pool", "Restaurant", "WiFi"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Courtyard by Marriott Madurai",
                "location": "Madurai",
                "room": "Deluxe Room",
                "price": 5500,
                "rating": 4.4,
                "amenities": ["Pool", "Gym", "Restaurant"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Hotel Temple View",
                "location": "Madurai",
                "room": "Deluxe Room",
                "price": 2800,
                "rating": 4.1,
                "amenities": ["WiFi", "Restaurant", "Parking"],
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "kodaikanal": [
            {
                "name": "Sterling Kodai Lake",
                "location": "Kodaikanal",
                "room": "Classic Room",
                "price": 5000,
                "rating": 4.3,
                "amenities": ["WiFi", "Restaurant", "Parking"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "The Carlton",
                "location": "Kodaikanal",
                "room": "Deluxe Room",
                "price": 7500,
                "rating": 4.5,
                "amenities": ["Lake View", "Restaurant", "WiFi"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Kodai Resort Hotel",
                "location": "Kodaikanal",
                "room": "Garden Room",
                "price": 4200,
                "rating": 4.2,
                "amenities": ["Garden", "Restaurant", "WiFi"],
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "chennai": [
            {
                "name": "Taj Club House",
                "location": "Chennai",
                "room": "Deluxe Room",
                "price": 6000,
                "rating": 4.4,
                "amenities": ["Pool", "Gym", "Restaurant"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "The Residency Towers",
                "location": "Chennai",
                "room": "Executive Room",
                "price": 5500,
                "rating": 4.3,
                "amenities": ["Pool", "WiFi", "Restaurant"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Holiday Inn Chennai OMR",
                "location": "Chennai",
                "room": "Standard Room",
                "price": 4500,
                "rating": 4.2,
                "amenities": ["Pool", "Parking", "WiFi"],
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ],

        "coimbatore": [
            {
                "name": "Vivanta Coimbatore",
                "location": "Coimbatore",
                "room": "Deluxe Room",
                "price": 5200,
                "rating": 4.4,
                "amenities": ["Pool", "Gym", "Restaurant"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Radisson Blu Coimbatore",
                "location": "Coimbatore",
                "room": "Superior Room",
                "price": 5800,
                "rating": 4.5,
                "amenities": ["Pool", "Gym", "WiFi"],
                "accessibility": True,
                "family": True,
                "pet": False
            },
            {
                "name": "Welcomhotel by ITC Hotels",
                "location": "Coimbatore",
                "room": "Deluxe Room",
                "price": 4800,
                "rating": 4.3,
                "amenities": ["Restaurant", "WiFi", "Parking"],
                "accessibility": True,
                "family": True,
                "pet": False
            }
        ]
    }

    destination_key = destination.lower().strip()

    hotels = hotel_data.get(
        destination_key,
        []
    )

    filtered_hotels = []

    # ---------------- BUDGET ----------------

    try:
        total_budget = int(
            str(budget).replace(",", "").replace("₹", "")
        )
    except:
        total_budget = 30000

    hotel_budget = max(
        total_budget * 0.40,
        3000
    )

    # ---------------- FILTER HOTELS ----------------

    for hotel in hotels:

        if hotel["price"] <= hotel_budget:
            filtered_hotels.append(hotel)

    # If budget filtering removes everything,
    # show destination hotels anyway.

    if not filtered_hotels:
        filtered_hotels = hotels.copy()

    # ---------------- SPECIAL NEEDS ----------------

    if "♿ Wheelchair accessibility" in needs:

        accessible_hotels = [
            hotel
            for hotel in filtered_hotels
            if hotel["accessibility"]
        ]

        if accessible_hotels:
            filtered_hotels = accessible_hotels

    if "🐕 Pet-friendly planning" in needs:

        pet_hotels = [
            hotel
            for hotel in filtered_hotels
            if hotel["pet"]
        ]

        if pet_hotels:
            filtered_hotels = pet_hotels

    if "👶 Kid-friendly planning" in needs:

        family_hotels = [
            hotel
            for hotel in filtered_hotels
            if hotel["family"]
        ]

        if family_hotels:
            filtered_hotels = family_hotels

    # ---------------- SORT BY RATING ----------------

    filtered_hotels.sort(
        key=lambda x: x["rating"],
        reverse=True
    )

    return filtered_hotels

    # Convert budget safely
    try:
        total_budget = int(str(budget).replace(",", ""))
    except:
        total_budget = 30000

    # Approximate hotel budget
    hotel_budget = max(total_budget * 0.40, 3000)

    for hotel in hotels:

        # Accessibility filtering
        if "♿ Wheelchair accessibility" in needs:
            if not hotel["accessibility"]:
                continue

        # Pet filtering
        if "🐕 Pet-friendly planning" in needs:
            if not hotel["pet"]:
                continue

        # Family filtering
        if "👶 Kid-friendly planning" in needs:
            if not hotel["family"]:
                continue

        filtered_hotels.append(hotel)

    # If filtering removes everything, show all hotels
    if not filtered_hotels:
        filtered_hotels = hotels

    # Sort by rating
    filtered_hotels.sort(
        key=lambda x: x["rating"],
        reverse=True
    )

    return filtered_hotels



    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination")

    if not destination:
        st.warning("📍 Please enter your destination first.")
        return

    days = trip_info.get("days") or 3
    travelers = trip_info.get("travelers") or 1
    budget = trip_info.get("budget") or "30000"
    needs = trip_info.get("needs", [])

    st.markdown("---")
    st.subheader("🏨 Hotel & Room Booking")

    st.markdown(
        """
        <div class="bot-message">
        🏨 <b>Find the right stay for your trip</b><br><br>
        I'll recommend hotels based on your destination,
        budget and travel needs.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- SEARCH DETAILS ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text_input(
            "📍 Destination",
            value=destination,
            disabled=True,
            key="hotel_destination"
        )

    with col2:
        check_in = st.date_input(
            "📅 Check-in",
            key="hotel_checkin"
        )

    with col3:
        check_out = st.date_input(
            "📅 Check-out",
            key="hotel_checkout"
        )

    col4, col5 = st.columns(2)

    with col4:
        room_count = st.number_input(
            "🛏️ Rooms",
            min_value=1,
            max_value=5,
            value=1,
            key="hotel_rooms"
        )

    with col5:
        guest_count = st.number_input(
            "👥 Guests",
            min_value=1,
            max_value=15,
            value=travelers,
            key="hotel_guests"
        )

    if check_out <= check_in:
        st.error("⚠️ Check-out date must be after check-in date.")
        return

    nights = (check_out - check_in).days

    st.info(
        f"📅 {nights} night(s)  |  "
        f"👥 {guest_count} guest(s)  |  "
        f"🛏️ {room_count} room(s)"
    )

    # ---------------- FIND HOTELS ----------------

    if st.button(
        "🔎 Find Recommended Hotels",
        key="find_hotels"
    ):

        hotels = get_hotel_recommendations(
            destination,
            budget,
            travelers,
            needs
        )

        st.session_state["hotel_results"] = hotels

    # ---------------- HOTEL RESULTS ----------------

    hotels = st.session_state.get("hotel_results", [])

    if hotels:

        st.markdown("### 🌟 Recommended Hotels")

        for index, hotel in enumerate(hotels):

            st.markdown("---")

            col1, col2 = st.columns([2, 1])

            with col1:

                st.markdown(
                    f"### 🏨 {hotel['name']}"
                )

                st.write(
                    f"📍 {hotel['location']}"
                )

                st.write(
                    f"⭐ {hotel['rating']} / 5"
                )

                st.write(
                    f"🛏️ {hotel['room']}"
                )

                st.write(
                    " • ".join(hotel["amenities"])
                )

                if hotel["accessibility"]:
                    st.success("♿ Accessible-friendly option")

                if hotel["family"]:
                    st.info("👨‍👩‍👧 Family-friendly")

                if hotel["pet"]:
                    st.info("🐕 Pet-friendly")

            with col2:

                total_price = (
                    hotel["price"]
                    * nights
                    * room_count
                )

                st.metric(
                    "Price / night",
                    f"₹{hotel['price']:,}"
                )

                st.write(
                    f"💰 Total: ₹{total_price:,}"
                )

                if st.button(
                    "🛏️ Select Room",
                    key=f"select_hotel_{index}"
                ):

                    st.session_state["selected_hotel"] = hotel
                    st.session_state["selected_hotel_total"] = total_price

                    st.success(
                        f"✅ {hotel['name']} selected!"
                    )

    # ---------------- ROOM CONFIRMATION ----------------

    selected_hotel = st.session_state.get(
        "selected_hotel"
    )

    if selected_hotel:

        st.markdown("---")
        st.markdown("### 🛏️ Room Selection")

        st.success(
            f"🏨 Selected Hotel: {selected_hotel['name']}"
        )

        st.write(
            f"🛏️ Room: {selected_hotel['room']}"
        )

        st.write(
            f"📅 Stay: {nights} night(s)"
        )

        st.write(
            f"👥 Guests: {guest_count}"
        )

        st.write(
            f"💰 Total Room Cost: "
            f"₹{st.session_state['selected_hotel_total']:,}"
        )

        st.markdown("### 👤 Guest Information")

        guest_name = st.text_input(
            "Full Name",
            key="hotel_guest_name"
        )

        guest_email = st.text_input(
            "Email",
            key="hotel_guest_email"
        )



# ---------------- HERO ----------------

    st.markdown("")

    st.image(
        "travel_banner.jpeg",
        use_container_width=True
    )

    st.markdown("")
    

    st.markdown(
        """
        <div class="hero-subtitle">
            ✨ Dream the trip. I’ll solve the travel.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.caption(
        "Your journey. Your needs. Your way."
    )


# ---------------- WELCOME MESSAGE ----------------

st.markdown("""
<div class="bot-message">

🤖 <b>Hi Traveller! 👋</b>

<br><br>

You don't have to know exactly what you need.

Just tell me something like:

<br><br>

💬 <i>
"I'm planning a 3-day Ooty trip with my husband,
6-year-old child and wheelchair-using mother.
My budget is ₹30,000."
</i>

<br><br>

I'll help you figure out the travel needs step by step. ✨

</div>
""", unsafe_allow_html=True)


# ---------------- CHAT INPUT ----------------

if st.session_state["page"] == "Plan":

    st.markdown("## 🗺️ Plan My Trip")

    st.subheader("💬 Your Travel Conversation")

    user_message = st.chat_input(
        "💬 Tell me about your trip..."
    )

else:

    user_message = None

# ---------------- CHAT MEMORY ----------------

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if user_message and user_message.strip():

    # Save the new user message
    st.session_state["chat_history"].append(
        {
            "role": "user",
            "message": user_message
        }
    )

    # ---------------- GEMINI AI RESPONSE ----------------

previous_trip = st.session_state.get(
    "trip_info",
    {}
)

new_trip = understand_trip(user_message)

trip_info = previous_trip.copy()

if new_trip:
    for key, value in new_trip.items():

        if value not in [None, [], ""]:
            trip_info[key] = value

st.session_state["trip_info"] = trip_info


with st.spinner("🤖 AI Travel Companion is thinking..."):

    ai_response = get_ai_travel_response(
        user_message,
        trip_info
    )

st.success(
    "🌍 Your AI Travel Companion is ready!"
)

st.markdown("### 🤖 AI Travel Companion")

st.markdown(
    f"""
    <div class="bot-message">
        {ai_response}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 🧠 What I heard")

st.markdown(
        f"""
        <div class="user-message">
            👤 <b>You</b><br><br>
            {user_message}
        </div>
        """,
        unsafe_allow_html=True
    )




# ---------------- SHOW CHAT HISTORY ----------------

for chat in st.session_state["chat_history"]:

    if chat["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br><br>
                {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------- MISSING INFORMATION CHECK ----------------

trip_info = st.session_state.get("trip_info", {})

missing = []

if not trip_info.get("destination"):
    missing.append("📍 Destination")

if not trip_info.get("days"):
    missing.append("📅 Number of days")

if not trip_info.get("budget"):
    missing.append("💰 Budget")

if not trip_info.get("travelers"):
    missing.append("👥 Travelers")


if missing:

    st.warning("🤖 I need a little more information:")

    if "📍 Destination" in missing:
        st.write("📍 Where would you like to travel?")

    if "📅 Number of days" in missing:
        st.write("📅 How many days are you planning for the trip?")

    if "💰 Budget" in missing:
        st.write("💰 What is your approximate trip budget?")

    if "👥 Travelers" in missing:
        st.write("👥 Who will be travelling with you?")

else:

    st.success("✅ I have all the basic trip details!")

    # ---------------- TRIP DETAILS ----------------

    st.markdown("### 🧠 Trip Details")

    st.write(
        f"📍 **Destination:** {trip_info['destination']}"
    )

    st.write(
        f"📅 **Duration:** {trip_info['days']} days"
    )

    st.write(
        f"👥 **Travelers:** {trip_info.get('travelers', 1)}"
    )

    if trip_info.get("child_age"):
        st.write(
            f"👶 **Child Age:** {trip_info['child_age']} years"
        )

    st.write(
        f"💰 **Budget:** ₹{trip_info['budget']}"
    )

    if trip_info.get("food_preference"):
        st.write(
            f"🍛 **Food Preference:** "
            f"{trip_info['food_preference']}"
        )

    if trip_info.get("interests"):

        st.write("🎯 **Interests:**")

        for interest in trip_info["interests"]:
            st.write(f"✓ {interest}")

    # ---------------- TRAVEL NEEDS ----------------

    st.markdown("### 🧩 Travel Needs Detected")

    if trip_info.get("needs"):

        for need in trip_info["needs"]:
            st.success(f"✓ {need}")

    else:
        st.info(
            "No special travel needs detected yet."
        )


    # ---------------- ITINERARY ----------------

    st.markdown("---")

    st.subheader("🗺️ Your Travel Plan")

    if st.button(
        "🌟 Generate My Itinerary",
        key="generate_itinerary"
    ):

        destination = trip_info.get(
            "destination",
            "your destination"
        )

        days = trip_info.get(
            "days",
            3
        )

        travelers = trip_info.get(
            "travelers",
            1
        )

        needs = trip_info.get(
            "needs",
            []
        )

        food_preference = trip_info.get(
            "food_preference"
        )

        st.success(
            f"✨ Creating a personalized "
            f"{days}-day {destination} trip..."
        )

        # ---------------- WHY THIS ITINERARY ----------------

        st.markdown("### 💡 Why this itinerary?")

        if "👵 Senior-friendly planning" in needs:
            st.info(
                "👵 Your plan includes shorter walks, "
                "comfortable transport and regular rest breaks."
            )

        if "👶 Kid-friendly planning" in needs:
            st.info(
                "👶 Your plan includes kid-friendly activities, "
                "easier pacing and family-friendly breaks."
            )

        if "♿ Wheelchair accessibility" in needs:
            st.info(
                "♿ Your plan prioritizes accessible routes, "
                "step-free access and comfortable transport."
            )

        if "🐕 Pet-friendly planning" in needs:
            st.info(
                "🐕 Your plan considers pet-friendly stays, "
                "activities and transport."
            )

        # ---------------- STAY REQUIREMENTS ----------------

        st.markdown("### 🏨 Stay Requirements")

        if "♿ Wheelchair accessibility" in needs:
            st.info(
                "♿ Step-free entrance, lift access and "
                "accessible bathroom recommended."
            )

        if "👵 Senior-friendly planning" in needs:
            st.info(
                "👵 Prefer hotels with lifts, nearby parking "
                "and easy room access."
            )

        if "👶 Kid-friendly planning" in needs:
            st.info(
                "👶 Prefer family rooms and easy restroom access."
            )

        if "🐕 Pet-friendly planning" in needs:
            st.info(
                "🐕 Confirm that the property allows pets."
            )

        # ---------------- TRANSPORT REQUIREMENTS ----------------

        st.markdown("### 🚗 Transport Requirements")

        if "♿ Wheelchair accessibility" in needs:
            st.info(
                "♿ Prefer accessible vehicles with easy boarding space."
            )

        if "👵 Senior-friendly planning" in needs:
            st.info(
                "👵 Prefer comfortable transport with minimal walking."
            )

        if "👶 Kid-friendly planning" in needs:
            st.info(
                "👶 Prefer family-friendly transport with comfortable seating."
            )

        if "🐕 Pet-friendly planning" in needs:
            st.info(
                "🐕 Confirm that pets are allowed before travelling."
            )

        # ---------------- DAY-WISE ITINERARY ----------------

        for day in range(1, days + 1):

            st.markdown(
                f"### 📅 Day {day}"
            )

            if "♿ Wheelchair accessibility" in needs:

                st.write(
                    "🌅 Morning — Easy-paced sightseeing "
                    "with comfortable transport."
                )

            elif "👶 Kid-friendly planning" in needs:

                st.write(
                    "🌅 Morning — Kid-friendly sightseeing."
                )

            else:

                st.write(
                    "🌅 Morning — Explore a popular local attraction."
                )

            if food_preference == "🥗 Vegetarian":

                st.write(
                    "🥗 Lunch — Try a local vegetarian restaurant."
                )

            elif food_preference == "🍗 Non-Vegetarian":

                st.write(
                    "🍗 Lunch — Try a local non-vegetarian restaurant."
                )

            else:

                st.write(
                    "🍛 Lunch — Try local cuisine."
                )

            st.write(
                "🌿 Afternoon — Discover another nearby place."
            )

            st.write(
                "🌇 Evening — Enjoy a relaxed evening experience."
            )

        # ---------------- ACCESSIBILITY ----------------

        if "♿ Wheelchair accessibility" in needs:

            st.markdown(
                "### ♿ Accessibility Support"
            )

            st.info(
                "🚶 Prefer routes with less walking."
            )

            st.info(
                "🛗 Check for lifts, ramps and step-free entrances."
            )

            st.info(
                "🚻 Check accessible restroom availability."
            )

            st.info(
                "🚗 Prefer comfortable and accessible transport."
            )

            st.warning(
                "⚠️ Accessibility details should be confirmed "
                "with the hotel or attraction before travel."
            )


    
# ==================================================
# HOTEL & ROOM BOOKING
# ==================================================

if st.session_state.get("page") == "Plan":

    st.markdown("---")
    st.markdown("## 🏨 Hotel & Room Booking")

    st.info(
        "Find a suitable hotel and room based on your "
        "destination, budget and travel needs."
    )    

    show_hotel_booking()

# ---------------- WEATHER ----------------

st.markdown("---")

st.subheader("🌦️ Destination Weather")

if st.button("🌤️ Check Weather"):

    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination")

    if destination:

        weather = get_weather(destination)

        st.info(weather)

    else:

        st.warning(
            "💬 Please enter your destination first."
        )


# ---------------- NEARBY PLACES ----------------

st.markdown("---")

st.subheader("🗺️ Nearby Places Explorer")

if st.button("📍 Explore Nearby Places"):

    trip_info = st.session_state.get("trip_info", {})
    destination = trip_info.get("destination")

    if destination:

        places = get_nearby_places(destination)

        if places:
            for place in places:
                st.info(place.get("display_name", "Unknown place"))
                st.caption("📍 You’re already nearby — consider adding this to your trip.")
        else:
            st.warning("😕 No nearby places found.")

    else:
        st.warning("💬 Please enter your destination first.")

# ---------------- BUDGET PLANNER ----------------

st.markdown("---")

st.subheader("💰 Trip Budget Estimate")

if st.button("💳 Calculate My Budget"):

    trip_info = st.session_state.get("trip_info", {})

    budget_text = trip_info.get("budget")

    if budget_text:

        budget = int(budget_text.replace(",", ""))

        days = trip_info.get("days") or 3
        travelers = trip_info.get("travelers") or 1

        transport = 4500
        hotel_per_day = 2000
        food_per_day = 1000
        activities_per_day = 700

        hotel = hotel_per_day * days
        st.caption(
            f"🏨 Stay: ₹{hotel_per_day:,}/day × {days} days"
        )
        food = food_per_day * days * travelers
        st.caption(f"🍛 Food: ₹{food_per_day:,}/person/day × {travelers} travelers × {days} days")
        activities = activities_per_day * days * travelers
        st.caption(
            f"🎟️ Activities: ₹{activities_per_day:,}/person/day × "
            f"{travelers} travelers × {days} days"
        )
        emergency = 1500

        st.write(f"🎯 **Your Budget:** ₹{budget:,}")
        st.write(f"👥 **Travelers:** {travelers}")

        daily_budget = budget / days

        st.write(f"📅 **Daily Budget:** ₹{daily_budget:,.0f}")

        st.write(f"🚗 Transport: ₹{transport:,.0f}")
        st.write(f"🏨 Stay: ₹{hotel:,.0f}")
        st.write(f"🍛 Food: ₹{food:,.0f}")
        st.write(f"🎟️ Activities: ₹{activities:,.0f}")
        st.write(f"🆘 Emergency buffer: ₹{emergency:,.0f}")

        estimated_total = (
            transport
            + hotel
            + food
            + activities
            + emergency
        )

        remaining = budget - estimated_total

        if remaining > 0:

            st.success(
                f"✅ Estimated trip cost: ₹{estimated_total:,.0f}"
            )

            st.info(
                f"💚 Remaining budget: ₹{remaining:,.0f}"
            )

        elif remaining == 0:

            st.success(
                f"✅ Estimated trip cost: ₹{estimated_total:,.0f} — "
                "Exactly within your budget!"
            )

        else:

            st.error(
                f"⚠️ Estimated trip cost: ₹{estimated_total:,.0f}"
            )

            st.warning(
                f"🔴 You are ₹{abs(remaining):,.0f} over your budget."
            )
            st.markdown("### 🤖 AI Budget Optimizer")

            if travelers >= 4:
                st.info("💡 For a larger group, consider a family room and shared transport.")

            elif days >= 4:
                st.info("💡 Consider reducing the trip by one day to save on stay and food.")

            else:
                st.info("💡 Consider a lower-cost hotel or reducing paid activities.")

            st.write(
                "💡 Try reducing hotel cost or local transport "
                "to bring the trip back within budget."
            )

            st.info(
                f"🎯 Suggested saving target: ₹{abs(remaining):,.0f}"
            )    

    else:

        st.warning(
            "💬 Please include your budget in your travel message."
        )

# ---------------- DYNAMIC RE-PLANNER ----------------

st.markdown("---")
st.subheader("🔄 Dynamic Trip Re-planner")

delay_hours = st.number_input(
    "⏰ Are you delayed? (hours)",
    min_value=0,
    max_value=12,
    value=0,
    step=1
)

if st.button("🔄 Re-plan My Trip"):

    if delay_hours > 0:

        st.info(
            f"⏰ You are {delay_hours} hour(s) late."
        )

    st.markdown("### 🧠 AI Re-planning")

    if delay_hours >= 2:

        st.warning(
            "⚠️ Your schedule is significantly delayed."
        )

        st.write("✂️ Morning activity can be skipped or shortened.")
        st.write("📍 Choose a nearby attraction instead of a distant place.")
        st.write("🍛 Keep lunch/rest break as a priority.")
        st.write("🚗 Use comfortable local transport.")
        st.write("🌇 Keep only one relaxed evening activity.")

    else:

        st.info(
            "🔄 Small delay detected. I'll make minor timing adjustments."
        )

        st.write("⏰ Shorten the current activity.")
        st.write("📍 Prefer the next nearby attraction.")
        st.write("🍛 Keep the planned food break.")

    st.success(
        "✅ Itinerary adjusted based on your delay."
    )

    st.markdown("### 🧠 AI Re-planning")

    st.write("✂️ Remove or skip activities that no longer fit the schedule.")
    st.write("📍 Prioritize nearby attractions.")
    st.write("🍛 Keep a suitable food/rest break.")
    st.write("🚗 Prefer comfortable transportation.")

    st.success(
            "✅ Your itinerary can be adjusted to the new timing."
        )

else:

        st.info(
            "😊 No delay detected. Your original itinerary can continue."
        )
# ---------------- SMART PACKING ASSISTANT ----------------

st.markdown("---")
st.subheader("🧳 Smart Packing Assistant")

if st.button("🎒 Create My Packing List"):

    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination") or "your destination"
    days = trip_info.get("days") or 3
    needs = trip_info.get("needs", [])

    st.markdown("### 🎒 Your Personalized Packing List")

    st.write(f"📍 **Destination:** {destination}")
    st.write(f"📅 **Duration:** {days} days")

    st.markdown("#### 👕 Essentials")

    st.write("✓ 👕 Clothes")
    clothing_count = days + 1

    st.write(
        f"✓ 👕 Pack approximately {clothing_count} sets of clothes"
    )
    st.write("✓ 🩳 Comfortable travel clothes")
    st.write("✓ 👟 Comfortable walking shoes")
    if destination.lower() in ["ooty", "kodaikanal"]:

        st.markdown("#### 🏔️ Hill Station Essentials")

    st.write("✓ 🧥 Warm jacket or sweater")
    st.write("✓ 🧣 Light shawl / scarf")
    st.write("✓ ☔ Umbrella or raincoat")
    st.write("✓ 🧦 Extra socks")
    st.write("✓ 🧴 Personal toiletries")
    st.write("✓ 🔋 Phone charger & power bank")
    st.write("✓ 📄 ID and travel documents")

    if "👶 Kid-friendly planning" in needs:
        st.markdown("#### 👶 Child Essentials")
        st.write("✓ 🧸 Child comfort items")
        st.write("✓ 👕 Extra clothes")
        st.write("✓ 🥤 Water bottle")
        st.write("✓ 🍪 Snacks")

    if "♿ Wheelchair accessibility" in needs:
        st.markdown("#### ♿ Accessibility Essentials")
        st.write("✓ ♿ Mobility equipment")
        st.write("✓ 💊 Required medicines")
        st.write("✓ 🔋 Mobility-device charger if applicable")

    if "👵 Senior-friendly planning" in needs:
        st.markdown("#### 👵 Senior Essentials")
        st.write("✓ 💊 Regular medicines")
        st.write("✓ 🪑 Comfortable support items")
        st.write("✓ 📄 Medical information")

    if "🐕 Pet-friendly planning" in needs:
        st.markdown("#### 🐕 Pet Essentials")
        st.write("✓ 🥣 Pet food & water")
        st.write("✓ 🦮 Leash")
        st.write("✓ 🧻 Cleaning supplies")
        st.write("✓ 📄 Pet vaccination documents")

    st.success("✅ Packing checklist created based on your travel needs.")

# ---------------- TRANSPORT SEARCH ----------------

st.markdown("---")
st.subheader("🚆 Transport Planner")

if st.button("🚆 Find Travel Options"):

    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination") or "your destination"
    travelers = trip_info.get("travelers") or 1
    needs = trip_info.get("needs", [])

    st.markdown("### 🚆 Travel Options")

    st.info(
        f"📍 Destination: {destination}  |  "
        f"👥 Travelers: {travelers}"
    )

    st.write("🚆 **Train** — Comfortable option for longer journeys.")
    st.write("🚌 **Bus** — Budget-friendly travel option.")
    st.write("🚗 **Cab / Taxi** — Flexible door-to-door travel.")

    if "♿ Wheelchair accessibility" in needs:
        st.markdown("### ♿ Accessibility Check")
        st.warning(
            "⚠️ Confirm wheelchair space and boarding assistance "
            "before booking."
        )

    if "👶 Kid-friendly planning" in needs:
        st.info(
            "👶 Prefer comfortable seating and family-friendly travel times."
        )

    if "👵 Senior-friendly planning" in needs:
        st.info(
            "👵 Prefer comfortable transport with fewer transfers."
        )

    if "🐕 Pet-friendly planning" in needs:
        st.warning(
            "🐕 Confirm pet travel rules before booking."
        )    

# ---------------- FEATURES ----------------

st.markdown("---")

st.subheader("✨ Your Travel Companion")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📍</div>
        <div class="feature-title">Explore</div>
        <div class="feature-text">
            Discover places around you
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏨</div>
        <div class="feature-title">Stay</div>
        <div class="feature-text">
            Find suitable hotels
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎫</div>
        <div class="feature-title">Bookings</div>
        <div class="feature-text">
            Plan tickets and bookings
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌦️</div>
        <div class="feature-title">Weather</div>
        <div class="feature-text">
            Weather-aware planning
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("🤖 AI Travel Assistant")

if st.button("✨ Ask My Travel Companion"):

    trip_info = st.session_state.get("trip_info", {})

    destination = trip_info.get("destination") or "your destination"
    days = trip_info.get("days") or 3
    budget = trip_info.get("budget")
    needs = trip_info.get("needs", [])
    food_preference = trip_info.get("food_preference")

    st.success("🤖 I'm creating your personalized travel plan...")

    st.markdown("### ✨ Your Personalized Plan")

    st.write(
        f"🌍 **Destination:** {destination}"
    )

    st.write(
        f"📅 **Duration:** {days} days"
    )

    if budget:
        st.write(
            f"💰 **Budget:** ₹{budget}"
    )

    interests = trip_info.get("interests", [])
    
    if interests:
        st.write("🎯 **Interests:**")
        for interest in interests:
            st.write(f"✓ {interest}")
    
    if needs:
        st.write("🧩 **Travel needs:**")
        for need in needs:
            st.write(f"✓ {need}")

    if food_preference:
        st.write(
            f"🍛 **Food preference:** {food_preference}"
        )

    st.markdown("### 🗺️ AI Personalized Suggestions")

    trip_info = st.session_state.get("trip_info", {})

    days = trip_info.get("days") or 3
    needs = trip_info.get("needs", [])
    food_preference = trip_info.get("food_preference")
    interests = trip_info.get("interests", [])
    destination = trip_info.get("destination") or "your destination"

    for day in range(1, days + 1):

        st.markdown(f"#### 📅 Day {day}")

        if "🌿 Nature" in interests:
            st.write("🌿 Nature-focused activity — scenic viewpoints, gardens and peaceful nature spots.")
        if "🛕 Temples" in interests:
            st.write("🛕 Temple-focused activity — explore local temples and nearby cultural places.")
        if "🍛 Local Food" in interests:
            st.write("🍛 Food-focused activity — try local dishes and popular food spots.")
        if "♿ Wheelchair accessibility" in needs:
            st.write("♿ Easy-access sightseeing with minimal walking.")
        elif "👵 Senior-friendly planning" in needs:
            st.write("👵 Relaxed sightseeing with comfortable transport and rest breaks.")
        elif "👶 Kid-friendly planning" in needs:
            st.write("👶 Kid-friendly activity with a relaxed family schedule.")
        else:
            st.write("🌿 Explore a popular local attraction.")

    if food_preference == "🥗 Vegetarian":
        st.write("🥗 Lunch — Local vegetarian restaurant.")
    elif food_preference == "🍗 Non-Vegetarian":
        st.write("🍗 Lunch — Local non-vegetarian restaurant.")
    else:
        st.write("🍛 Lunch — Try a local restaurant.")

    if destination == "Ooty":

     if day == 1:
        st.write("🌿 Morning — Explore Ooty Lake and enjoy a relaxed boat ride.")
        st.write("🏞️ Afternoon — Visit the Botanical Garden with comfortable walking breaks.")
        st.write("🌇 Evening — Enjoy a scenic sunset viewpoint.")

    elif day == 2:
        st.write("🚂 Morning — Enjoy the Nilgiri Mountain Railway experience.")
        st.write("🌲 Afternoon — Explore a peaceful nature spot with easy access.")
        st.write("☕ Evening — Relax with Ooty tea and local snacks.")

    else:
        st.write("🌄 Morning — Visit a scenic viewpoint.")
        st.write("🌿 Afternoon — Explore a nearby nature attraction.")
        st.write("🛍️ Evening — Local shopping and relaxed family time.")

else:

    st.write("🌿 Morning — Explore a popular attraction in the destination.")
    st.write("📍 Afternoon — Discover a nearby local place.")
    st.write("🌇 Evening — Relax and enjoy the local atmosphere.")