import streamlit as st
import streamlit.components.v1 as components
from modules.press_room import PressRoom

st.set_page_config(page_title="Evolution Studio", layout="wide")

press_room = PressRoom()

# --- SESSION STATE ---
if "_initialized" not in st.session_state:
    # Clear any stale internal widget IDs from previous versions of the app
    st.session_state.clear()
    st.session_state["_initialized"] = True

if "blocks" not in st.session_state:
    st.session_state["blocks"] = []  # The ordered list of content blocks
if "raw_text" not in st.session_state:
    st.session_state["raw_text"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "Input"

# Sidebar
with st.sidebar:
    st.header("🏇 Evolution Studio")
    update_type = st.selectbox(
        "Update Type",
        ["Trainer Update", "Race Preview", "Race Result"],
        key="update_type_select",
    )
    
    # Navigation
    st.markdown("---")
    page_select = st.radio(
        "Step",
        ["1. Input Content", "2. Edit Blocks"],
        index=0 if st.session_state["page"] == "Input" else 1,
        key="step_radio",
    )
    
    if page_select == "1. Input Content":
        st.session_state["page"] = "Input"
    else:
        st.session_state["page"] = "Editor"

    # "Add Block" Menu (Only visible in Editor)
    if st.session_state["page"] == "Editor":
        st.markdown("---")
        st.subheader("Add Element")
        add_type = st.selectbox("Type", ["Body Text", "Grey Box (Media/Quote)", "Heading", "Subheading"])
        if st.button("➕ Add to Bottom"):
            if add_type == "Body Text":
                st.session_state["blocks"].append({"type": "body", "content": ""})
            elif add_type == "Grey Box (Media/Quote)":
                st.session_state["blocks"].append({"type": "grey_box", "media": "", "quote": "", "name": ""})
            elif add_type == "Heading":
                st.session_state["blocks"].append({"type": "heading", "content": ""})
            elif add_type == "Subheading":
                st.session_state["blocks"].append({"type": "subheading", "content": ""})
            st.rerun()

st.title("📢 Investor Update Builder")

# --- PARSER LOGIC ---
def parse_and_order_content(text):
    """Parses raw text into an ordered list of blocks.
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
            # It's a sidebar element. Create composite block.
            grey_box = {"type": "grey_box", "media": "", "quote": "", "name": ""}
            
            # Consume adjacent sidebar items
            while i < len(segments) and segments[i]["type"] in ["media", "quote", "name"]:
                curr = segments[i]
                grey_box[curr["type"]] = curr["content"]
                i += 1
            blocks.append(grey_box)
            
    return blocks

# --- LAYOUT ---
col1, col2 = st.columns([1.2, 1])

with col1:
    if st.session_state["page"] == "Input":
        st.subheader("1. Paste Content")
        st.caption("Use tags: HEADING, SUBHEADING, BODY, MEDIA, QUOTE, NAME")
        
        raw_text = st.text_area(
            "Raw Input", 
            height=500,
            value=st.session_state["raw_text"],
            placeholder="HEADING\nTitle\n\nBODY\nText...\n\nQUOTE\nWe won!\nNAME\nTrainer"
        )
        st.session_state["raw_text"] = raw_text

        if st.button("➡️ Generate & Edit", type="primary", use_container_width=True):
            blocks = parse_and_order_content(raw_text)
            st.session_state["blocks"] = blocks
            st.session_state["page"] = "Editor"
            st.rerun()

    elif st.session_state["page"] == "Editor":
        st.subheader("2. Edit Blocks")
        
        # Helper to move items
        def move_block(index, direction):
            if direction == -1 and index > 0:
                st.session_state["blocks"][index], st.session_state["blocks"][index-1] = st.session_state["blocks"][index-1], st.session_state["blocks"][index]
            elif direction == 1 and index < len(st.session_state["blocks"]) - 1:
                st.session_state["blocks"][index], st.session_state["blocks"][index+1] = st.session_state["blocks"][index+1], st.session_state["blocks"][index]
        
        def delete_block(index):
            st.session_state["blocks"].pop(index)

        # Loop through blocks
        for i, block in enumerate(st.session_state["blocks"]):
            b_type = block["type"]
            
            # Create a container frame
            with st.expander(f"{b_type.upper().replace('_', ' ')}", expanded=True):
                
                # Content Controls
                if b_type == "heading":
                    block["content"] = st.text_input("Heading Text", block["content"], key=f"h_{i}")
                elif b_type == "subheading":
                    block["content"] = st.text_input("Subheading Text", block["content"], key=f"s_{i}")
                elif b_type == "body":
                    block["content"] = st.text_area("Body Text", block["content"], height=150, key=f"b_{i}")
                elif b_type == "grey_box":
                    block["media"] = st.text_input("Media Link", block.get("media", ""), key=f"gm_{i}")
                    block["quote"] = st.text_area("Quote", block.get("quote", ""), height=80, key=f"gq_{i}")
                    block["name"] = st.text_input("Name", block.get("name", ""), key=f"gn_{i}")

                # Action Buttons
                c1, c2, c3, c4 = st.columns([1, 1, 3, 1])
                if c1.button("⬆️", key=f"up_{i}"):
                    move_block(i, -1)
                    st.rerun()
                if c2.button("⬇️", key=f"down_{i}"):
                    move_block(i, 1)
                    st.rerun()
                if c4.button("🗑️", key=f"del_{i}", type="secondary"):
                    delete_block(i)
                    st.rerun()

        st.caption("Tip: Add new blocks from the Sidebar.")

with col2:
    st.subheader("Mobile Preview")
    
    # Global settings
    st.caption("Settings")
    orientation = st.radio("Media Style", ["Landscape (16:9)", "Portrait (9:16)"], horizontal=True)
    is_portrait = "Portrait" in orientation

    # Generate HTML from blocks
    html = press_room.generate_report(
        blocks=st.session_state.get("blocks", []),
        update_type=update_type,
        global_media_portrait=is_portrait
    )
    
    components.html(html, height=850, width=430, scrolling=True)
    
    st.download_button(
        "⬇️ Download HTML",
        data=html,
        file_name="update.html",
        mime="text/html",
        type="primary",
        use_container_width=True
    )
