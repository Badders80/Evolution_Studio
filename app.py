import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from modules.press_room import PressRoom


load_dotenv()

st.set_page_config(page_title="Evolution Studio", layout="wide")

press_room = PressRoom()

# Initialize session state
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

# Sidebar
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
        selected = st.radio(
            "Step",
            ["Raw Content", "Structured Input"],
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
            ["Raw Content", "Structured Input"],
            index=0 if st.session_state["page"] == "Raw Content" else 1,
            label_visibility="collapsed",
        )

st.session_state["page"] = selected
page = st.session_state["page"]

st.title("📢 Investor Update Builder")

# ============================================
# PAGE 1: RAW CONTENT
# ============================================
if page == "Raw Content":
    st.subheader("0. Raw Content Staging")
    st.caption("Paste structured content with labels, or use AI parsing for unstructured text")

    raw_block = st.text_area(
        "Paste content here",
        height=450,
        placeholder=(
            "Heading\nFirst Gear Targeting Otaki\n\n"
            "Subheading\nPatience is key...\n\n"
            "Body\nFirst Gear has come through...\n\n"
            "Quote1\n\"Today is good because...\"\n\n"
            "Name1\nBruno Queiroz\n\n"
            "Media1\nhttps://... or <iframe>...</iframe>\n"
        ),
        value=st.session_state.get("raw_block", ""),
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➡️ Continue to Structured Input", type="primary", use_container_width=True):
            sections = {
                "Heading": "",
                "Subheading": "",
                "Body": "",
                "Quote1": "",
                "Name1": "",
                "Media1": "",
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
        if st.button("🤖 Smart Parse with AI", use_container_width=True):
            if not raw_block:
                st.warning("Please paste some content first")
            else:
                api_key = os.environ.get("GEMINI_API_KEY")
                if not api_key:
                    st.error("GEMINI_API_KEY is not set in environment")
                else:
                    with st.spinner("Analyzing content with AI..."):
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
                            parsed = json.loads(response.text.strip().replace("``````", ""))

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
                            st.success("✨ AI parsing complete!")
                            st.rerun()

                        except Exception as e:  # pragma: no cover - UX surface
                            st.error(f"AI parsing failed: {str(e)}")

# ============================================
# PAGE 2: STRUCTURED INPUT
# ============================================
elif page == "Structured Input":
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. Structured Input")

        # Main Section Inputs
        st.markdown("### Main Content")
        heading = st.text_input("Heading *", value=st.session_state["input_data"].get("heading", ""))
        subheading = st.text_input("Subheading", value=st.session_state["input_data"].get("subheading", ""))
        body = st.text_area("Body Text", height=200, value=st.session_state["input_data"].get("body", ""))

        st.markdown("### Right Column")
        media1 = st.text_area(
            "Media 1 (Canva embed/YouTube/Image URL)",
            height=100,
            value=st.session_state["input_data"].get("media1", ""),
            placeholder="<iframe>...</iframe> or https://...",
        )

        quote1_text = st.text_area(
            "Quote 1 *", height=100, value=st.session_state["input_data"].get("quote1_text", "")
        )
        quote1_name = st.text_input(
            "Name 1 *", value=st.session_state["input_data"].get("quote1_name", ""), placeholder="Bruno Queiroz, Jockey"
        )

        st.markdown("---")

        # Bonus Section
        st.markdown("### Bonus Section (Optional)")
        enable_bonus = st.checkbox(
            "Add bonus section below main content", value=st.session_state["bonus_section"]["enabled"]
        )

        bonus_elements = []
        if enable_bonus:
            st.caption("Select 1-3 elements. They'll display left-to-right automatically.")

            # Initialize stored selection state from any existing bonus elements
            existing_types = [
                e["type"].title() for e in st.session_state["bonus_section"].get("elements", [])
            ]
            if "bonus_selected_types" not in st.session_state:
                st.session_state["bonus_selected_types"] = existing_types

            selected_types = st.multiselect(
                "Choose elements (max 3)",
                ["Body", "Media", "Quote"],
                default=st.session_state.get("bonus_selected_types", existing_types),
                max_selections=3,
                key="bonus_selected_types_widget",
            )

            for idx, elem_type in enumerate(selected_types, 1):
                st.markdown(f"**Element {idx}: {elem_type}**")

                if elem_type == "Body":
                    bonus_body = st.text_area(f"Body Text {idx}", height=120, key=f"bonus_body_{idx}")
                    if bonus_body:
                        bonus_elements.append({"type": "body", "content": bonus_body})

                elif elem_type == "Media":
                    bonus_media = st.text_area(f"Media {idx} (Canva/URL)", height=80, key=f"bonus_media_{idx}")
                    if bonus_media:
                        bonus_elements.append({"type": "media", "content": bonus_media})

                elif elem_type == "Quote":
                    bonus_quote = st.text_area(f"Quote Text {idx}", height=80, key=f"bonus_quote_{idx}")
                    bonus_name = st.text_input(f"Name {idx}", key=f"bonus_name_{idx}")
                    if bonus_quote:
                        bonus_elements.append({"type": "quote", "content": bonus_quote, "name": bonus_name})

            # Inline 'Add another' control using remaining, not-yet-selected types
            remaining_types = [t for t in ["Body", "Media", "Quote"] if t not in selected_types]
            if remaining_types and len(selected_types) < 3:
                st.markdown("_Add another bonus element:_")
                add_cols = st.columns([3, 1])
                with add_cols[0]:
                    add_choice = st.selectbox(
                        "Add another",
                        remaining_types,
                        key="bonus_add_choice",
                    )
                with add_cols[1]:
                    if st.button("➕ Add", key="bonus_add_button", use_container_width=True):
                        st.session_state["bonus_selected_types"] = selected_types + [add_choice]
                        st.rerun()

        st.markdown("---")

        if st.button("✨ Update Preview", type="primary", use_container_width=True):
            if not heading or not quote1_text or not quote1_name:
                st.error("Heading, Quote 1, and Name 1 are required!")
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
                        bonus_elements=bonus_elements if enable_bonus else [],
                    )
                    st.session_state["html"] = html_output
                    st.success("Preview updated!")
                except Exception as exc:
                    st.error(f"Could not build the report: {exc}")

    with col2:
        st.subheader("2. Preview")

        if "html" in st.session_state:
            # Mobile-only preview for now
            width, height = 430, 1600

            components.html(
                st.session_state["html"],
                height=height,
                width=width,
                scrolling=True,
            )

            st.download_button(
                label="⬇️ Download HTML File",
                data=st.session_state["html"],
                file_name=f"investor_update_{update_type.lower().replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True,
            )
        else:
            st.info("👈 Fill in the required fields and click 'Update Preview'")
