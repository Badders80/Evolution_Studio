# Evolution Stables - System Patterns

## Project Structure Patterns

### Evolution-3.1 (Next.js)
```
src/
├── app/                 # Next.js app router pages
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components (Button, Card, etc.)
│   ├── layout/         # Layout components
│   ├── site/           # Site-specific components
│   ├── marketing/      # Marketing components
│   ├── media/          # Media components
│   └── icons/          # Icon components
├── lib/                # Utility libraries
│   └── api/            # API integration layer
└── styles/             # Global styles and themes
```

### Evolution-Content-Factory (Python)
```
Evolution-Content-Factory/
├── orchestrator/          # FastAPI backend (state machine API)
├── workers/               # Stateless containerized agents
│   ├── researcher/        # Scrapes racing data (Firecrawl)
│   ├── writer/            # Writes scripts (Gemini/Moonshot)
│   ├── clip-agent/        # Downloads YouTube segments
│   ├── editor/            # Renders video (FFmpeg NVENC)
│   └── voice-agent/       # Generates voiceover (Kokoro/ElevenLabs)
├── frontend/              # Next.js dashboard (Phase 6)
├── assets/                # Storage
│   ├── broll/             # B-roll library
│   ├── clips/             # Downloaded YouTube segments
│   ├── renders/           # Final video outputs
│   └── templates/         # Video composition templates
└── docker-compose.yml     # Local stack orchestration
```

### Evolution-Content-Builder (React + Python)
```
Evolution-Content-Builder/
├── app.py                 # Main FastAPI application
├── seek_app.py            # Seek app for content search
├── backend/               # Backend logic
│   ├── core/             # Core functionality
│   ├── google_seek/      # Google Seek integration
│   ├── rag/              # RAG system
│   └── web/              # Web endpoints
├── builder-ui/            # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── lib/          # Utility functions
│   │   └── types/        # TypeScript types
│   └── public/           # Static assets
├── config/                # Configuration files
│   ├── schemas/          # JSON schemas
│   └── tone_guidelines.md # Tone guidelines
├── docs/                  # Documentation
├── lib/                   # Helper libraries
│   ├── prompts.py        # AI prompts
│   └── studio.py         # Studio integration
├── scripts/               # Helper scripts
├── assets/                # Media assets
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

### evolution-studios-engine (Monorepo)
```
evolution-studios-engine/
├── apps/                  # Frontend applications
│   ├── owners/           # Owner dashboard
│   ├── studio/           # Content studio
│   └── valuation/        # Valuation calculator
├── services/             # Backend services
│   ├── enrich-svc/       # Content enrichment
│   ├── orchestrator/     # Job orchestration
│   ├── refiner/          # Content refinement
│   ├── scraper/          # Web scraping
│   └── transcriber/      # Audio transcription
├── database/             # Database migrations
│   └── migrations/       # SQL migrations
├── docker-compose.yml    # Docker configuration
├── package.json          # Dependencies (Turbo monorepo)
└── turbo.json            # Turbo configuration
```

## Content System Patterns

### Block-Based Content (Press Room)
The `press_room.py` module in Content Factory implements a linear block-based content system:

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

### Content Block Structure
```json
{
  "type": "grey_box",
  "content": "",
  "media": "https://youtube.com/watch?v=...",
  "quote": "— Trainer quote",
  "name": "Trainer Name"
}
```

## FFmpeg Patterns

### Ken Burns Effect
Used in `generate_ken_burns_batch.sh` to create zoom/pan effects on static images:
```bash
ffmpeg -loop 1 -i input.jpg \
  -vf "scale=1920:1080,zoompan=z='min(zoom+0.001,1.5)':x='iw/2-(iw*zoom)/2':y='ih/2-(ih*zoom)/2':d=125" \
  -c:v libx264 -t 5 -pix_fmt yuv420p output.mp4
```

### Video Composition
Used in `auto_reel_builder.py` and `test_reel_pipeline.py`:
- Concatenating clips
- Adding overlays (lower thirds, badges)
- Adding audio (voiceover + background music)
- Adjusting speed and transitions

## ComfyUI Workflow Patterns

### AI Image Generation
Custom workflows for horse racing imagery:
- **Horse Portraits**: Generating realistic horse images
- **Race Scenes**: Creating dynamic race day scenes
- **B-Roll**: Generating cinematic footage for reels

### Common Nodes
- Checkpoint Loader (Realistic Vision 5.1)
- VAE Loader (vae-ft-mse-840000-ema-pruned.ckpt)
- ControlNet (OpenPose for poses)
- Stable Diffusion Sampler (DPM++ 2M Karras)

## 70-80-10 Asset Composition Rule
For video content:
- **70%**: Original/owned content (racing footage, training videos)
- **80%**: Licensed content (B-roll from partners)
- **10%**: AI-generated content (for unique visuals)

## Project Connection Patterns

### Data Flow
```
Research Engine → Content Factory → Social Media → Website → Waitlist → Syndication
```

1. **Research Engine** scrapes racing data from NZTR, Racing.com, TAB
2. **Content Factory** generates video content using research data
3. **Social Media** distributes content to build audience
4. **Website** (Evolution-3.1) converts audience to waitlist
5. **Syndication Platform** manages ownership shares

### API Integration
- **Evolution-Research-Engine** exposes FastAPI endpoints at `http://localhost:8001`
- **Evolution-Content-Factory** orchestrator runs at `http://localhost:8000`
- **Evolution-3.1** uses API routes to communicate with backend services

## n8n Automation Patterns

### Stable Scout Asset Gen Workflow
```json
{
  "name": "Stable Scout Asset Gen",
  "nodes": [
    {
      "type": "webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "stable-scout"
      }
    },
    {
      "type": "executeCommand",
      "parameters": {
        "command": "/home/node/.n8n/mcp_proxy.sh \"{{ $json.horse }} at {{ $json.meeting }}\""
      }
    },
    {
      "type": "webhookResponse"
    }
  ]
}
```
- Triggered by webhook with horse and meeting data
- Executes MCP proxy to generate assets
- Responds with success/failure
