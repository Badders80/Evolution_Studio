from datetime import datetime
from typing import Dict, List, Optional
import re


class PressRoom:
    def __init__(self) -> None:
        pass

    def generate_report(
        self,
        heading: str,
        subheading: str,
        body: str,
        update_type: str,
        quote1_text: str,
        quote1_name: str,
        media1: Optional[str] = None,
        media_portrait: bool = False,
        bonus_elements: Optional[List[Dict]] = None,
    ) -> str:
        """Generate HTML report with main layout plus optional bonus section."""
        if not heading or not quote1_text or not quote1_name:
            raise ValueError("Heading, Quote1 text, and Quote1 name are required")

        body_paragraphs = self._to_paragraphs(body) if body else []
        
        # Process media with orientation logic
        media1_html = self._process_media(media1, media_portrait) if media1 else None

        # Load SVG watermark for header branding
        try:
            with open("assets/Evolution-Watermark-DoubleLine-Black.svg", "r", encoding="utf-8") as svg_file:
                brand_svg = svg_file.read()
        except Exception:
            brand_svg = ""

        bonus_html = ""
        if bonus_elements:
            bonus_html = self._generate_bonus_section(bonus_elements)

        sidebar_class = "quote-sidebar-with-media" if media1_html else "quote-sidebar-centered"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        {self._get_styles()}
    </style>
</head>
<body>
    <div class="page-container">
        <header>
            <div class="header-content">
                <div class="brand-mark">{brand_svg}</div>
                <div class="template-type">{update_type.upper()}</div>
            </div>
        </header>
        
        <main>
            <div class="headline-block">
                <h1 class="headline">{heading}</h1>
                {f'<div class="subheadline">{subheading}</div>' if subheading else ''}
            </div>
            
            <div class="content-layout">
                <div class="main-content">
                    {self._format_body_paragraphs(body_paragraphs)}
                </div>
                
                <div class="quote-sidebar {sidebar_class}">
                    {media1_html if media1_html else ''}
                    <blockquote>"{quote1_text}"</blockquote>
                    <cite>— {quote1_name}</cite>
                </div>
            </div>
            
            {bonus_html}
        </main>
        
        <footer>
            <div class="footer-hero">
                <h2>The Future of Ownership Has Arrived</h2>
                <p>Digital-Syndication, by Evolution Stables, Powered By Tokinvest</p>
            </div>
            <div class="footer-bar">
                <div class="footer-legal">
                    <span> 2023 Evolution Stables</span>
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                </div>
                <div class="footer-social">
                    <a href="https://x.com/evostables" target="_blank" aria-label="X">
                        <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://instagram.com/evostables" target="_blank" aria-label="Instagram">
                        <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    </a>
                    <a href="mailto:alex@evolutionstables.nz" aria-label="Email">
                        <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                    </a>
                </div>
            </div>
        </footer>
    </div>
