import os
import html
import requests
import streamlit as st
from datetime import date, time, timedelta, datetime
from io import BytesIO

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="dubizzle Cars",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded",
)

                                                              
               
                                                              

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--wine:#541B2A;--wine-deep:#241017;--wine-mid:#713044;--red:#A83246;--ink:#211B1D;--muted:#81777A;--paper:#F5F1EE;--line:#E8DFDB}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important}
.stApp{background:var(--paper)!important;color:var(--ink)!important}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0}
.block-container{max-width:1450px;padding:1.2rem 3rem 5rem}
[data-testid="stSidebar"]{background:#211218!important;border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stSidebar"]>div{padding:2rem 1.25rem 1rem}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] label p{color:#E8DDE0!important;font-size:12px;font-weight:600}
[data-testid="stSidebar"] [data-testid="stTextInput"] input{background:#302027!important;color:#FFF!important;border:1px solid #60404A!important;border-radius:9px!important}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#302027!important;color:#FFF!important;border:1px solid #60404A!important;border-radius:9px!important}
[data-testid="stSidebar"] hr{border-color:#51343D!important}
.brand{font:800 29px Manrope,sans-serif;letter-spacing:-1.8px;color:#FFF!important}
.brand span{color:#D99AA4!important}
.brand-caption{font-size:9px;letter-spacing:2px;color:#BDAEB2!important;margin-top:-3px}
.side-label{font-size:9px;letter-spacing:1.8px;font-weight:800;color:#B79FA6!important;margin:26px 0 10px}
.side-note{background:#302027;border:1px solid #51343D;border-radius:12px;padding:15px;color:#D5C7CB!important;font-size:11px;line-height:1.8}
.side-note strong{color:#FFF!important}
.hero-premium{position:relative;overflow:hidden;min-height:420px;border-radius:4px 28px 4px 28px;margin:8px 0 28px;background-color:#241017;background-size:cover;background-position:center 58%;box-shadow:0 22px 55px rgba(45,20,29,.16);isolation:isolate}
.hero-premium:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(29,13,19,.98) 0%,rgba(47,19,29,.88) 43%,rgba(47,19,29,.24) 100%);z-index:-1}
.hero-content{padding:58px 56px;max-width:670px;position:relative;z-index:1}
.eyebrow{font-size:9px;letter-spacing:2.6px;font-weight:800;color:#D9A2AA!important;margin-bottom:20px;text-transform:uppercase}
.hero-premium h1{font:600 clamp(38px,4.4vw,62px)/1.06 'Playfair Display',serif;color:#FFF!important;letter-spacing:-1.2px;margin:0 0 17px}
.hero-premium p{font-size:13px;line-height:1.9;color:#E5DADD!important;max-width:430px;margin:0}
.hero-meta{margin-top:30px;color:#D8BFC5!important;font-size:9px;letter-spacing:1.8px;text-transform:uppercase}
.search-shell{background:#FFFCFA;border:1px solid var(--line);padding:20px 22px 14px;border-radius:3px 16px 3px 16px;box-shadow:0 10px 30px rgba(50,30,35,.045);margin-bottom:34px}
.search-kicker,.featured-kicker{font-size:9px;letter-spacing:2px;font-weight:800;color:var(--red)!important;text-transform:uppercase}
.search-title{font:600 23px 'Playfair Display',serif;color:var(--ink)!important;margin:4px 0 12px}
.heading{font:600 29px 'Playfair Display',serif;color:var(--ink)!important;letter-spacing:-.4px;margin:24px 0 5px}
.subheading{font-size:11px;color:var(--muted)!important;margin-bottom:18px}
.section-line{height:1px;background:var(--line);margin:24px 0}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input,.stTimeInput input{background:#FFFCFA!important;color:var(--ink)!important;border:1px solid #DCCFCB!important;border-radius:8px!important;min-height:43px}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--red)!important;box-shadow:0 0 0 2px rgba(168,50,70,.10)!important}
.stButton>button,.stFormSubmitButton>button{border-radius:8px!important;border:1px solid #DCCFCB!important;background:#FFFCFA!important;color:var(--wine)!important;min-height:42px;font-size:11px!important;font-weight:700!important;transition:all .22s ease!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-2px);border-color:var(--red)!important;background:#F8ECEE!important}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--wine)!important;color:#FFF!important;border-color:var(--wine)!important;box-shadow:0 7px 18px rgba(84,27,42,.17)}
.stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{background:var(--red)!important}
div[data-testid="stForm"]{background:#FFFCFA!important;border:1px solid var(--line)!important;border-radius:14px!important;padding:17px!important}
.featured-card{background:#FFFCFA;border:1px solid var(--line);padding:10px 10px 15px;border-radius:3px 15px 3px 15px;transition:transform .25s ease,box-shadow .25s ease;animation:fadeup .5s ease both;height:100%}
.featured-card:hover{transform:translateY(-5px);box-shadow:0 15px 32px rgba(49,24,32,.10)}
.featured-name{font:600 16px 'Playfair Display',serif;color:var(--ink)!important;margin:10px 0 4px}
.featured-price{font:700 15px Manrope,sans-serif;color:var(--wine)!important}
.featured-meta{font-size:10px;color:var(--muted)!important;margin-top:5px}
.car-card,.panel,.metric{background:#FFFCFA;border:1px solid var(--line);border-radius:3px 16px 3px 16px;padding:17px;margin:10px 0 18px}
.car-title{font:600 22px 'Playfair Display',serif;color:var(--ink)!important}
.car-price{font:700 23px Manrope,sans-serif;color:var(--wine)!important;margin:9px 0}
.car-tag{display:inline-block;background:#F3E6E7;color:var(--wine)!important;border-radius:3px;padding:6px 9px;font-size:8px;font-weight:800;letter-spacing:1.2px;margin-bottom:10px}
.car-specs{display:flex;gap:7px;flex-wrap:wrap;margin-top:13px}
.car-spec{background:#F3EEEB;border-radius:4px;padding:7px 9px;color:#65575B!important;font-size:10px;font-weight:600}
div[data-testid="stImage"] img{border-radius:4px 12px 4px 12px;transition:transform .35s ease}
div[data-testid="stImage"]:hover img{transform:scale(1.018)}
.metric-label{font-size:9px;letter-spacing:1.3px;text-transform:uppercase;color:var(--muted)!important}
.metric-value{font:600 22px 'Playfair Display',serif;color:var(--wine)!important;margin-top:8px}
.st-key-chat_launcher{position:fixed!important;right:28px!important;bottom:22px!important;width:174px!important;z-index:100000!important}
.st-key-chat_launcher .stButton>button{width:100%;height:53px;border-radius:30px!important;background:var(--wine)!important;color:#FFF!important;border:1px solid rgba(255,255,255,.18)!important;box-shadow:0 12px 30px rgba(57,20,33,.30)!important;font-size:12px!important;letter-spacing:.3px}
.st-key-chat_launcher .stButton>button:hover{background:var(--red)!important;transform:translateY(-3px)}
.st-key-chat_popup{
    position:fixed!important;
    right:28px!important;
    bottom:88px!important;
    width:410px!important;
    max-width:calc(100vw - 32px)!important;
    height:650px!important;
    overflow-y:auto!important;
    background:#FFFCFA!important;
    border:1px solid #E3D7D4!important;
    border-radius:5px 20px 5px 20px!important;
    padding:14px!important;
    box-shadow:0 24px 75px rgba(35,13,21,.28)!important;
    z-index:99999!important;
}
.st-key-chat_popup [data-testid="stVerticalBlock"]{gap:.45rem!important;min-height:0!important}\n.st-key-chat_popup [data-testid="stForm"]{flex-shrink:0!important;margin-top:8px!important;background:#FFFCFA!important;position:relative!important;z-index:2!important}\n.st-key-chat_popup [data-testid="stTextInput"] input{min-height:38px!important}\n.st-key-chat_popup [data-testid="stFormSubmitButton"] button{min-height:38px!important}
.chat-head{background:linear-gradient(115deg,#241017,#5A2032);border-radius:4px 13px 4px 13px;padding:15px 16px;margin-bottom:5px;color:#FFF!important}
.chat-head strong{color:#FFF!important;font:600 18px 'Playfair Display',serif}
.chat-head small{color:#E2C9CF!important;font-size:10px}
.chat-bubble{background:#F4EFEC;border:1px solid #E9DFDC;border-radius:4px 12px 12px 12px;padding:10px 12px;margin:6px 0;color:#403438!important;font-size:11px;line-height:1.65;overflow-wrap:anywhere}
.chat-bubble.user{background:#F4E7E9;border-color:#E8D1D5}
.chat-caption{font-size:9px;color:#9A858B!important;margin:5px 0 1px;letter-spacing:.6px;text-transform:uppercase}
.st-key-chat_popup .stTextInput input{font-size:11px!important}
.st-key-chat_popup .stFormSubmitButton>button{min-height:37px}
.footer{border-top:1px solid var(--line);margin-top:48px;padding-top:18px;text-align:center;color:#9A8D90!important;font-size:10px;line-height:1.8}
@keyframes fadeup{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:800px){.block-container{padding:1rem 1rem 5rem}.hero-content{padding:35px 25px}.hero-premium{min-height:350px}.hero-premium h1{font-size:39px}.st-key-chat_popup{right:10px!important;bottom:80px!important;width:calc(100vw - 20px)!important;height:72vh!important}.st-key-chat_launcher{right:12px!important;bottom:12px!important}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style>
""", unsafe_allow_html=True)


                                                              
             
                                                              

def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=60
        )

        if response.ok:
            return response.json()

        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        st.error(f"Request failed ({response.status_code}): {detail}")
        return None

    except requests.RequestException:
        st.error(
            "Cannot connect to the assistant. "
            "Please check that the FastAPI server is running."
        )
        return None


def api_get(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=20
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        st.error("Unable to retrieve your information from the server.")
        return None



@st.cache_data(ttl=3600, show_spinner=False)
def fetch_listing_image(image_url):
    """Fetch and cache listing images; supports WebP responses from Dubizzle."""
    if not image_url:
        return None

    try:
        response = requests.get(
            image_url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

                                                                           
        content_type = response.headers.get("content-type", "").lower()
        if not content_type.startswith("image/"):
            return None

        image_bytes = response.content
        if not image_bytes:
            return None

                                                                      
        try:
            from PIL import Image
            image = Image.open(BytesIO(image_bytes))
            image.load()
                                                              
            output = BytesIO()
            image.convert("RGB").save(output, format="PNG")
            return output.getvalue()
        except Exception:
                                                                          
                                                                               
            return image_bytes

    except (requests.RequestException, ValueError):
        return None


def display_listing_image(image_url, caption=None):
    """Render a listing image with a graceful fallback."""
    image_data = fetch_listing_image(image_url)
    if image_data:
        st.image(image_data, caption=caption, use_container_width=True)
    else:
        st.markdown(
            '<div class="panel">Vehicle image unavailable</div>',
            unsafe_allow_html=True,
        )


                                                              
               
                                                              

defaults = {
    "user_id": "demo_customer_01",
    "name": "",
    "page": "Home",
    "chat_open": False,
    "chat_history": [],
    "last_cars": [],
    "pending_chat": None,
    "latest_search_id": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


                                                              
                     
                                                              

def render_hero(title, subtitle, eyebrow="DUBIZZLE CARS", image_url=None):
    image_style = ""
    if image_url:
        safe_url = html.escape(str(image_url), quote=True)
        image_style = f'background-image:url("{safe_url}");'
    st.markdown(f"""
    <section class="hero-premium" style="{image_style}">
      <div class="hero-content">
        <div class="eyebrow">{html.escape(eyebrow)}</div>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(subtitle)}</p>
        <div class="hero-meta">Discover &nbsp; / &nbsp; Compare &nbsp; / &nbsp; Drive</div>
      </div>
    </section>
    """, unsafe_allow_html=True)


def heading(title, subtitle=""):
    st.markdown(
        f'<div class="heading">{html.escape(title)}</div>',
        unsafe_allow_html=True
    )
    if subtitle:
        st.markdown(
            f'<div class="subheading">{html.escape(subtitle)}</div>',
            unsafe_allow_html=True
        )


def render_car(car, index=None, can_save=False):
    make = str(car.get("make") or "")
    model = str(car.get("model") or "")
    year = car.get("year") or ""
    trim = str(car.get("trim") or "")

    title = html.escape(
        f"{year} {make} {model} {trim}".strip().title()
    )

    price = car.get("price_aed")
    mileage = car.get("mileage_km")

    try:
        price_label = (
            f"AED {float(price):,.0f}"
            if price is not None else "Price not specified"
        )
    except (TypeError, ValueError):
        price_label = "Price not specified"

    try:
        mileage_label = (
            f"{float(mileage):,.0f} km"
            if mileage is not None else "Not specified"
        )
    except (TypeError, ValueError):
        mileage_label = "Not specified"

    st.markdown('<div class="car-card">', unsafe_allow_html=True)

    image_col, info_col = st.columns([1.05, 1.5], gap="large")

    with image_col:
        display_listing_image(
            car.get("photo_url"),
            caption=f"{year} {make} {model}".strip()
        )

    with info_col:
        st.markdown(
            '<div class="car-tag">AVAILABLE LISTING</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="car-title">{title}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="car-price">{price_label}</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <div class="car-specs">
          <span class="car-spec">Year · {html.escape(str(year))}</span>
          <span class="car-spec">Mileage · {html.escape(mileage_label)}</span>
          <span class="car-spec">{html.escape(trim or "Standard trim")}</span>
        </div>
        """, unsafe_allow_html=True)

        if can_save and index is not None:
            if st.button(
                "Save to favourites",
                key=f"fav_{index}_{make}_{model}",
                use_container_width=True
            ):
                result = api_post(
                    f"/cars/{index}/like/{st.session_state.user_id}",
                    {}
                )
                if result:
                    st.success("Saved to your favourites.")

    st.markdown('</div>', unsafe_allow_html=True)


                                                              
         
                                                              

with st.sidebar:
    st.markdown(
        '<div class="brand">dubizzle<span>.</span></div>'
        '<div class="brand-caption">CARS · DISCOVER · DRIVE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-label">YOUR ACCOUNT</div>',
        unsafe_allow_html=True
    )

    new_name = st.text_input(
        "Your name",
        value=st.session_state.name,
        placeholder="Enter your name"
    )

    if new_name != st.session_state.name:
        st.session_state.name = new_name

    new_user = st.text_input(
        "Customer ID",
        value=st.session_state.user_id
    )

    if new_user != st.session_state.user_id:
        st.session_state.user_id = new_user
        st.session_state.chat_history = []
        st.session_state.last_cars = []
        st.session_state.latest_search_id = None

    st.divider()

    st.markdown(
        '<div class="side-label">EXPLORE</div>',
        unsafe_allow_html=True
    )

                                                                             
    page_options = ["Home", "Chat Assistant", "My Favourites", "Test Drive", "My Profile"]
    current_page = st.session_state.get("page", "Home")
    page = st.selectbox(
        "Explore pages",
        page_options,
        index=page_options.index(current_page) if current_page in page_options else 0,
        format_func=lambda item: {
            "Home": "Home",
            "Chat Assistant": "Chat with Assistant",
            "My Favourites": "My Favourites",
            "Test Drive": "Book a test drive",
            "My Profile": "My profile",
        }.get(item, item),
        label_visibility="collapsed",
        key="navigation_dropdown",
    )

    st.session_state.page = page

    st.divider()

    st.markdown("""
    <div class="side-note">
      <strong>Looking for your next car?</strong><br>
      Tell our assistant your budget, preferences and requirements.
      We'll help you explore available listings.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<span style="background:#EEF5EB;color:#527448;'
        'padding:7px 10px;border-radius:20px;font-size:10px;'
        'font-weight:700;">Assistant services</span>',
        unsafe_allow_html=True
    )


                                                              
           
                                                              

if page == "Home":
    featured_response = api_post("/cars/search", {"query": "car", "limit": 20})
    raw_featured = featured_response.get("cars", []) if featured_response else []
    featured_cars = [
        car for car in raw_featured
        if car.get("photo_url") and car.get("price_aed") is not None
    ][:6]
    hero_car = featured_cars[0] if featured_cars else None

    render_hero(
        "Find your next drive.",
        "Thoughtfully explore real listings, compare the details that matter and find a vehicle that feels right for your next chapter.",
        "THE DUBIZZLE CARS EDITION",
        hero_car.get("photo_url") if hero_car else None,
    )

    st.markdown("""
    <div class="search-shell">
      <div class="search-kicker">A MORE PERSONAL WAY TO SEARCH</div>
      <div class="search-title">What are you looking for?</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("homepage_search_form", clear_on_submit=True):
        search_col, action_col = st.columns([5, 1.25], vertical_alignment="bottom")
        with search_col:
            homepage_query = st.text_input(
                "Describe your ideal car",
                placeholder="Try: a family SUV under AED 100,000 with low mileage",
                label_visibility="collapsed",
            )
        with action_col:
            search_clicked = st.form_submit_button(
                "Explore cars",
                type="primary",
                use_container_width=True,
            )

    if search_clicked:
        if not homepage_query.strip():
            st.warning("Tell us what kind of car you're looking for.")
        else:
            st.session_state.chat_open = True
            st.session_state.chat_history.append({"role": "user", "content": homepage_query.strip()})
            with st.spinner("Finding relevant listings..."):
                search_result = api_post("/chat", {
                    "user_id": st.session_state.user_id,
                    "name": st.session_state.name or None,
                    "message": homepage_query.strip(),
                })
            if search_result:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": search_result.get("response", "I couldn't process that request."),
                    "cars": search_result.get("cars", []),
                })
                if search_result.get("cars"):
                    st.session_state.last_cars = search_result["cars"]
            st.rerun()

    heading("The current collection", "A considered selection from the available inventory.")
    if featured_cars:
        for row_start in range(0, len(featured_cars), 3):
            cols = st.columns(3, gap="medium")
            for col, car in zip(cols, featured_cars[row_start:row_start + 3]):
                with col:
                    make = str(car.get("make") or "").title()
                    model = str(car.get("model") or "").title()
                    year = car.get("year") or ""
                    trim = str(car.get("trim") or "").title()
                    price = car.get("price_aed")
                    mileage = car.get("mileage_km")
                    vehicle_name = html.escape(f"{year} {make} {model} {trim}".strip())
                    price_text = f"AED {float(price):,.0f}" if price is not None else "Price not listed"
                    mileage_text = f"{float(mileage):,.0f} km" if mileage is not None else "Mileage not listed"
                    st.markdown('<div class="featured-card">', unsafe_allow_html=True)
                    display_listing_image(car.get("photo_url"))
                    st.markdown(
                        f'<div class="featured-kicker">DUBIZZLE SELECTION</div>'
                        f'<div class="featured-name">{vehicle_name}</div>'
                        f'<div class="featured-price">{html.escape(price_text)}</div>'
                        f'<div class="featured-meta">{html.escape(mileage_text)}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No priced listings with photographs are currently available. Use the search above to explore the full inventory.")

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    heading("A considered way to find your next car", "From the first search to the first drive.")
    feature_cols = st.columns(3, gap="medium")
    features = [
        ("01", "Discover", "Describe what matters to you and explore matching vehicles from the real inventory."),
        ("02", "Compare", "Review available prices, mileage and listing details before making a decision."),
        ("03", "Experience", "Save your shortlist and request a pre-booked test-drive appointment."),
    ]
    for col, (number, title, description) in zip(feature_cols, features):
        with col:
            st.markdown(
                f'<div class="panel"><div class="featured-kicker">{number} / THE PROCESS</div>'
                f'<div class="featured-name">{title}</div>'
                f'<div class="featured-meta" style="font-size:11px;line-height:1.8;">{description}</div></div>',
                unsafe_allow_html=True,
            )



elif page == "Chat Assistant":
    render_hero(
        "Let's find your next car.",
        "Tell us what matters to you. I can search listings, compare vehicles and help request a test drive.",
        "DUBIZZLE CAR ASSISTANT"
    )

    heading("Chat with the assistant", "Ask about available cars, prices, mileage or test drives.")

    latest_car_message = max(
        (i for i, entry in enumerate(st.session_state.chat_history)
         if entry.get("role") == "assistant" and entry.get("cars")),
        default=-1,
    )
    history_start = max(0, len(st.session_state.chat_history) - 12)
    for absolute_index in range(history_start, len(st.session_state.chat_history)):
        item = st.session_state.chat_history[absolute_index]
        role_label = "You" if item["role"] == "user" else "Assistant"
        bubble_class = "user" if item["role"] == "user" else ""
        st.markdown(
            f'<div class="chat-caption">{role_label}</div>'
            f'<div class="chat-bubble {bubble_class}">'
            f'{html.escape(item["content"])}</div>',
            unsafe_allow_html=True
        )
        if item.get("cars"):
            for car_index, car in enumerate(item["cars"]):
                render_car(
                    car,
                    index=car_index,
                    can_save=(absolute_index == latest_car_message),
                )

    with st.form("full_page_chat_form", clear_on_submit=True):
        chat_text = st.text_input(
            "Message",
            placeholder="e.g. Show me Toyota SUVs under AED 100,000"
        )
        send = st.form_submit_button(
            "Send message",
            type="primary",
            use_container_width=True
        )

    if send and chat_text.strip():
        user_text = chat_text.strip()
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_text
        })
        payload = {
            "user_id": st.session_state.user_id,
            "name": st.session_state.name or None,
            "message": user_text
        }
        with st.spinner("Checking the listings..."):
            result = api_post("/chat", payload)

        if result:
            cars = result.get("cars", [])
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result.get("response", "I couldn't process that request."),
                "cars": cars
            })
            if cars:
                st.session_state.last_cars = cars
        st.rerun()


elif page == "My Favourites":
    render_hero(
        "Your saved collection.",
        "All the vehicles you've liked, together in one place.",
        "YOUR PERSONAL GARAGE"
    )

    result = api_get(f"/memory/{st.session_state.user_id}")

    if result:
        cars = result.get("liked_cars", [])

        heading(
            "Saved vehicles",
            f"You currently have {len(cars)} saved vehicle(s)."
        )

        if cars:
            for car in cars:
                render_car(car)
        else:
            st.markdown("""
            <div class="panel">
              <div style="font:800 21px Manrope;color:#20252B;">
                Your garage is waiting.
              </div>
              <p style="color:#77808A;">
                Open the assistant and save vehicles you'd like to revisit.
              </p>
            </div>
            """, unsafe_allow_html=True)


                                                              
                 
                                                              

elif page == "Test Drive":
    render_hero(
        "Take it for a drive.",
        "Found a vehicle you like? Request your preferred date and time.",
        "YOUR NEXT DRIVE"
    )

    heading(
        "Request an appointment",
        "Prebooking is required. Available Monday to Saturday, 8 AM to 8 PM."
    )

    # Only show vehicles returned by the customer's latest assistant search.
    cars = st.session_state.last_cars or []

    if not cars:
        st.info(
            "Search for vehicles in Chat Assistant first. The cars returned "
            "by your latest search will be available to select here."
        )
    else:
        options = [
            f"{car.get('year') or 'Year N/A'} {car.get('make') or ''} "
            f"{car.get('model') or ''} {car.get('trim') or ''}".strip()
            for car in cars
        ]

        selected = st.selectbox(
            "Select a vehicle",
            options=[None] + list(range(len(cars))),
            index=0,
            format_func=lambda value: "Choose a vehicle" if value is None else options[value],
            key="booking_vehicle_selection",
        )

        if selected is None:
            st.info("Choose a vehicle from your retrieved search results to continue. No car is preselected.")
        else:
            car = cars[selected]
            st.markdown(
                f'<div class="panel"><strong>{html.escape(options[selected])}</strong></div>',
                unsafe_allow_html=True
            )

            with st.form("booking_form"):
                st.markdown("#### Your details")

                customer_name = st.text_input(
                    "Full name",
                    value=st.session_state.name
                )
                phone = st.text_input("Phone number")
                booking_date = st.date_input(
                    "Preferred date",
                    min_value=date.today(),
                    value=date.today() + timedelta(days=1)
                )
                booking_time = st.time_input(
                    "Preferred time",
                    value=time(10, 0),
                    step=1800
                )
                notes = st.text_area(
                    "Additional notes",
                    placeholder="Anything else we should know?"
                )
                submitted = st.form_submit_button(
                    "Request test drive",
                    type="primary",
                    use_container_width=True
                )

                if submitted:
                    if not customer_name.strip() or not phone.strip():
                        st.error("Please enter your name and phone number.")
                    elif booking_date.weekday() == 6:
                        st.error("Test drives are available Monday to Saturday only.")
                    elif not time(8, 0) <= booking_time < time(20, 0):
                        st.error("Choose a time between 8 AM and 8 PM.")
                    elif (
                        booking_date == date.today()
                        and booking_time <= datetime.now().time().replace(
                            second=0, microsecond=0
                        )
                    ):
                        st.error("Please choose a future appointment time.")
                    else:
                        payload = {
                            "user_id": st.session_state.user_id,
                            "name": customer_name,
                            "phone": phone,
                            "make": car.get("make"),
                            "model": car.get("model"),
                            "year": car.get("year"),
                            "booking_date": booking_date.isoformat(),
                            "booking_time": booking_time.isoformat(),
                            "notes": notes,
                        }
                        result = api_post("/bookings", payload)
                        if result:
                            st.success(result.get("message", "Your request has been submitted."))
                            st.info("Your request is pending confirmation.")


elif page == "My Profile":
    render_hero(
        "Your car journey.",
        "Manage your preferences and tell us more about the vehicle you're looking for.",
        "YOUR DUBIZZLE PROFILE"
    )

    result = api_get(f"/memory/{st.session_state.user_id}")

    if result:
        profile = result.get("profile") or {}
        favourites = result.get("liked_cars", [])
        messages = result.get("recent_messages", [])

        metrics = [
            ("Customer", profile.get("name") or "Guest"),
            ("Saved cars", str(len(favourites))),
            ("Recent messages", str(len(messages))),
        ]

        cols = st.columns(3)

        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric">
                  <div class="metric-label">{html.escape(str(label))}</div>
                  <div class="metric-value">{html.escape(str(value))}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    heading(
        "Tell us what you're looking for",
        "Share your requirements so our team can better understand your needs."
    )

    with st.form("lead_form"):
        lead_name = st.text_input(
            "Full name",
            value=st.session_state.name
        )

        phone = st.text_input("Phone number")
        email = st.text_input("Email address")

        budget = st.number_input(
            "Your budget (AED)",
            min_value=0,
            value=100000,
            step=5000
        )

        make = st.text_input("Preferred make")
        model = st.text_input("Preferred model")

        requirements = st.text_area(
            "Additional requirements",
            placeholder=(
                "For example: a reliable family SUV, "
                "good fuel economy and low mileage..."
            )
        )

        submitted = st.form_submit_button(
            "Submit enquiry",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not lead_name.strip():
                st.error("Please enter your name.")
            else:
                payload = {
                    "user_id": st.session_state.user_id,
                    "name": lead_name,
                    "phone": phone or None,
                    "email": email or None,
                    "budget_aed": budget or None,
                    "preferred_make": make or None,
                    "preferred_model": model or None,
                    "requirements": requirements or None,
                }

                result = api_post("/leads", payload)

                if result:
                    st.success(
                        result.get(
                            "message",
                            "Your enquiry has been saved."
                        )
                    )


                                                              
                      
                                                              

                                                                 
                                                                   
                                                               

with st.container(key="chat_launcher"):
    launcher_label = (
        "Close assistant"
        if st.session_state.chat_open
        else "Chat with us"
    )

    if st.button(
        launcher_label,
        key="toggle_chat",
        use_container_width=True
    ):
        st.session_state.chat_open = not st.session_state.chat_open
        st.rerun()


if st.session_state.chat_open:
    with st.container(key="chat_popup"):
        st.markdown("""
        <div class="chat-head">
          <strong>dubizzle car assistant</strong><br>
          <small>Ask about listings, vehicle details or test drives.</small>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-bubble">
              Hello! I'm here to help you explore our available cars.
              What kind of vehicle are you looking for?
            </div>
            """, unsafe_allow_html=True)

                                                
        latest_car_message = max(
            (i for i, entry in enumerate(st.session_state.chat_history)
             if entry.get("role") == "assistant" and entry.get("cars")),
            default=-1,
        )
        history_start = max(0, len(st.session_state.chat_history) - 6)
        for absolute_index in range(history_start, len(st.session_state.chat_history)):
            item = st.session_state.chat_history[absolute_index]
            role_label = "You" if item["role"] == "user" else "Assistant"
            bubble_class = "user" if item["role"] == "user" else ""

            st.markdown(
                f'<div class="chat-caption">{role_label}</div>'
                f'<div class="chat-bubble {bubble_class}">'
                f'{html.escape(item["content"])}'
                f'</div>',
                unsafe_allow_html=True
            )

            if item.get("cars"):
                # Show every retrieved listing; only the latest search can be saved,
                # because the backend favourite endpoint uses the latest result set.
                for car_index, car in enumerate(item["cars"]):
                    car_name = (
                        f'{car.get("year", "")} '
                        f'{car.get("make", "")} '
                        f'{car.get("model", "")} '
                        f'{car.get("trim", "")}'
                    ).strip()
                    car_price = car.get("price_aed")
                    price_label = (
                        f'AED {float(car_price):,.0f}'
                        if car_price is not None else 'Price not specified'
                    )
                    mileage = car.get("mileage_km")
                    mileage_label = (
                        f'{float(mileage):,.0f} km'
                        if mileage is not None else 'Mileage not specified'
                    )

                    image_col, details_col = st.columns([1, 1.35], gap="small")
                    with image_col:
                        display_listing_image(car.get("photo_url"))
                    with details_col:
                        st.markdown(
                            f'<div class="chat-bubble">'
                            f'<strong>{html.escape(car_name)}</strong><br>'
                            f'{html.escape(price_label)}<br>{html.escape(mileage_label)}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        if absolute_index == latest_car_message:
                            if st.button(
                                "Save to favourites",
                                key=f'popup_fav_{absolute_index}_{car_index}_{st.session_state.user_id}',
                                use_container_width=True,
                            ):
                                saved = api_post(
                                    f"/cars/{car_index}/like/{st.session_state.user_id}",
                                    {}
                                )
                                if saved:
                                    st.success("Saved to My Favourites.")
    

        with st.form("floating_chat_form", clear_on_submit=True):
            chat_text = st.text_input(
                "Message",
                placeholder="Ask me about available cars...",
                label_visibility="collapsed"
            )

            send = st.form_submit_button(
                "Send message",
                type="primary",
                use_container_width=True
            )

        if send and chat_text.strip():
            user_text = chat_text.strip()

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_text
            })

            payload = {
                "user_id": st.session_state.user_id,
                "name": st.session_state.name or None,
                "message": user_text,
            }

            with st.spinner("Checking the listings..."):
                result = api_post("/chat", payload)

            if result:
                answer = result.get(
                    "response",
                    "I couldn't process that request."
                )

                cars = result.get("cars", [])

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "cars": cars,
                })

                if result.get("intent") == "search_cars" and cars:
                    st.session_state.last_cars = cars

            st.rerun()


                                                              
        
                                                              

st.markdown("""
<div class="footer">
  <strong style="color:#46515C;">dubizzle Cars</strong><br>
  AI-powered vehicle discovery · Discover your next drive
</div>
""", unsafe_allow_html=True)
