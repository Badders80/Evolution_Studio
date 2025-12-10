import os
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from modules.press_room import PressRoom

load_dotenv()

st.set_page_config(page_title="Evolution Studio", layout="wide")

press_room = PressRoom()

# --- 1. SESSION STATE INITIALIZATION ---
if "input_data" not in st.session_state:
    st.session_state["input_data"] = {
        "heading": "",
        "subheading": "",
        "body": "",
        "quote1_text": "",
        "quote1_name": "",
        "media1": "",
    }
if "bonus_section" not in st.session_state:
    st.session_state["bonus_section"] = {"enabled": False, "elements": []}
if "raw_block" not in st.session_state:
    st.session_state["raw_block"] = ""
if "sidebar_collapsed" not in st.session_state:
    st.session_state["sidebar_collapsed"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Raw Content"


# --- 2. SIDEBAR CONFIGURATION ---
sidebar_container = st.sidebar
with sidebar_container:
    top_cols = st.columns([4, 1])
    with top_cols[0]:
        st.header("🏇 Evolution Studio")
        st.caption("v1.0 | Investor Hub")
    with top_cols[1]:
        if st.button("⟨⟩" if not st.session_state["sidebar_collapsed"] else "☰"):
            st.session_state["sidebar_collapsed"] = not st.session_state["sidebar_collapsed"]

    if not st.session_state["sidebar_collapsed"]:
        update_type = st.selectbox("Update Type", ["Trainer Update", "Race Preview", "Race Result"])
        # Renamed steps for clarity
        selected = st.radio(
            "Workflow Step",
            ["1. Raw Content", "2. Editor & Preview"],
            index=0 if st.session_state["page"] == "Raw Content" else 1,
        )
    else:
        update_type = st.selectbox(
            "Update Type",
            ["Trainer Update", "Race Preview", "Race Result"],
            label_visibility="collapsed",
        )
        selected = st.radio(
            "Step",
            ["1. Raw Content", "2. Editor & Preview"],
            index=0 if st.session_state["page"] == "Raw Content" else 1,
            label_visibility="collapsed",
        )

# Map UI selection back to internal page names
if "1." in selected:
    st.session_state["page"] = "Raw Content"
else:
    st.session_state["page"] = "Structured Input"

page = st.session_state["page"]
st.title("📢 Investor Update Builder")


# ============================================
# PAGE 1: RAW CONTENT STAGING
# ============================================
if page == "Raw Content":
    st.subheader("1. Raw Content Staging")
    st.caption("Paste your rough text below. Use the AI Parser to structure it automatically.")

    # Simplified placeholder to reduce visual noise
    raw_block = st.text_area(
        "Content Dump",
        height=400,
        placeholder="Heading\n...\n\nSubheading\n...\n\nBody\n...\n\nQuote\n...",
        value=st.session_state.get("raw_block", ""),
    )

    col1, col2 = st.columns(2)

    with col1:
        # Primary Action: Move Forward
        if st.button("➡️ Continue to Editor", type="primary", use_container_width=True):
            # Basic manual parsing fallback
            sections = {
                "Heading": "", "Subheading": "", "Body": "",
                "Quote1": "", "Name1": "", "Media1": "",
            }
            current = None
            for line in (raw_block or "").splitlines():
                stripped = line.strip()
                if stripped in sections:
                    current = stripped
                    continue
                if current:
                    if current == "Body" and sections[current] and stripped:
                        sections[current] += "\n\n" + stripped
                    else:
                        sections[current] += ("\n" if sections[current] else "") + stripped

            st.session_state["input_data"] = {
                "heading": sections["Heading"].strip(),
                "subheading": sections["Subheading"].strip(),
                "body": sections["Body"].strip(),
                "quote1_text": sections["Quote1"].strip(),
                "quote1_name": sections["Name1"].strip(),
                "media1": sections["Media1"].strip(),
            }
            st.session_state["raw_block"] = raw_block
            st.session_state["page"] = "Structured Input"
            st.rerun()

    with col2:
        # AI Action
        if st.button("🤖 Smart Parse (Gemini AI)", use_container_width=True):
            if not raw_block:
                st.warning("⚠️ Paste some content first")
            else:
                api_key = os.environ.get("GEMINI_API_KEY")
                if not api_key:
                    st.error("GEMINI_API_KEY is not set")
                else:
                    with st.spinner("Analyzing content structure..."):
                        try:
                            import json
                            import google.generativeai as genai

                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel("gemini-2.0-flash-exp")

                            prompt = f"""Extract structured data from this racing update content.
Return ONLY valid JSON with these exact keys:
{{
  "heading": "main headline",
  "subheading": "subtitle or key message",
  "body": "full body text with paragraphs separated by \\n\\n",
  "quote1_text": "first quote text",
  "quote1_name": "person name and title",
  "media1": "video or image URL if mentioned"
}}

Content:
{raw_block}
"""
                            response = model.generate_content(prompt)
                            parsed = json.loads(response.text.strip().replace("``````", "").replace("json", "").replace("```", ""))

                            st.session_state["input_data"] = {
                                "heading": parsed.get("heading", ""),
                                "subheading": parsed.get("subheading", ""),
                                "body": parsed.get("body", ""),
                                "quote1_text": parsed.get("quote1_text", ""),
                                "quote1_name": parsed.get("quote1_name", ""),
                                "media1": parsed.get("media1", ""),
                            }
                            st.session_state["raw_block"] = raw_block
                            st.session_state["page"] = "Structured Input"
                            st.success("Structure extracted!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"AI parsing failed: {str(e)}")


# ============================================
# PAGE 2: EDITOR & PREVIEW
# ============================================
elif page == "Structured Input":
    col1, col2 = st.columns([1, 1.2]) # Adjusted ratio slightly to give preview more room

    # --- LEFT COLUMN: EDITOR ---
    with col1:
        st.subheader("2. Editor")

        st.caption("Required Fields")
        heading = st.text_input("Heading", value=st.session_state["input_data"].get("heading", ""))
        
        # Reduced height for density
        body = st.text_area("Body Text", height=150, value=st.session_state["input_data"].get("body", ""))

        st.caption("Optional Context")
        subheading = st.text_input("Subheading (Subtitle)", value=st.session_state["input_data"].get("subheading", ""))

        st.markdown("#### 🖼️ Hero Media & Quote")
        
        # 1. Input the Link
        media1 = st.text_area(
            "Primary Visual (URL or Embed)",
            height=80,
            value=st.session_state["input_data"].get("media1", ""),
            placeholder="https://youtu.be/... or Canva Link",
            help="Paste a YouTube, Vimeo, or Canva link here."
        )
        
        # 2. STRONG LOGIC: Only ask for orientation if media exists
        is_portrait = False  # Default to Landscape if no media
        
        if media1 and media1.strip():
            # The toggle ONLY appears if media1 is not empty
            st.caption("⚙️ Media Settings")
            media_orientation = st.radio(
                "Visual Style",
                ["Landscape (16:9)", "Portrait (9:16)"],
                horizontal=True,
                index=0,
                key="hero_media_orientation"
            )
            is_portrait = "Portrait" in media_orientation
        else:
            # Clean up UI: If they deleted the link, don't show the option
            pass 

        # Grouping Quote controls
        quote1_text = st.text_area(
            "Hero Quote Text", 
            height=100, 
            value=st.session_state["input_data"].get("quote1_text", "")
        )
        quote1_name = st.text_input(
            "Quote Author", 
            value=st.session_state["input_data"].get("quote1_name", ""), 
            placeholder="e.g. Stephen Gray, Trainer"
        )

        st.markdown("---")

        # --- BONUS SECTION ---
        st.markdown("#### ➕ Bonus Content")
        enable_bonus = st.checkbox(
            "Enable Bonus Section", value=st.session_state["bonus_section"]["enabled"]
        )

        bonus_elements = []
        if enable_bonus:
            st.info("💡 Elements display left-to-right (Desktop) or stacked (Mobile).")

            # Load existing selection
            existing_types = [
                e["type"].title() for e in st.session_state["bonus_section"].get("elements", [])
            ]
            if "bonus_selected_types" not in st.session_state:
                st.session_state["bonus_selected_types"] = existing_types

            selected_types = st.multiselect(
                "Active Elements (Max 3)",
                ["Body", "Media", "Quote"],
                default=st.session_state.get("bonus_selected_types", existing_types),
                max_selections=3,
                key="bonus_selected_types_widget",
            )

            for idx, elem_type in enumerate(selected_types, 1):
                st.markdown(f"**Element {idx}: {elem_type}**")

                if elem_type == "Body":
                    bonus_body = st.text_area(f"Bonus Body {idx}", height=100, key=f"bonus_body_{idx}")
                    if bonus_body:
                        bonus_elements.append({"type": "body", "content": bonus_body})

                elif elem_type == "Media":
                    bonus_media = st.text_area(f"Bonus Media URL {idx}", height=70, key=f"bonus_media_{idx}")
                    if bonus_media:
                        bonus_elements.append({"type": "media", "content": bonus_media})

                elif elem_type == "Quote":
                    bonus_quote = st.text_area(f"Bonus Quote {idx}", height=70, key=f"bonus_quote_{idx}")
                    bonus_name = st.text_input(f"Author {idx}", key=f"bonus_name_{idx}")
                    if bonus_quote:
                        bonus_elements.append({"type": "quote", "content": bonus_quote, "name": bonus_name})
            
            # Simple "Add" logic
            if len(selected_types) < 3:
                remaining = [t for t in ["Body", "Media", "Quote"] if t not in selected_types]
                if remaining:
                    col_add1, col_add2 = st.columns([2, 1])
                    new_type = col_add1.selectbox("Add Element type", remaining, label_visibility="collapsed")
                    if col_add2.button("Add", use_container_width=True):
                        st.session_state["bonus_selected_types"] = selected_types + [new_type]
                        st.rerun()

        st.markdown("---")

    # --- RIGHT COLUMN: PREVIEW ---
    with col2:
        # UX IMPROVEMENT: Dual Trigger
        # A refresh button at the top so users don't have to scroll down the left form
        top_bar = st.columns([3, 1])
        with top_bar[0]:
            st.subheader("3. Live Preview")
            st.caption("📱 Mobile View (iPhone 14 Pro Max)")
        with top_bar[1]:
            # This button acts as a secondary trigger for the generation logic below
            trigger_refresh = st.button("🔄 Refresh")

        if "html" in st.session_state:
            # Fixed Mobile Dimensions
            width, height = 430, 850 
            
            components.html(
                st.session_state["html"],
                height=height,
                width=width,
                scrolling=True,
            )
            
            # Download Button (High visibility)
            st.download_button(
                label="⬇️ Download Final HTML",
                data=st.session_state["html"],
                file_name=f"investor_update_{update_type.lower().replace(' ', '_')}.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
            )
        else:
            st.info("👈 Click 'Update Preview' to generate the layout.")

    # --- GENERATION LOGIC (Bottom of Col 1) ---
    # We place this here so it catches the 'Refresh' trigger from Col 2 
    # OR the main button at bottom of Col 1
    with col1:
        if st.button("✨ Update Preview", type="primary", use_container_width=True) or trigger_refresh:
            if not heading or not quote1_text or not quote1_name:
                st.error("⚠️ Missing Required Fields: Heading, Hero Quote, or Author.")
            else:
                try:
                    st.session_state["bonus_section"] = {
                        "enabled": enable_bonus,
                        "elements": bonus_elements,
                    }

                    html_output = press_room.generate_report(
                        heading=heading,
                        subheading=subheading,
                        body=body,
                        update_type=update_type,
                        quote1_text=quote1_text,
                        quote1_name=quote1_name,
                        media1=media1,
                        media_portrait=is_portrait,
                        bonus_elements=bonus_elements if enable_bonus else [],
                    )
                    st.session_state["html"] = html_output
                    st.success("Preview updated!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Error building report: {exc}")
