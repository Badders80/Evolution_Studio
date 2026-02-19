# Evolution Stables - Project Brief

## Business Context
Evolution Stables is building a digital syndication platform for horse racing ownership. The platform aims to democratize access to horse racing investments by allowing users to own fractional shares of racehorses. Key markets include New Zealand, Dubai, and Hong Kong.

## Evolution_Studio (Django Application) - `/home/evo/projects/Evolution_Studio/`
Evolution_Studio is the Django-based content management system for Evolution Stables. It provides a Streamlit interface for creating and managing press updates, with a block-based content system. Key features:
- Streamlit interface for content creation
- Block-based editor (heading, subheading, body, bullets, grey box)
- HTML generation with responsive design
- Django ORM for content storage
- Media asset management

## Evolution-3.1 (Frontend) - `/home/evo/projects/Evolution-3.1/`
Evolution-3.1 is the frontend web application for Evolution Stables. It's built with Next.js 14, TypeScript, Tailwind CSS, and Framer Motion. The application serves as the public-facing website, providing information about the platform, horse profiles, race updates, and the syndication model.

## Project Ecosystem Map
### Core Projects:
1. **Evolution_Studio** (Content Management) - `/home/evo/projects/Evolution_Studio`
   - Django-based content management system
   - Streamlit interface for creating press updates
   - Block-based editor (heading, subheading, body, bullets, grey box)
   - HTML generation with responsive design

2. **Evolution-3.1** (Frontend) - `/home/evo/projects/Evolution-3.1`
   - Next.js 14 web application
   - Public website with horse profiles, race updates, and syndication information
   - Key features: Marketplace, My Stable, Press Room, Valuation tool

3. **Evolution-Content-Factory** (Video Pipeline) - `/home/evo/projects/Evolution-Content-Factory`
   - AI-powered TikTok/Reels content generation pipeline
   - Components: Orchestrator (FastAPI), Researcher, Writer, Clip Agent, Editor, Voice Agent
   - Uses: FFmpeg for video editing, Gemini for script writing, ElevenLabs for voiceovers

4. **Evolution-Research-Engine** (Data Layer) - `/home/evo/projects/Evolution-Research-Engine`
   - FastAPI-based research and scraping engine
   - Scrapes racing data from NZTR, Racing.com, TAB
   - Provides API endpoints for content generation and social intelligence

### Supporting Projects:
1. **Asset_Generation** - `/home/evo/projects/Asset_Generation`
   - Image and video asset generation
   - Integrates with ComfyUI for AI-generated content
   - Reel factory for video editing

2. **ComfyUI** - `/home/evo/projects/ComfyUI`
   - AI image generation tool
   - Custom workflows for horse racing-related imagery

3. **n8n** - `/home/evo/projects/n8n`
   - Automation tool for workflow management
   - Stable Scout Asset Gen workflow for automated asset generation

4. **04_Intelligence** - `/home/evo/projects/04_Intelligence`
   - Local LLM server (llama.cpp) for offline processing
   - GLM-4 model for Chinese language tasks

5. **Evolution-Content-Builder** - `/home/evo/projects/Evolution-Content-Builder`
   - AI content generation platform
   - Uses Google Generative AI and Vertex AI Search
   - React frontend with device preview

6. **evolution-studios-engine** - `/home/evo/projects/evolution-studios-engine`
   - Full stack platform with apps (owners, studio, valuation)
   - Services: orchestrator, scraper, transcriber, refiner, enrich-svc

7. **Brand_Voice** - `/home/evo/projects/Brand_Voice`
   - Brand voice and messaging guidelines
   - Contains 00_kernel, 01_modules, 02_logic structure
   - Brand Bible v2.2 Nov 2025

8. **Local_LLM** - `/home/evo/projects/Local_LLM`
   - Local LLM integration (Ollama + LlamaCPP)
   - Hybrid LLM orchestrator with Groq + Gemini watchdog

9. **evolution-email-builder** - `/home/evo/projects/evolution-email-builder`
   - Email marketing tool with drag-and-drop builder
   - Integrates with SendGrid for email delivery

10. **evolution-studio-mcp** - `/home/evo/projects/evolution-studio-mcp`
    - MCP server for integration with AI agents
    - Contains vault query and workflow listing tools

11. **firecrawl** - `/home/evo/projects/firecrawl`
    - Web scraping tool using Firecrawl API
    - Monorepo with API, JS SDK, Python SDK, Rust SDK

## Platform Vision
The platform is being built toward a comprehensive horse racing ownership ecosystem that includes:
- Fractional ownership of racehorses
- Real-time race updates and data
- AI-generated content for social media
- Syndication management tools
- Valuation and analytics dashboards

The current focus is on building the content generation pipeline (Content Factory) to drive audience growth through social media, following the "Fight Club" funnel strategy (build audience before revealing ownership model).