</body>
</html>"""
        return html

    def _get_styles(self) -> str:
        """Complete CSS styles for the layout."""
        return """
        /* --- RESET & GLOBAL SAFEGUARDS --- */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html, body {
            overflow-x: hidden; /* Prevents horizontal scroll/wobble */
            width: 100%;
        }
        body {
            background: #ffffff;
            color: #000000;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            width: 430px; /* Locked mobile width for simulation */
            min-height: 100vh;
        }
        img, iframe, video {
            max-width: 100%; /* Prevents media from breaking layout */
        }
        .page-container {
            width: 100%;
            padding: 16px 20px 24px;
            display: flex;
            flex-direction: column;
        }
        
        /* HEADER STYLES (non-sticky, left-aligned) */
        header {
            width: 100%;
            max-width: 430px; /* Ensure header doesn't stretch on desktop view */
            background: #ffffff;
            border-bottom: 2px solid #000000;
            padding: 20px 0 15px 0;
            display: flex;
            justify-content: flex-start;
        }
        .header-content {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
            padding: 0 20px;
            gap: 6px;
        }
        .brand-mark {
            display: block;
            line-height: 0;
        }
        .brand-mark svg {
            height: 40px;
            width: auto;
            display: block;
        }
        .template-type {
            font-family: 'Inter', sans-serif;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #666;
        }
        
        /* MAIN CONTENT TYPOGRAPHY */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .content-layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-bottom: 16px;
        }
        .headline-block {
            width: 100%;
            margin-bottom: 24px;
            text-align: left;
        }
        .main-content {
            min-width: 0;
        }
        .headline {
            font-family: 'Playfair Display', serif;
            font-size: 46px; /* PUNCHIER: Bigger size */
            font-weight: 900;
            line-height: 1.05; /* Tighter leading */
            margin-bottom: 16px;
            color: #000000;
            letter-spacing: -1.5px; /* Tighter tracking for impact */
        }
        .subheadline {
            font-family: 'Playfair Display', serif;
            font-size: 22px; /* PUNCHIER: Larger size */
            font-weight: 600; /* PUNCHIER: Heavier weight */
            line-height: 1.35;
            color: #111111; /* Darker for better contrast */
            font-style: italic;
        }
        .content {
            font-family: 'Inter', sans-serif;
            font-size: 14px; /* Slightly larger body text for readability */
            line-height: 1.7;
            color: #1a1a1a;
        }
        .content p {
            margin-bottom: 1.4em;
        }
        /* Editorial Drop Cap for First Paragraph */
        .content p:first-of-type::first-letter {
            font-family: 'Playfair Display', serif;
            font-size: 3.8em;
            font-weight: 700;
            float: left;
            line-height: 0.8;
            margin-right: 8px;
            margin-top: 4px;
        }
        
        /* SIDEBAR / MEDIA / QUOTES */
        .quote-sidebar {
            background: #f8f8f8;
            padding: 32px 24px;
            border-left: 4px solid #000000; /* Thicker accent line */
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        .quote-sidebar-with-media {
            justify-content: flex-start;
        }
        .quote-sidebar-centered {
            justify-content: center;
            align-items: center;
        }
        .quote-sidebar blockquote {
            font-family: 'Playfair Display', serif;
            font-size: 24px; /* PUNCHIER: Magazine style size */
            font-style: italic;
            line-height: 1.3;
            color: #000000;
            margin: 0;
            font-weight: 700; /* Bold quote */
            text-align: center;
        }
        .quote-sidebar cite {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-style: normal;
            color: #666666;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            display: block;
            letter-spacing: 1px;
        }
        
        /* MEDIA CONTAINERS */
        .media-container-landscape, .media-container-portrait {
            position: relative;
            width: 100%; /* Changed to 100% of the sidebar/container */
            max-width: 85%; /* Constrained for aesthetics */
            margin: 0 auto 10px auto;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        .media-container-landscape {
            aspect-ratio: 16/9;
        }
        .media-container-portrait {
            aspect-ratio: 9/16;
        }
        .media-container-landscape iframe, .media-container-portrait iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .sidebar-media-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* BONUS SECTION */
        .bonus-section {
            display: grid;
            gap: 32px;
            margin-bottom: 32px;
            width: 100%;
        }
        .bonus-body {
            background: #ffffff;
            padding: 0;
        }
        .bonus-media {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .bonus-quote {
            background: #eaeaea; /* Slightly darker than sidebar for differentiation */
            padding: 30px 24px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 16px;
        }
        .bonus-quote blockquote {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            font-style: italic;
            line-height: 1.4;
            color: #000000;
            margin: 0;
            text-align: center;
            font-weight: 600;
        }
        
        /* FOOTER STYLES (non-sticky) */
        footer {
            width: 100%;
            max-width: 430px; /* Locked to simulation width */
            background: #000000;
            color: #ffffff;
            padding: 30px 20px 40px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            text-align: center;
            margin-top: 32px;
        }
        .footer-hero h2 {
            font-family: 'Playfair Display', serif;
            font-size: 24px;
            font-weight: 600;
            color: #ffffff;
            margin: 0 0 10px 0;
        }
        .footer-hero p {
            font-family: 'Inter', sans-serif;
            font-size: 10px;
            color: #aaaaaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 16px;
            border-top: 1px solid #333333;
        }
        .footer-legal {
            display: flex;
            gap: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 9px;
            color: #888888;
        }
        .footer-legal a {
            color: #888888;
            text-decoration: none;
            transition: color 0.2s;
        }
        .footer-legal a:hover {
            color: #ffffff;
        }
        .footer-social {
            display: flex;
            gap: 12px;
        }
        .footer-social svg {
            width: 16px;
            height: 16px;
            fill: #888888;
            transition: fill 0.2s;
        }
        .footer-social a:hover svg {
            fill: #ffffff;
        }

        @media (max-width: 430px) {
            .headline { font-size: 36px; } 
            .content { font-size: 14px; }
            .bonus-section { grid-template-columns: 1fr !important; }
        }
        """

    def _format_body_paragraphs(self, paragraphs: List[str]) -> str:
        if not paragraphs:
            return ""
        html = '<div class="content">'
        for para in paragraphs:
            html += f'<p>{para}</p>'
        html += "</div>"
        return html

    def _generate_bonus_section(self, elements: List[Dict]) -> str:
        if not elements:
            return ""

        num_elements = len(elements)
        grid_layouts = {
            1: "1fr",
            2: "1fr 1fr",
            3: "1fr 1fr 1fr",
        }
        grid_template = grid_layouts.get(num_elements, "1fr")

        html = f'<div class="bonus-section" style="grid-template-columns: {grid_template};">'

        for element in elements:
            elem_type = element.get("type")
            content = element.get("content", "")

            if elem_type == "body":
                paragraphs = self._to_paragraphs(content)
                html += '<div class="bonus-body"><div class="content">'
                for para in paragraphs:
                    html += f'<p>{para}</p>'
                html += "</div></div>"

            elif elem_type == "media":
                # For bonus media, default to landscape/square, or we could add logic
                media_html = self._process_media(content, is_portrait=False) 
                if media_html:
                    html += f'<div class="bonus-media">{media_html}</div>'

            elif elem_type == "quote":
                name = element.get("name", "")
                html += f"""
                <div class="bonus-quote">
                    <blockquote>"{content}"</blockquote>
                    <cite>— {name}</cite>
                </div>
                """

        html += "</div>"
        return html

    def _process_media(self, media_input: str, is_portrait: bool = False) -> Optional[str]:
        if not media_input or not media_input.strip():
            return None

        media_input = media_input.strip()
        
        # Determine container class based on orientation flag
        container_class = "media-container-portrait" if is_portrait else "media-container-landscape"

        if "<iframe" in media_input and "canva.com" in media_input:
            iframe_match = re.search(r"<iframe[^>]*>.*?</iframe>", media_input, re.DOTALL)
            if iframe_match:
                # Canva embeds often have their own styles, but we wrap them
                return f'<div class="{container_class}">{iframe_match.group(0)}</div>'

        if "canva.com/design/" in media_input:
            design_match = re.search(r"/design/([^/]+)", media_input)
            if design_match:
                design_id = design_match.group(1)
                return f"""
                <div class="{container_class}">
                    <iframe loading="lazy" 
                            src="https://www.canva.com/design/{design_id}/watch?embed" 
                            allowfullscreen="allowfullscreen" 
                            allow="fullscreen">
                    </iframe>
                </div>
                """

        if "youtube.com" in media_input or "youtu.be" in media_input:
            video_id = None
            if "youtu.be/" in media_input:
                video_id = media_input.split("youtu.be/")[1].split("?")[0]
            elif "v=" in media_input:
                video_id = media_input.split("v=")[1].split("&")[0]
            if video_id:
                return f"""
                <div class="{container_class}">
                    <iframe src="https://www.youtube.com/embed/{video_id}" 
                            allowfullscreen>
                    </iframe>
                </div>
                """

        if "vimeo.com" in media_input:
            video_id = media_input.split("/")[-1]
            return f"""
            <div class="{container_class}">
                <iframe src="https://player.vimeo.com/video/{video_id}" 
                        allowfullscreen>
                </iframe>
            </div>
            """

        if any(ext in media_input.lower() for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
            return f"""
            <div class="{container_class}">
                <img src="{media_input}" class="sidebar-media-image" />
            </div>
            """

        return None

    def _to_paragraphs(self, raw_text: str) -> List[str]:
        if not raw_text:
            return []

        paragraphs = raw_text.split("\n\n")
        cleaned: List[str] = []

        for para in paragraphs:
            cleaned_para = " ".join(para.strip().split("\n"))
            if cleaned_para:
                cleaned.append(cleaned_para)

        return cleaned
