# Evolution Stables - Tech Context

## Tools and Frameworks Installed
### Frontend
- **Next.js 14** with App Router (Evolution-3.1, evolution-studios-engine)
- **Streamlit** for content management interface (Evolution_Studio)
- **React + TypeScript + Vite** for content builder (Evolution-Content-Builder)
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **NextAuth.js** for authentication

### Backend
- **Django 4.x** for content management (Evolution_Studio)
- **FastAPI** for API development (Content Factory, Research Engine)
- **Python 3.12** for backend services
- **Supabase** for database and authentication
- **SQLite** for local development (Evolution_Studio)
- **Docker** for containerization

### AI/LLM
- **Gemini API** for content generation (Evolution_Content_Builder)
- **Moonshot API** for Chinese language tasks
- **ElevenLabs** for voiceovers (Evolution_Content_Factory)
- **llama.cpp** with GLM-4 model for local processing (04_Intelligence)
- **Ollama** for local LLM integration (Local_LLM)
- **LlamaCPP** for quantized models (Local_LLM)
- **Google Generative AI** for content creation (Evolution_Content_Builder)
- **Vertex AI Search** for RAG (Evolution_Content_Builder)
- **ComfyUI** for AI image generation

### Data and Scraping
- **Requests + BeautifulSoup4** for web scraping
- **Firecrawl** for automated web crawling
- **Supabase** for data storage

### Video Processing
- **FFmpeg** for video editing and processing (Evolution_Content_Factory)
- **NVENC** for GPU-accelerated video encoding
- **Kohya LoRA** for model training (Evolution_Content_Builder)

### Automation
- **n8n** for workflow automation
- **Cron** for scheduled tasks
- **Turbo** for monorepo management (evolution-studios-engine)

## Hardware Configuration
- **GPU**: RTX 3060 12GB
- **CPU**: Ryzen (WSL2 Ubuntu)
- **RAM**: 16GB+ (WSL2 allocation)
- **Storage**: /mnt/scratch for large files, /home/evo/projects for code

## GPU Allocation
- **ComfyUI**: Uses RTX 3060 for AI image generation
- **FFmpeg**: Uses CPU for video processing (can use GPU with NVENC)
- **llama.cpp**: Uses CPU (can be configured for GPU)

## WSL2 Path Translations
- **Windows Path**: `C:\Users\Evo\` → **WSL2 Path**: `/mnt/c/Users/Evo/`
- **Projects Directory**: `/home/evo/projects/` (WSL2) → Accessible from Windows

## Explicitly Not Used
### Frameworks
- **Django**: Not used (Evolution-3.1 is Next.js, not Django)
- **Scrapy/Selenium**: Not used for scraping (Requests + BeautifulSoup preferred)
- **OpenAI**: Not used (Gemini API preferred)

### Reasoning
- **Django vs Next.js**: Frontend-focused application, Next.js provides better SEO and performance
- **Scraping Tools**: Simple requests + BeautifulSoup is sufficient for racing data
- **LLM Choice**: Gemini API provides better integration with Google ecosystem

## Environment Setup Patterns
### .env Files
- **Evolution-3.1**: `.env.local` for local development
- **Evolution-Content-Factory**: `.env` for pipeline configuration
- **Evolution-Research-Engine**: `config/` directory for API keys

### Environment Variables
- **Supabase**: URL and Anon Key for database access
- **Gemini API Key**: For content generation
- **ElevenLabs API Key**: For voiceovers
- **Firecrawl API Key**: For web crawling

## Configured Services
- **Supabase**: Database and authentication
- **Gemini API**: Content generation
- **ElevenLabs**: Voiceovers
- **Firecrawl**: Web scraping
- **Moonshot API**: Chinese language tasks
- **SendGrid**: Email delivery (evolution-email-builder)
- **Google Cloud**: AI and search services (Evolution_Content_Builder)
