from datetime import datetime
from typing import List, Dict, Optional
import re

class PressRoom:
    def __init__(self) -> None:
        pass

    def generate_report(
        self,
        blocks: List[Dict],
        update_type: str,
        global_media_portrait: bool = False,
    ) -> str:
        """
        Generate HTML report using a Linear "Block" layout.
        Renders blocks exactly in the order provided.
        """
        
        # Validation
        if not isinstance(blocks, list):
            raise ValueError("blocks must be a list")
        
        main_content_html = ""
        
        # Iterate through the blocks and build HTML linearly
        for block in blocks:
            b_type = block.get("type")
            content = block.get("content", "")
            
            if b_type == "heading":
                main_content_html += f'<h1 class="headline">{content}</h1>'
            
            elif b_type == "subheading":
                main_content_html += f'<div class="subheadline">{content}</div>'
                
            elif b_type == "body":
                # Render standard text
                main_content_html += self._format_body_paragraphs(content)

            elif b_type == "bullets":
                # Render bullet points
                items = [line.strip() for line in content.split('\n') if line.strip()]
                if items:
                    list_items = "".join([f"<li>{item}</li>" for item in items])
                    main_content_html += f'''
                    <div class="bullet-highlight">
                        <ul class="bullet-list">{list_items}</ul>
                    </div>
                    '''
                
            elif b_type == "grey_box":
                # Render the grouped Media/Quote/Name block (The Sidebar Style)
                media_html = ""
                if block.get("media"):
                    is_portrait = block.get("media_portrait", global_media_portrait)
                    media_html = self._process_media(block["media"], is_portrait) or ""
                
                quote_html = (
                    f'<blockquote><span class="quote-mark">“</span>--{block["quote"]}--<span class="quote-mark">”</span></blockquote>'
                    if block.get("quote")
                    else ""
                )
                name_html = f'<cite>— {block["name"]}</cite>' if block.get("name") else ""
                
                if media_html or quote_html or name_html:
                    main_content_html += f"""
                    <div class="quote-sidebar">
                        {media_html}
                        {quote_html}
                        {name_html}
                    </div>
                    """

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

        # Ensure update_type is a string for safe uppercasing
        update_label = str(update_type) if update_type is not None else ""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Geist+Sans:wght@400;500;600&family=Playfair+Display:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;500;600;800&display=swap" rel="stylesheet">
    <style>
        {self._get_styles()}
    </style>
