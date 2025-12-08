from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape


class PressRoom:
    def __init__(self, template_name: str = "report_a4.html") -> None:
        base_dir = Path(__file__).resolve().parent.parent
        templates_dir = base_dir / "assets" / "templates"
        self._env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._template_name = template_name

    def generate_report(
        self,
        heading: str,
        subheading: str,
        body: str,
        update_type: str,
        links: Optional[List[Dict[str, str]]] = None,
        quotes: Optional[List[Dict[str, str]]] = None,
        image_url: Optional[str] = None,
    ) -> str:
        if not (heading or body):
            raise ValueError("Heading or body must be provided.")

        parsed_links = self._normalize_links(links or [])
        paragraphs = self._to_paragraphs(body)
        cleaned_quotes = self._normalize_quotes(quotes or [])
        badge_icon = {
            "Trainer Update": "🏇",
            "Race Preview": "📢",
            "Race Result": "🏆",
        }.get(update_type, "📝")

        try:
            template = self._env.get_template(self._template_name)
        except TemplateNotFound as exc:
            raise FileNotFoundError(f"Template {self._template_name} not found.") from exc

        return template.render(
            heading=heading.strip(),
            subheading=subheading.strip(),
            update_type=update_type,
            update_icon=badge_icon,
            report_date=datetime.now().strftime("%d %b %Y"),
            body_paragraphs=paragraphs,
            links=parsed_links,
            quotes=cleaned_quotes,
            image_url=(image_url or "").strip() or None,
        )

    def _normalize_links(self, links: List[Dict[str, str]]) -> List[Dict[str, str]]:
        cleaned: List[Dict[str, str]] = []
        for link in links:
            url = (link.get("url") or "").strip()
            label = (link.get("label") or "").strip() or "Open Link"
            if url:
                cleaned.append({"url": url, "label": label})
        return cleaned

    def _normalize_quotes(self, quotes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        cleaned: List[Dict[str, str]] = []
        for quote in quotes:
            text = (quote.get("text") or "").strip()
            name = (quote.get("name") or "").strip()
            if text:
                cleaned.append({"text": text, "name": name})
        return cleaned

    def _to_paragraphs(self, raw_text: str) -> List[str]:
        lines = [line.strip() for line in (raw_text or "").splitlines()]
        paragraphs: List[str] = []
        buffer: List[str] = []

        for line in lines:
            if line:
                buffer.append(line)
            elif buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []

        if buffer:
            paragraphs.append(" ".join(buffer))

        return paragraphs
