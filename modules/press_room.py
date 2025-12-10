from datetime import datetime
from typing import List, Optional
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
        quote_text: str,
        quote_name: str,
        media: Optional[str] = None,
        media_portrait: bool = False,
    ) -> str:
        """
        Generate HTML report. 
        Strict Layout: Main Body on left, Sidebar (Media/Quote/Name) on right.
        """
        # Parse body paragraphs
        body_paragraphs = self._to_paragraphs(body) if body else []
        
        # Process media
        media_html = self._process_media(media, media_portrait) if media else None

        # Load SVG watermark for header branding
        try:
            with open("assets/Evolution-Watermark-DoubleLine-Black.svg", "r", encoding="utf-8") as svg_file:
                brand_svg = svg_file.read()
        except Exception:
            brand_svg = ""

        # Load footer logo SVG
        try:
            with open("assets/Logo-Black.svg", "r", encoding="utf-8") as svg_file:
                footer_logo_svg = svg_file.read()
        except Exception:
            footer_logo_svg = ""

        # Sidebar Logic: Render if ANY sidebar element exists
        has_sidebar_content = any([media_html, quote_text, quote_name])
        
        sidebar_html = ""
        if has_sidebar_content:
            sidebar_html = f"""
            <div class="quote-sidebar">
                {media_html if media_html else ''}
                {f'<blockquote>"{quote_text}"</blockquote>' if quote_text else ''}
                {f'<cite>— {quote_name}</cite>' if quote_name else ''}
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
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
                {sidebar_html}
            </div>
        </main>
        
        <footer>
            <div class="footer-hero">
                <h2>The Future of <span class="highlight-ownership">Ownership</span><br>Has Arrived</h2>
                <p>Digital-Syndication, by Evolution Stables, Powered By Tokinvest</p>
            </div>
            <div class="footer-bar">
                <div class="footer-logo">{footer_logo_svg}</div>
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
        """CSS: Mobile-first, single column layout."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { overflow-x: hidden; width: 100%; }
        body {
            background: #ffffff; color: #000000;
            font-family: 'Inter', sans-serif;
            margin: 0; padding: 0;
            width: 430px; min-height: 100vh;
        }
        img, iframe, video { max-width: 100%; }
        .page-container {
            width: 100%; padding: 24px 24px 24px;
            display: flex; flex-direction: column; min-height: 100%;
        }
        
        /* HEADER */
        header {
            width: 100%; max-width: 430px;
            background: #ffffff;
            padding: 8px 0 12px 0;
            border-bottom: 1px solid #000000;
            display: flex;
            justify-content: flex-start;
        }
        .header-content { display: flex; flex-direction: column; align-items: flex-start; text-align: left; gap: 2px; }
        .brand-mark {
            display: block;
            line-height: 0;
            margin-bottom: 2px;
        }
        .brand-mark svg {
            height: 90px; /* visual size similar to previous header */
            width: auto;
            display: block;
        }
        .template-type {
            font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 600;
            letter-spacing: 3px; text-transform: uppercase; color: #666; margin-top: 0;
        }
        
        /* MAIN */
        main { flex: 1; display: flex; flex-direction: column; margin-top: 26px; }
        .headline-block { width: 100%; margin-bottom: 32px; text-align: left; }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 44px; font-weight: 300;
            line-height: 1.1; margin-bottom: 20px; color: #000; letter-spacing: -0.5px;
        }
        .subheadline {
            font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 400;
            line-height: 1.4; color: #222;
        }
        
        /* CONTENT */
        .content { font-family: 'Inter', sans-serif; font-size: 15px; line-height: 1.75; color: #1a1a1a; }
        .content p { margin-bottom: 1.5em; }
        .content p:first-of-type::first-letter {
            font-family: 'Playfair Display', serif; font-size: 3.8em; font-weight: 300;
            float: left; line-height: 0.8; margin-right: 8px; margin-top: 4px;
        }
        
        /* SIDEBAR (Quote/Media/Name Block) */
        .quote-sidebar {
            background: #f9f9f9; padding: 32px 24px;
            border-left: 2px solid #000000;
            display: flex; flex-direction: column; gap: 24px;
            margin-top: 12px;
        }
        .quote-sidebar blockquote {
            font-family: 'Playfair Display', serif; font-size: 22px; font-style: italic;
            line-height: 1.4; color: #000; margin: 0; font-weight: 500; text-align: center;
        }
        .quote-sidebar cite {
            font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal;
            color: #666; font-weight: 600; text-transform: uppercase;
            text-align: center; display: block; letter-spacing: 1px;
        }
        
        /* MEDIA CONTAINERS */
        .media-container-landscape {
            position: relative; width: 100%; margin: 0 auto; border-radius: 2px;
            overflow: hidden; aspect-ratio: 16/9;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .media-container-portrait {
            position: relative; width: 100%; margin: 0 auto; border-radius: 2px;
            overflow: hidden; aspect-ratio: 9/16;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        iframe, .sidebar-media-image {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; object-fit: cover;
        }
        
        /* FOOTER */
        footer {
            position: relative; width: 100%; background: #000000; color: #ffffff;
            padding: 56px 24px 60px; margin-top: 72px; display: flex; flex-direction: column;
            gap: 32px; text-align: center;
        }
        .footer-hero h2 {
            font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 400;
            color: #fff; margin: 0 0 14px 0;
        }
        .footer-hero .highlight-ownership {
            color: #d4a964;
        }
        .footer-hero p {
            font-family: 'Inter', sans-serif; font-size: 10px; color: #888;
            text-transform: uppercase; letter-spacing: 1px;
            margin: 0 0 6px 0;
        }
        .footer-bar {
            display: flex; justify-content: space-between; align-items: center;
            padding-top: 26px; border-top: 1px solid #333;
        }
        .footer-logo {
            display: flex;
            align-items: center;
        }
        .footer-logo svg {
            width: 16px;
            height: 16px;
            fill: #666;
            display: block;
        }
        .footer-social { display: flex; gap: 12px; }
        .footer-social svg { width: 16px; height: 16px; fill: #666; }
        """

    def _format_body_paragraphs(self, paragraphs: List[str]) -> str:
        if not paragraphs: return ""
        html = '<div class="content">'
        for para in paragraphs:
            html += f'<p>{para}</p>'
        html += "</div>"
        return html

    def _process_media(self, media_input: str, is_portrait: bool = False) -> Optional[str]:
        if not media_input or not media_input.strip(): return None
        media_input = media_input.strip()
        container_class = "media-container-portrait" if is_portrait else "media-container-landscape"

        if "<iframe" in media_input:
            match = re.search(r"<iframe[^>]*>.*?</iframe>", media_input, re.DOTALL)
            if match:
                return f'<div class="{container_class}">{match.group(0)}</div>'
        
        # Simple Logic: If it's a Canva link, build the iframe
        if "canva.com/design" in media_input:
            # Basic extraction - in prod might need more regex if URL varies
            try:
                # remove query params for clean ID extraction
                base = media_input.split('?')[0]
                return f"""<div class="{container_class}">
                    <iframe loading="lazy" src="{base}?embed" allowfullscreen="allowfullscreen" allow="fullscreen"></iframe>
                </div>"""
            except: pass

        return None # Fallback
    
    def _to_paragraphs(self, raw_text: str) -> List[str]:
        if not raw_text: return []
        return [p.strip() for p in raw_text.split('\n\n') if p.strip()]
