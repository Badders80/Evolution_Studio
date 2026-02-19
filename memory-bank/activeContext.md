# Evolution Stables - Active Context

## Current Development Phase

### Evolution-3.1 (Frontend)
- **Phase**: Foundation + Content Integration
- **Current State**: Fully functional public website with:
  - Home page with hero section and features
  - Marketplace page for syndication offerings
  - My Stable page for owner dashboard
  - Press Room for news and updates
  - Valuation tool for horse valuation
- **Next Build Target**: Integrate with Content Factory for dynamic content

### Evolution-Content-Factory (Video Pipeline)
- **Phase**: AI-Native Content Pipeline
- **Current State**: Fully functional pipeline with:
  - Orchestrator API (FastAPI)
  - Worker services (Researcher, Writer, Clip Agent, Editor, Voice Agent)
  - FFmpeg video rendering with NVENC support
  - Asset library management
- **Next Build Target**: Improve b-roll generation and automation

### Evolution-Research-Engine (Data Layer)
- **Phase**: Scraper Implementation
- **Current State**: Scaffolded with FastAPI endpoints and mock data
- **Next Build Target**: Implement actual scraping for NZTR, Racing.com, TAB

### Evolution-Content-Builder (AI Content Generation)
- **Phase**: Production Ready (Phase 1)
- **Current State**: AI-powered content generation platform with:
  - Google Generative AI integration
  - Vertex AI Search for RAG
  - React frontend with device preview
  - Whisper for audio transcription
- **Next Build Target**: Integrate with Evolution-3.1 for content display

### evolution-studios-engine (Full Stack Platform)
- **Phase**: Integration Complete
- **Current State**: Monorepo with apps (owners, studio, valuation) and services (orchestrator, scraper, transcriber)
- **Next Build Target**: Migrate to production environment

### Brand_Voice (Brand Guidelines)
- **Phase**: Foundation Layer
- **Current State**: Contains brand voice and messaging guidelines
- **Next Build Target**: Integrate with all content generation tools

### Local_LLM (Local LLM Integration)
- **Phase**: Scaffolded
- **Current State**: Local LLM integration with Ollama and LlamaCPP
- **Next Build Target**: Implement real LLM integration

### evolution-email-builder (Email Marketing)
- **Phase**: Scaffolded
- **Current State**: Email marketing tool with drag-and-drop builder
- **Next Build Target**: Implement real email builder and sending functionality

## Recent Development Activity

### Last 5 Commits - Evolution-3.1
1. **ab15e68e** - feat(content-factory): Add Evolution Content Factory v3.0 (Feb 17, 2026)
2. **e0d86aa9** - feat: pnpm + SEO/perf foundation (no visual changes) (Feb 13, 2026)
3. **061cee34** - feat: institutionalised SEO and waitlist foundation (Feb 13, 2026)
4. **8eaf65f1** - Fix merge conflict in page.tsx (Feb 13, 2026)
5. **3e092bb1** - feat: SEO audit implementation and enhancements (Feb 13, 2026)

### Last 5 Commits - Evolution-Content-Factory
1. **bc3c70d** - feat: Integrate Evolution Studio components (Feb 19, 2026)
2. **b894200** - feat: B-Roll Library with Ken Burns + Veo 3 (Feb 19, 2026)
3. **4b25ab4** - feat: Smart AI-Native Content Pipeline (Feb 19, 2026)
4. **08c50b2** - docs: add README, design specs, and build scripts (Feb 18, 2026)
5. **eea904e** - feat: Evolution Content Factory v3.0 (Feb 18, 2026)

### Last 2 Commits - Evolution-Research-Engine
1. **e68173d** - feat: Research Engine implementation (Feb 19, 2026)
2. **3c99f14** - feat: Evolution Research Engine - Initial scaffold (Feb 19, 2026)

### Last 5 Commits - Evolution-Content-Builder
1. **[commit hash]** - feat: Add Google Generative AI integration (Feb 2026)
2. **[commit hash]** - feat: Implement Vertex AI Search for RAG (Feb 2026)
3. **[commit hash]** - feat: Add React frontend with device preview (Feb 2026)
4. **[commit hash]** - feat: Implement Whisper for audio transcription (Feb 2026)
5. **[commit hash]** - feat: Add ComfyUI integration (Feb 2026)

### Last 5 Commits - evolution-studios-engine
1. **[commit hash]** - feat: Add owner dashboard (Feb 2026)
2. **[commit hash]** - feat: Implement content studio (Feb 2026)
3. **[commit hash]** - feat: Add valuation calculator (Feb 2026)
4. **[commit hash]** - feat: Implement orchestrator service (Feb 2026)
5. **[commit hash]** - feat: Add scraper and transcriber services (Feb 2026)

## Recent AI Contributions

### Clawbot/Kilo Activity
- **Evolution-3.1**: Implemented SEO foundation, waitlist system, and content-factory integration
- **Evolution-Content-Factory**: Built AI-native pipeline with workers, FFmpeg integration, and asset management
- **Evolution-Research-Engine**: Scaffolded FastAPI endpoints and scraper architecture
- **Evolution-Content-Builder**: Implemented Google Generative AI and Vertex AI Search integration
- **evolution-studios-engine**: Built full stack platform with apps and services
- **CLAUDE.md Files**: Created CLAUDE.md files for all repos

### Kilo Contributions Today
- **CLAUDE.md Generation**: Created CLAUDE.md files for all repos (10 in total)
- **00_DNA Integration**: Updated all CLAUDE.md files to reference 00_DNA
- **Memory Bank Updates**: Updated projectBrief.md, techContext.md, systemPatterns.md, activeContext.md
- **EVOLUTION_MASTER_CONTEXT.md**: Created master context file with all repos and key information

## Known Issues and Gaps

### Evolution-3.1
- No direct integration with Content Factory for dynamic content
- Limited horse profile data (mock data only)
- No user authentication for owner dashboard

### Evolution-Content-Factory
- Scraper worker (Firecrawl) not fully implemented
- Voice agent needs better error handling
- Video rendering could be optimized for GPU

### Evolution-Research-Engine
- All scrapers are mock implementations (no real data fetching)
- No social intelligence monitoring (TikTok/Instagram trends)
- API endpoints not documented

### Evolution-Content-Builder
- Need to test audio transcription with real files
- Need to optimize RAG system performance
- Need to integrate with Evolution-3.1

### evolution-studios-engine
- Need to test all services together
- Need to optimize frontend performance
- Need to integrate with Supabase

### Brand_Voice
- Need to update brand guidelines with new content types
- Need to integrate with all content generation tools

### Local_LLM
- Need to implement real LLM integration
- Need to test with various quantized models

### evolution-email-builder
- Need to implement real email builder and sending functionality
- Need to integrate with SendGrid

## Open Architectural Decisions

### Merge Content Factory into Studio vs Separate
- **Current Status**: Separate repos
- **Pros of Separate**: Focused codebase, easier deployment
- **Pros of Merge**: Unified architecture, better integration
- **Decision**: TBD - currently maintaining separate repos

### Database Choice for Research Engine
- **Current Status**: Supabase (PostgreSQL)
- **Options**: Supabase vs. Local SQLite vs. MongoDB
- **Decision**: Supabase for now (scalable, managed)

### LLM Provider
- **Current Status**: Gemini API
- **Options**: OpenAI vs. Gemini vs. Moonshot
- **Decision**: Gemini for now (Google ecosystem integration)
