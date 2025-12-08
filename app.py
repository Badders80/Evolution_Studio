import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from modules.press_room import PressRoom


load_dotenv()

st.set_page_config(page_title="Evolution Studio", layout="wide")

if "input_data" not in st.session_state:
    st.session_state["input_data"] = {
        "heading": "",
        "subheading": "",
        "body": "",
        "quotes": [],
        "image_url": "",
        "link_url": "",
        "link_label": "",
    }
if "raw_block" not in st.session_state:
    st.session_state["raw_block"] = ""
if "sidebar_collapsed" not in st.session_state:
    st.session_state["sidebar_collapsed"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Raw Content"

sidebar_container = st.sidebar
with sidebar_container:
    top_cols = st.columns([4, 1])
    with top_cols[0]:
        st.header("🏇 Evolution Studio")
        st.caption("v1.0 | Investor Hub")
    with top_cols[1]:
        if st.button("⟨⟩" if not st.session_state["sidebar_collapsed"] else "☰", help="Toggle sidebar"):
            st.session_state["sidebar_collapsed"] = not st.session_state["sidebar_collapsed"]

    label_visibility = "visible" if not st.session_state["sidebar_collapsed"] else "collapsed"
    update_type = st.selectbox(
        "Update Type", ["Trainer Update", "Race Preview", "Race Result"], label_visibility=label_visibility
    )
    template_choice = st.selectbox(
        "Template Style", ["A4 PDF Report", "Digital Social Card"], label_visibility=label_visibility
    )
    selected = st.radio(
        "Step",
        ["Raw Content", "Structured Input"],
        index=0 if st.session_state["page"] == "Raw Content" else 1,
        label_visibility=label_visibility,
    )

st.session_state["page"] = selected
page = st.session_state["page"]

template_file_map = {
    "A4 PDF Report": "report_a4.html",
    "Digital Social Card": "report_template.html",
}
template_file = template_file_map.get(template_choice, "report_template.html")

st.title("📢 Investor Update Builder")

if page == "Raw Content":
    st.subheader("0. Raw Content Staging")
    raw_block = st.text_area(
        "Paste structured content here",
        height=450,
        placeholder=(
            "Heading\nMy heading here\n\n"
            "Subheading\nMy subheading here\n\n"
            "Body\nBody text...\n\n"
            "Quote1\nQuote text...\n\n"
            "Quote2\nQuote text...\n\n"
            "Image\nhttps://image-url...\n\n"
            "Link\nhttps://video-or-article-url...\nButton Label Here"
        ),
        value=st.session_state.get("raw_block", ""),
    )

    if st.button("➡️ Continue to Structured Input", type="primary"):
        sections: dict[str, str] = {
            "Heading": "",
            "Subheading": "",
            "Body": "",
            "Quote1": "",
            "Name1": "",
            "Quote2": "",
            "Name2": "",
            "Image": "",
            "Link": "",
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

        quotes: list[dict[str, str]] = []
        if sections["Quote1"].strip():
            quotes.append({
                "text": sections["Quote1"].strip(),
                "name": sections["Name1"].strip(),
            })
        if sections["Quote2"].strip():
            quotes.append({
                "text": sections["Quote2"].strip(),
                "name": sections["Name2"].strip(),
            })

        image_url = sections["Image"].strip()

        link_raw = sections["Link"].strip()
        link_url = ""
        link_label = ""
        if link_raw:
            link_lines = [l for l in link_raw.splitlines() if l.strip()]
            if link_lines:
                link_url = link_lines[0].strip()
                if len(link_lines) > 1:
                    link_label = " ".join(link_lines[1:]).strip()

        st.session_state["raw_block"] = raw_block
        st.session_state["input_data"] = {
            "heading": sections["Heading"].strip(),
            "subheading": sections["Subheading"].strip(),
            "body": sections["Body"].strip(),
            "quotes": quotes,
            "image_url": image_url,
            "link_url": link_url,
            "link_label": link_label or "Watch Replay",
        }
        st.success("Content pushed. Switched to Structured Input.")
        st.session_state["page"] = "Structured Input"
        st.experimental_rerun()

    st.markdown("---")
    st.caption("Or use AI-powered parsing for unstructured content:")

    if st.button("🤖 Smart Parse with AI", help="Use Gemini to extract structure from messy content"):
        if not raw_block:
            st.warning("Please paste some content first")
        else:
            with st.spinner("Analyzing content with AI..."):
                try:
                    import json

                    import google.generativeai as genai

                    api_key = os.environ.get("GEMINI_API_KEY")
                    if not api_key:
                        raise RuntimeError("GEMINI_API_KEY is not set in environment.")

                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.0-flash-exp")

                    prompt = f"""Extract structured data from this racing update content.
Return ONLY valid JSON with these exact keys:
{{
  "heading": "main headline",
  "subheading": "subtitle or key message",
  "body": "full body text with paragraphs separated by \\n\\n",
  "quotes": [
    {{"text": "quote text", "name": "person name and title"}},
    {{"text": "second quote if exists", "name": "person name"}}
  ],
  "image_url": "image URL if mentioned",
  "link_url": "video or article URL if mentioned",
  "link_label": "button text like 'Watch Replay'"
}}

Content:
{raw_block}
"""

                    response = model.generate_content(prompt)
                    raw_text = response.text or ""
                    parsed = json.loads(raw_text)

                    st.session_state["input_data"] = {
                        "heading": parsed.get("heading", ""),
                        "subheading": parsed.get("subheading", ""),
                        "body": parsed.get("body", ""),
                        "quotes": parsed.get("quotes", []),
                        "image_url": parsed.get("image_url", ""),
                        "link_url": parsed.get("link_url", ""),
                        "link_label": parsed.get("link_label", "Watch Replay"),
                    }
                    st.session_state["raw_block"] = raw_block
                    st.session_state["page"] = "Structured Input"
                    st.success("✨ AI parsing complete!")
                    st.experimental_rerun()
                except Exception as e:  # pragma: no cover - best-effort UX
                    st.error(f"AI parsing failed: {e}")

elif page == "Structured Input":
    # Responsive layout: wider preview on larger screens, simple stack on narrow viewports
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. Structured Input")

        heading = st.text_input("Heading", value=st.session_state["input_data"].get("heading", ""))
        subheading = st.text_input("Subheading", value=st.session_state["input_data"].get("subheading", ""))
        body = st.text_area("Body", height=200, value=st.session_state["input_data"].get("body", ""))

        st.markdown("### Quotes")
        quotes: list[dict[str, str]] = []

        existing_quotes = st.session_state["input_data"].get("quotes", [])
        q1_default = existing_quotes[0]["text"] if len(existing_quotes) > 0 else ""
        quote_1 = st.text_area("Quote 1", height=80, value=q1_default)
        quote_1_name = st.text_input("Name 1", placeholder="Trainer / Jockey / Owner")
        if quote_1:
            quotes.append({"text": quote_1, "name": quote_1_name})

        add_second_quote = st.checkbox("Add another quote", value=len(existing_quotes) > 1)
        if add_second_quote:
            q2_default = existing_quotes[1]["text"] if len(existing_quotes) > 1 else ""
            quote_2 = st.text_area("Quote 2", height=80, value=q2_default)
            quote_2_name = st.text_input("Name 2")
            if quote_2:
                quotes.append({"text": quote_2, "name": quote_2_name})

        st.markdown("### Media")
        image_url = st.text_input(
            "Image URL",
            value=st.session_state["input_data"].get("image_url", ""),
            placeholder="https://... (can also be a hosted image link)",
        )

        st.markdown("### Embedded Link / Button")
        video_link = st.text_input(
            "Video or Article Link (YouTube/Vimeo/URL)",
            value=st.session_state["input_data"].get("link_url", ""),
        )
        link_label = st.text_input(
            "Button Label",
            value=st.session_state["input_data"].get("link_label", "Watch Replay") or "Watch Replay",
        )

        if st.button("✨ Update Preview", type="primary"):
            if heading or body:
                links = []
                if video_link:
                    links.append({"url": video_link, "label": link_label})

                try:
                    press_room = PressRoom(template_name=template_file)
                    html_output = press_room.generate_report(
                        heading=heading,
                        subheading=subheading,
                        body=body,
                        update_type=update_type,
                        links=links,
                        quotes=quotes,
                        image_url=image_url,
                    )
                    st.session_state["html"] = html_output
                except Exception as exc:
                    st.error(f"Could not build the report: {exc}")
            else:
                st.warning("Please enter a heading or body first.")

    with col2:
        st.subheader("2. Preview")
        if "html" in st.session_state:
            view = st.radio("Viewport", ["Desktop", "Tablet", "Mobile"], horizontal=True)

            if view == "Desktop":
                # Full-width desktop preview
                width = None
                height = 1400
            elif view == "Tablet":
                # Typical tablet width
                width, height = 820, 1400
            else:
                # Phone-sized viewport to trigger mobile CSS
                width, height = 430, 1100

            components.html(
                st.session_state["html"],
                height=height,
                width=width,
                scrolling=True,
            )

            st.download_button(
                label="⬇️ Download HTML File",
                data=st.session_state["html"],
                file_name="investor_update.html",
                mime="text/html",
            )
        else:
            st.info("Preview will appear here...")
