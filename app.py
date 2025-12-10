import streamlit as st
import streamlit.components.v1 as components
from modules.press_room import PressRoom

st.set_page_config(page_title="Evolution Studio", layout="wide")

# Initialize Logic
press_room = PressRoom()

# Initialize Session State
if "input_data" not in st.session_state:
    st.session_state["input_data"] = {
        "heading": "", "subheading": "", "body": "",
        "media": "", "quote": "", "name": ""
    }
if "html" not in st.session_state:
    st.session_state["html"] = ""

# Sidebar (Config only)
with st.sidebar:
    st.header("🏇 Evolution Studio")
    update_type = st.selectbox("Update Type", ["Trainer Update", "Race Preview", "Race Result"])

st.title("📢 Investor Update Simulator")

# --- PARSER FUNCTION ---
def parse_raw_text(text):
    """Simple parser: Finds keywords and populates fields. First match wins."""
    lines = text.splitlines()
    data = {"heading": "", "subheading": "", "body": "", "media": "", "quote": "", "name": ""}
    
    current_key = None
    buffer = []
    
    def save_buffer(key, content):
        if key and not data[key.lower()]: # Only save if empty (First match wins)
            data[key.lower()] = content.strip()

    keywords = ["HEADING", "SUBHEADING", "BODY", "MEDIA", "QUOTE", "NAME"]

    for line in lines:
        clean = line.strip()
        upper = clean.upper()
        
        # Check if line is a keyword
        if upper in keywords:
            if current_key:
                save_buffer(current_key, "\n".join(buffer))
            current_key = upper
            buffer = []
        else:
            if current_key:
                buffer.append(clean)
    
    # Save last block
    if current_key:
        save_buffer(current_key, "\n".join(buffer))
        
    return data

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("1. Input")
    
    # Raw Input
    raw_text = st.text_area(
        "Raw Content (Tagged)", 
        height=400,
        placeholder="HEADING\nTitle...\n\nBODY\nText...\n\nMEDIA\nLink...",
        help="Paste your text with tags: HEADING, SUBHEADING, BODY, MEDIA, QUOTE, NAME"
    )
    
    # Media Controls
    st.caption("Visual Settings")
    media_orientation = st.radio(
        "Media Orientation", 
        ["Landscape (16:9)", "Portrait (9:16)"], 
        horizontal=True
    )
    is_portrait = "Portrait" in media_orientation

    # GENERATE BUTTON
    if st.button("➡️ Generate Preview", type="primary", use_container_width=True):
        # 1. Parse
        parsed = parse_raw_text(raw_text)
        st.session_state["input_data"] = parsed
        
        # 2. Build HTML
        html = press_room.generate_report(
            heading=parsed["heading"],
            subheading=parsed["subheading"],
            body=parsed["body"],
            update_type=update_type,
            quote_text=parsed["quote"],
            quote_name=parsed["name"],
            media=parsed["media"],
            media_portrait=is_portrait
        )
        st.session_state["html"] = html

    # Manual Overrides (Collapsible)
    with st.expander("📝 Manual Overrides (Edit Parsed Data)"):
        # This allows user to tweak if parser missed something
        d = st.session_state["input_data"]
        new_h = st.text_input("Heading", d["heading"])
        new_s = st.text_input("Subheading", d["subheading"])
        new_b = st.text_area("Body", d["body"])
        new_m = st.text_input("Media Link", d["media"])
        new_q = st.text_area("Quote", d["quote"])
        new_n = st.text_input("Name", d["name"])
        
        # Determine if we need to update state from manual edits
        if st.button("Update from Manual Edits"):
            st.session_state["input_data"] = {
                "heading": new_h, "subheading": new_s, "body": new_b,
                "media": new_m, "quote": new_q, "name": new_n
            }
            # Re-gen HTML
            st.session_state["html"] = press_room.generate_report(
                heading=new_h, subheading=new_s, body=new_b,
                update_type=update_type, quote_text=new_q, quote_name=new_n,
                media=new_m, media_portrait=is_portrait
            )
            st.rerun()

with col2:
    st.subheader("2. Mobile Preview")
    if st.session_state["html"]:
        components.html(
            st.session_state["html"],
            height=850,
            width=430,
            scrolling=True
        )
        st.download_button(
            "⬇️ Download HTML",
            data=st.session_state["html"],
            file_name="update.html",
            mime="text/html",
            type="primary"
        )
    else:
        st.info("Paste text and click Generate to see preview.")
