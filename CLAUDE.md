# CLAUDE.md - Evolution_Studio

## What this repo is and what it solves
Evolution_Studio is a Django-based content management system for Evolution Stables. It solves the problem of creating and managing press updates for horse racing syndication by providing a user-friendly block-based editor.

## Full Stack
### What IS used:
- **Django 4.x** for backend and ORM
- **Streamlit** for content management interface
- **SQLite** for local development
- **Python 3.12** for backend services
- **python-dotenv** for environment management
- **google-generativeai** for AI features

### What IS NOT used:
- **Django REST Framework**: Not used (Streamlit interface preferred)
- **OpenAI**: Not used (Gemini API used for AI features)
- **PostgreSQL**: Not used (SQLite for local development)

## Hard Coding Rules

1. **No empty placeholder files** - Implement or don't create the file
2. **TextChoices enums** - Use TextChoices for all model choices
3. **Environment validation** - Follow env.py startup validation pattern
4. **Streamlit best practices** - Use session state for interactive elements
5. **Django ORM** - Use Django's ORM for database operations

## Project Structure
```
Evolution_Studio/
├── app.py                 # Streamlit main application
├── env.py                 # Environment validation
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3             # SQLite database
├── assets/                # Media assets (SVG, images)
├── evolution_studio_web/  # Django project settings
├── studio_content/        # Content management app
│   ├── models.py          # Update, ContentBlock, MediaAsset
│   └── migrations/        # Database migrations
├── studio_profiles/       # Horse/Owner/Trainer profiles
│   ├── models.py          # Horse, Owner, Trainer
│   └── migrations/
├── studio_leases/         # Lease management
│   ├── models.py          # Lease
│   └── migrations/
├── modules/               # Helper modules
│   └── press_room.py      # HTML generation
└── src/                   # Source code
```

## Django App Map
- **studio_profiles**: Manages horse, owner, and trainer profiles
- **studio_content**: Manages press updates, content blocks, and media assets
- **studio_leases**: Manages lease agreements between owners and trainers

## How the Block-Based Content System Works
The block-based content system is implemented in `modules/press_room.py`:

```python
class PressRoom:
    def generate_report(self, blocks: List[Dict], update_type: str) -> str:
        # Renders blocks exactly in the order provided
        # Block types: heading, subheading, body, bullets, grey_box
```

Blocks are rendered linearly with support for:
- Headings (Playfair Display font)
- Subheadings (Inter font)
- Body text with markdown support (**bold**, *italic*)
- Bullet point lists (black background with gold accent)
- Grey box (quote/media/name sidebar with gold accent border)

## References to Other Repos
- **Evolution-3.1**: Public website that will display content created in Evolution_Studio
- **Evolution-Content-Factory**: Could integrate with Evolution_Studio for video content generation
- **Evolution-Research-Engine**: Could provide data for content creation

## WSL2 Paths
- **Project Path**: `/home/evo/projects/Evolution_Studio/`
- **Windows Path**: `C:\Users\Evo\projects\Evolution_Studio\`
- **Streamlit Port**: 8501 (default)

## Current Phase and Next Build Target
- **Current Phase**: Content Management System
- **Next Build Target**: Integrate with Evolution-3.1 for content display

## Commands
- **Run Streamlit**: `streamlit run app.py` (runs on port 8501)
- **Django Migrations**: `python manage.py migrate`
- **Django Shell**: `python manage.py shell`
- **Install Dependencies**: `pip install -r requirements.txt`

## Source of Truth
**All development standards are defined in 00_DNA**:
- **Build Philosophy**: `/home/evo/00_DNA/build-philosophy/Master_Config_2026.md`
- **System Prompts**: `/home/evo/00_DNA/system-prompts/PROMPT_LIBRARY.md`
- **Brand Voice**: `/home/evo/00_DNA/brand-identity/BRAND_VOICE.md`
- **Workflows**: `/home/evo/00_DNA/workflows/`

**Core Bible Documents**:
1. `/home/evo/00_DNA/brand-identity/Evolution_Content_Factory.md` - Content Factory brand guidelines
2. `/home/evo/00_DNA/brand-identity/Branding.md` - Q7 layer institutional voice
3. `/home/evo/00_DNA/build-philosophy/Evolution_OS.md` - Technical architecture & operations manual

**Key Files to Reference**:
1. `/home/evo/00_DNA/AGENTS.core.md` - Universal agent rules
2. `/home/evo/00_DNA/build-philosophy/Master_Config_2026.md` - Hardware and architecture specs
3. `/home/evo/00_DNA/brand-identity/MESSAGING_CHEAT_SHEET.md` - Brand voice guidelines
