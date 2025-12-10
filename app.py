import streamlit as st
import streamlit.components.v1 as components
from modules.press_room import PressRoom

st.set_page_config(page_title="Evolution Studio", layout="wide")

press_room = PressRoom()

# --- SESSION STATE ---
if "blocks" not in st.session_state:
    st.session_state["blocks"] = []
if "raw_text" not in st.session_state:
    st.session_state["raw_text"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "Input" # Default start page

# --- SIDEBAR (Global Settings) ---
with st.sidebar:
    st.header("🏇 Evolution Studio")
    update_type = st.selectbox("Update Type", ["Trainer Update", "Race Preview", "Race Result"])
    
    st.markdown("---")
    # Reset Button to start over
    if st.button("Start New Update", type="secondary"):
        st.session_state["blocks"] = []
        st.session_state["raw_text"] = ""
        st.session_state["page"] = "Input"
        st.rerun()

st.title("📢 Investor Update Simulator")

# --- PARSER LOGIC ---
def parse_and_order_content(text):
    """
    Parses raw text into an ordered list of blocks.
    Groups Media/Quote/Name into 'grey_box' blocks.
    """
    lines = text.splitlines()
    blocks = []
    
    current_key = None
    buffer = []
    
    keywords = ["HEADING", "SUBHEADING", "BODY", "MEDIA", "QUOTE", "NAME"]

    # 1. Tokenize
    segments = []
    for line in lines:
        clean = line.strip()
        upper = clean.upper()
        if upper in keywords:
            if current_key:
                segments.append({"type": current_key.lower(), "content": "\n".join(buffer).strip()})
            current_key = upper
            buffer = []
        else:
            if current_key:
                buffer.append(clean)
    if current_key:
        segments.append({"type": current_key.lower(), "content": "\n".join(buffer).strip()})

    # 2. Group Sidebar Elements
    i = 0
    while i < len(segments):
        seg = segments[i]
        stype = seg["type"]
        
        if stype in ["heading", "subheading", "body"]:
            blocks.append(seg)
            i += 1
        else:
            grey_box = {"type": "grey_box", "media": "", "quote": "", "name": "", "media_portrait": False}
            seen_media = False
            while i < len(segments) and segments[i]["type"] in ["media", "quote", "name"]:
                curr = segments[i]
                ctype = curr["type"]

                # If we encounter a second MEDIA in the same run, start a new grey box
                if ctype == "media" and seen_media:
                    # close current grey_box and start a fresh one without advancing i
                    blocks.append(grey_box)
                    grey_box = {"type": "grey_box", "media": "", "quote": "", "name": "", "media_portrait": False}
                    seen_media = False
                    continue

                grey_box[ctype] = curr["content"]
                if ctype == "media":
                    seen_media = True
                i += 1

            blocks.append(grey_box)
            
    return blocks

# --- LAYOUT ---
col1, col2 = st.columns([1.2, 1])

# === LEFT COLUMN: EDITOR & INPUT ===
with col1:
    # VIEW 1: RAW INPUT (The "Dump")
    if st.session_state["page"] == "Input":
        st.subheader("1. Content Ingestion")
        st.caption("Paste your tagged content below.")
        
        raw_text = st.text_area(
            "Raw Input", 
            height=500,
            value=st.session_state["raw_text"],
            placeholder="HEADING\nTitle\n\nBODY\nText...\n\nQUOTE\nWe won!\nNAME\nTrainer",
            label_visibility="collapsed"
        )
        st.session_state["raw_text"] = raw_text

        if st.button("➡️ Generate & Edit", type="primary", use_container_width=True):
            blocks = parse_and_order_content(raw_text)
            st.session_state["blocks"] = blocks
            st.session_state["page"] = "Editor" # Auto-switch to editor
            st.rerun()

    # VIEW 2: BLOCK EDITOR (The "Builder")
    elif st.session_state["page"] == "Editor":
        st.subheader("2. Story Builder")
        
        # Helper Functions
        def move_block(index, direction):
            if direction == -1 and index > 0:
                st.session_state["blocks"][index], st.session_state["blocks"][index-1] = st.session_state["blocks"][index-1], st.session_state["blocks"][index]
            elif direction == 1 and index < len(st.session_state["blocks"]) - 1:
                st.session_state["blocks"][index], st.session_state["blocks"][index+1] = st.session_state["blocks"][index+1], st.session_state["blocks"][index]
        
        def delete_block(index):
            st.session_state["blocks"].pop(index)

        # 1. Render the Stack
        if not st.session_state["blocks"]:
            st.info("No blocks yet. Add one below!")

        for i, block in enumerate(st.session_state["blocks"]):
            b_type = block["type"]
            
            # Use columns to put Move/Delete buttons on the same row as the expander
            # Note: Streamlit layout is tricky here, putting buttons INSIDE the expander is cleaner for width
            
            label_map = {
                "heading": "H1 Heading",
                "subheading": "H2 Subheading",
                "body": "Body Text",
                "bullets": "Bullet List",
                "grey_box": "Sidebar Module (Media/Quote)"
            }
            
            with st.expander(f"{label_map.get(b_type, b_type)}  (#{i+1})", expanded=False):
                # Content Inputs
                if b_type == "heading":
                    block["content"] = st.text_input("Text", block["content"], key=f"h_{i}", label_visibility="collapsed")
                elif b_type == "subheading":
                    block["content"] = st.text_input("Text", block["content"], key=f"s_{i}", label_visibility="collapsed")
                elif b_type == "body":
                    block["content"] = st.text_area("Text", block["content"], height=150, key=f"b_{i}", label_visibility="collapsed")
                elif b_type == "bullets":
                    st.caption("One item per line")
                    block["content"] = st.text_area("List Items", block["content"], height=100, key=f"bl_{i}", label_visibility="collapsed")
                elif b_type == "grey_box":
                    st.caption("Media")
                    block["media"] = st.text_input("Media Link", block.get("media", ""), key=f"gm_{i}")
                    # Per-block media orientation
                    current_portrait = block.get("media_portrait", False)
                    orientation_choice = st.radio(
                        "Media Aspect Ratio",
                        ["Landscape (16:9)", "Portrait (9:16)"],
                        index=1 if current_portrait else 0,
                        horizontal=True,
                        key=f"ratio_{i}",
                    )
                    block["media_portrait"] = "Portrait" in orientation_choice
                    st.caption("Quote")
                    block["quote"] = st.text_area("Quote", block.get("quote", ""), height=80, key=f"gq_{i}")
                    st.caption("Name")
                    block["name"] = st.text_input("Name", block.get("name", ""), key=f"gn_{i}")

                # Formatting hint
                st.caption("Formatting: use **bold** and *italics* markdown in text fields.")

                # Control Bar (Move Up / Move Down / Delete)
                c1, c2, c3, c4 = st.columns([1, 1, 4, 1])
                if c1.button("⬆️", key=f"up_{i}", help="Move Up"):
                    move_block(i, -1)
                    st.rerun()
                if c2.button("⬇️", key=f"down_{i}", help="Move Down"):
                    move_block(i, 1)
                    st.rerun()
                if c4.button("🗑️", key=f"del_{i}", type="secondary", help="Delete Block"):
                    delete_block(i)
                    st.rerun()

        # 2. "Add Block" Section (At the bottom of the stack)
        st.markdown("---")
        st.markdown("##### ➕ Add New Block")
        
        add_col1, add_col2 = st.columns([3, 1])
        with add_col1:
            add_type = st.selectbox(
                "Block Type", 
                ["Body Text", "Bullet List", "Grey Box (Media/Quote)", "Heading", "Subheading"],
                label_visibility="collapsed"
            )
        with add_col2:
            if st.button("Add Block", use_container_width=True):
                if add_type == "Body Text":
                    st.session_state["blocks"].append({"type": "body", "content": ""})
                elif add_type == "Bullet List":
                    st.session_state["blocks"].append({"type": "bullets", "content": "• Point 1\n• Point 2"})
                elif add_type == "Grey Box (Media/Quote)":
                    st.session_state["blocks"].append({"type": "grey_box", "media": "", "quote": "", "name": ""})
                elif add_type == "Heading":
                    st.session_state["blocks"].append({"type": "heading", "content": ""})
                elif add_type == "Subheading":
                    st.session_state["blocks"].append({"type": "subheading", "content": ""})
                st.rerun()

# === RIGHT COLUMN: PREVIEW ===
with col2:
    st.subheader("Mobile Preview")
    
    # Generate HTML from blocks (orientation is now per-grey-box)
    html = press_room.generate_report(
        blocks=st.session_state.get("blocks", []),
        update_type=update_type,
    )
    
    # Preview Container (Fixed Width)
    components.html(html, height=850, width=430, scrolling=True)
    
    # Place Download + Regenerate side by side, filling the full column width
    col_download, col_regen = st.columns(2)
    with col_download:
        st.download_button(
            "⬇️ Download HTML",
            data=html,
            file_name="update.html",
            mime="text/html",
            type="primary",
            use_container_width=True,
        )
    with col_regen:
        if st.button(
            "🔄 Regenerate Preview",
            help="Force a full refresh if things look stuck",
            use_container_width=True,
        ):
            st.experimental_rerun()
