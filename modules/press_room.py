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
        bonus_elements: Optional[List[Dict]] = None,
    ) -> str:
        """Generate HTML report with main 50/50 layout plus optional bonus section."""
        if not heading or not quote1_text or not quote1_name:
            raise ValueError("Heading, Quote1 text, and Quote1 name are required")

        body_paragraphs = self._to_paragraphs(body) if body else []
        media1_html = self._process_media(media1) if media1 else None

        bonus_html = ""
        if bonus_elements:
            bonus_html = self._generate_bonus_section(bonus_elements)

        has_media = bool(media1_html)
        sidebar_class = "quote-sidebar-with-media" if has_media else "quote-sidebar-centered"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        {self._get_styles()}
    </style>
</head>
<body>
    <div class="page-container">
        <!-- HEADER -->
        <header>
            <div class="header-left">
                <div class="brand-name">EVOLUTION STABLES</div>
            </div>
            <div class="template-type">{update_type.upper()}</div>
        </header>
        
        <!-- MAIN BODY (50/50) -->
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
            
            <!-- BONUS SECTION -->
            {bonus_html}
        </main>
        
        <!-- FOOTER -->
        <footer>
            <div class="footer-hero">
                <h2>The Future of Ownership Has Arrived</h2>
                <p>Digital-Syndication, by Evolution Stables, Powered By Tokinvest</p>
            </div>
            <div class="footer-bar">
                <div class="footer-legal">
                    <span>© {datetime.now().year} Evolution Stables</span>
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
                    <a href="https://www.linkedin.com/in/alex-baddeley/" target="_blank" aria-label="LinkedIn">
                        <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #ffffff;
            color: #000000;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            width: 430px;
            min-height: 100vh;
        }
        .page-container {
            width: 100%;
            padding: 16px 20px 24px;
            display: flex;
            flex-direction: column;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12mm;
            padding-bottom: 5mm;
            border-bottom: 2px solid #000000;
        }
        .brand-name {
            font-family: 'Inter', sans-serif;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
            text-transform: uppercase;
        }
        .template-type {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2.5px;
            text-transform: uppercase;
        }
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .content-layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }
        .headline-block {
            width: 100%;
            margin-bottom: 8mm;
        }
        .main-content {
            min-width: 0;
        }
        .headline {
            font-family: 'Playfair Display', serif;
            font-size: 52px;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 8mm;
            color: #000000;
            letter-spacing: -1px;
        }
        .subheadline {
            font-family: 'Playfair Display', serif;
            font-size: 24px;
            font-weight: 600;
            line-height: 1.3;
            margin-bottom: 6mm;
            color: #333333;
            font-style: italic;
        }
        .content {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            line-height: 1.7;
            color: #1a1a1a;
        }
        .content p {
            margin-bottom: 1em;
        }
        .quote-sidebar {
            background: #f8f8f8;
            padding: 25px 20px;
            border-left: 3px solid #000000;
            display: flex;
            flex-direction: column;
            min-height: 400px;
            gap: 20px;
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
            font-size: 18px;
            font-style: italic;
            line-height: 1.5;
            color: #000000;
            margin: 0;
            font-weight: 600;
        }
        .quote-sidebar cite {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-style: normal;
            color: #666666;
            font-weight: 500;
        }
        .canva-embed-container {
            position: relative;
            width: 70%;
            max-width: 100%;
            padding-top: 56.25%;
            margin: 0 auto 20px auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .canva-embed-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .sidebar-media-image {
            width: 70%;
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 0 auto 20px auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* BONUS SECTION */
        .bonus-section {
            display: grid;
            gap: 8mm;
            margin-bottom: 8mm;
            width: 100%;
        }
        .bonus-body {
            background: #ffffff;
            padding: 20px;
        }
        .bonus-body .content {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            line-height: 1.7;
            color: #1a1a1a;
        }
        .bonus-body .content p {
            margin-bottom: 1em;
        }
        .bonus-media {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .bonus-quote {
            background: #c9c9c9;
            padding: 24px 18px 28px;
            border-left: none;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 16px;
        }
        .bonus-quote blockquote {
            font-family: 'Playfair Display', serif;
            font-size: 18px;
            font-style: italic;
            line-height: 1.5;
            color: #000000;
            margin: 0;
            text-align: center;
        }
        .bonus-quote cite {
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-style: normal;
            color: #666666;
            font-weight: 500;
        }
        
        /* FOOTER */
        footer {
            margin-top: auto;
            padding-top: 8mm;
            border-top: 2px solid #000000;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .footer-hero {
            text-align: center;
            padding: 15px 0;
        }
        .footer-hero h2 {
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            font-weight: 600;
            color: #000000;
            margin: 0 0 8px 0;
        }
        .footer-hero p {
            font-family: 'Inter', sans-serif;
            font-size: 9px;
            color: #666666;
        }
        .footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 8px;
            border-top: 1px solid #e0e0e0;
        }
        .footer-legal {
            display: flex;
            gap: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 8px;
            color: #666666;
        }
        .footer-legal a {
            color: #666666;
            text-decoration: none;
        }
        .footer-social {
            display: flex;
            gap: 12px;
        }
        .footer-social svg {
            width: 14px;
            height: 14px;
            fill: #666666;
        }
        
        /* Mobile-focused layout; media queries kept minimal for now */
        @media (max-width: 430px) {
            .headline {
                font-size: 28px;
            }
            .subheadline {
                font-size: 16px;
            }
            .content {
                font-size: 11px;
            }
            .bonus-section {
                grid-template-columns: 1fr !important;
            }
            .quote-sidebar {
                padding: 16px;
            }
            .brand-name {
                font-size: 18px;
            }
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
                media_html = self._process_media(content)
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

    def _process_media(self, media_input: str) -> Optional[str]:
        if not media_input or not media_input.strip():
            return None

        media_input = media_input.strip()

        if "<iframe" in media_input and "canva.com" in media_input:
            iframe_match = re.search(r"<iframe[^>]*>.*?</iframe>", media_input, re.DOTALL)
            if iframe_match:
                return f'<div class="canva-embed-container">{iframe_match.group(0)}</div>'

        if "canva.com/design/" in media_input:
            design_match = re.search(r"/design/([^/]+)", media_input)
            if design_match:
                design_id = design_match.group(1)
                return f"""
                <div class="canva-embed-container">
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
                <div class="canva-embed-container">
                    <iframe src="https://www.youtube.com/embed/{video_id}" 
                            allowfullscreen>
                    </iframe>
                </div>
                """

        if "vimeo.com" in media_input:
            video_id = media_input.split("/")[-1]
            return f"""
            <div class="canva-embed-container">
                <iframe src="https://player.vimeo.com/video/{video_id}" 
                        allowfullscreen>
                </iframe>
            </div>
            """

        if any(ext in media_input.lower() for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
            return f'<img src="{media_input}" class="sidebar-media-image" />'

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