</head>
<body>
    <div class="page-container">
        <header>
            <div class="header-content">
                <div class="brand-mark">{brand_svg}</div>
                <div class="template-type">{update_label.upper()}</div>
            </div>
        </header>
        
        <main>
            <div class="content-layout">
                {main_content_html}
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
                    <a href="https://www.linkedin.com/in/alex-baddeley/" target="_blank" aria-label="LinkedIn">
                        <svg viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.88 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1 4.98 2.12 4.98 3.5zM0 8h5v16H0V8zm8.5 0h4.8v2.2h.07c.67-1.27 2.3-2.6 4.73-2.6 5.06 0 6 3.33 6 7.66V24h-5v-7.3c0-1.74-.03-3.98-2.43-3.98-2.43 0-2.8 1.9-2.8 3.86V24h-5V8z"/></svg>
                    </a>
                    <a href="https://x.com/evostables" target="_blank" aria-label="X">
                        <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://instagram.com/evostables" target="_blank" aria-label="Instagram">
                        <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
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
        
        /* .headline-block removed as we are linear now */
        
        .headline {
            font-family: 'Playfair Display', serif; 
            font-size: 44px; 
            font-weight: 400; /* UPDATED: Slightly heavier (was 300) */
            line-height: 1.1; 
            margin-bottom: 20px; 
            color: #000; 
            letter-spacing: -0.5px;
        }
        .subheadline {
            font-family: 'Inter', sans-serif; /* UPDATED: Changed to Inter */
            font-size: 20px; /* UPDATED: Inter is naturally larger, so 20px matches the previous 22px visual */
            font-weight: 500; /* UPDATED: Medium weight for emphasis */
            line-height: 1.5; 
            color: #222; 
            margin-bottom: 24px;
            text-align: justify;
            hyphens: none;
        }
        
        /* CONTENT (Spread look) */
        .content { 
            font-family: 'Inter', sans-serif; 
            font-size: 15px; 
            line-height: 1.75; 
            color: #1a1a1a; 
            margin-bottom: 16px;
            text-align: justify;
            hyphens: none;
        }
        .content p { margin-bottom: 2em; }
        /* Only apply drop cap to the VERY first paragraph of the main content area if it appears first */
        .content:first-of-type p:first-of-type::first-letter {
            font-family: 'Playfair Display', serif; font-size: 3.8em; font-weight: 300;
            float: left; line-height: 0.8; margin-right: 8px; margin-top: 4px;
        }
        
        /* BULLET LISTS */
        .bullet-highlight {
            background: #000000;
            color: #ffffff;
            padding: 28px 24px;
            border-left: 3px solid #d4a964;
            margin: 24px 0;
        }
        .bullet-list {
            font-family: 'Inter', sans-serif;
            font-size: 20px;
            font-weight: 500;
            line-height: 1.5;
            color: #ffffff;
            list-style: disc;
            margin: 0;
            padding-left: 22px;
            text-align: left;
        }
        .bullet-list li { margin-bottom: 10px; }
        .bullet-list li:last-child { margin-bottom: 0; }
        .bullet-list li::marker { color: #ffffff; font-size: 1em; }
        
        /* SIDEBAR (Quote/Media/Name Block) */
        .quote-sidebar {
            background: #fafafa; 
            padding: 32px 24px;
            border-left: 3px solid #d4a964; /* Gold accent, slightly thicker */
            display: flex; flex-direction: column; gap: 24px;
            margin: 24px 0;
        }
        .quote-sidebar blockquote {
            font-family: 'Geist Sans', sans-serif;
            font-size: 20px;
            font-style: normal;
            font-weight: 500;
            line-height: 1.7;
            color: #000;
            margin: 0;
            text-align: left;
            letter-spacing: -0.01em;
        }
        .quote-sidebar cite {
            font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal;
            color: #666; font-weight: 600; text-transform: uppercase;
            text-align: left; display: block; letter-spacing: 1px;
        }
        .quote-sidebar .quote-mark {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            line-height: 0.8;
            vertical-align: top;
            margin-right: 4px;
        }
        
        /* MEDIA CONTAINERS */
        .media-container-landscape {
            position: relative; width: 100%; margin: 0 auto; border-radius: 8px;
            overflow: hidden; aspect-ratio: 16/9;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .media-container-portrait {
            position: relative; width: 100%; margin: 0 auto; border-radius: 8px;
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
            font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 400;
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
            padding-top: 26px;
        }
        .footer-logo {
            display: flex;
            align-items: center;
        }
        .footer-logo svg {
            width: 16px;
            height: 16px;
            fill: #d4a964;
            display: block;
        }
        .footer-social { display: flex; gap: 12px; }
        .footer-social svg { width: 16px; height: 16px; fill: #d4a964; }
        """

    def _format_body_paragraphs(self, paragraphs: str) -> str:
        """Accept raw text, apply basic markdown, and split into paragraphs."""
        if not paragraphs:
            return ""
        
        # Basic markdown support
        def apply_markdown(text):
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)  # **bold**
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)  # *italic*
            return text
        
        parts = [apply_markdown(p.strip()) for p in paragraphs.split("\n\n") if p.strip()]
        if not parts:
            return ""
        
        html = '<div class="content">'
        for para in parts:
            html += f'<p>{para}</p>'
        html += "</div>"
        return html

    def _process_media(self, media_input: str, is_portrait: bool = False) -> Optional[str]:
        if not media_input or not media_input.strip(): 
            return None
        
        media_input = media_input.strip()
        container_class = "media-container-portrait" if is_portrait else "media-container-landscape"

        # Handle existing iframes
        if "<iframe" in media_input:
            match = re.search(r"<iframe[^>]*>.*?</iframe>", media_input, re.DOTALL)
            if match:
                return f'<div class="{container_class}">{match.group(0)}</div>'
        
        # YouTube handling
        if "youtube.com" in media_input or "youtu.be" in media_input:
            try:
                video_id = None
                if "youtu.be/" in media_input:
                    video_id = media_input.split("youtu.be/")[1].split("?")[0]
                elif "watch?v=" in media_input:
                    video_id = media_input.split("watch?v=")[1].split("&")[0]
                
                if video_id:
                    return f'''<div class="{container_class}">
                        <iframe src="https://www.youtube.com/embed/{video_id}" 
                                frameborder="0" allowfullscreen loading="lazy"></iframe>
                    </div>'''
            except Exception:
                return None
        
        # Canva handling
        if "canva.com/design" in media_input:
            try:
                base = media_input.split('?')[0]
                return f'''<div class="{container_class}">
                    <iframe loading="lazy" src="{base}?embed" 
                            allowfullscreen="allowfullscreen" allow="fullscreen"></iframe>
                </div>'''
            except Exception:
                return None

        return None
