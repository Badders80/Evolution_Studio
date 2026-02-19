# Evolution Stables - Machine Context

## WSL2 Configuration
- **WSL Version**: WSL2 Ubuntu
- **Windows Host**: Windows 10/11
- **Home Directory**: `/home/evo/`

## Project Mount Points
### Evolution-3.1 (Frontend)
- **WSL2 Path**: `/home/evo/projects/Evolution-3.1/`
- **Windows Path**: `C:\Users\Evo\projects\Evolution-3.1\`
- **Port**: 3000

### Evolution-Content-Factory (Video Pipeline)
- **WSL2 Path**: `/home/evo/projects/Evolution-Content-Factory/`
- **Windows Path**: `C:\Users\Evo\projects\Evolution-Content-Factory\`
- **Ports**:
  - Orchestrator: 8000
  - Workers: Docker internal (not exposed)

### Evolution-Research-Engine (Data Layer)
- **WSL2 Path**: `/home/evo/projects/Evolution-Research-Engine/`
- **Windows Path**: `C:\Users\Evo\projects\Evolution-Research-Engine\`
- **Port**: 8001

### Other Projects
- **Asset_Generation**: `/home/evo/projects/Asset_Generation/`
- **ComfyUI**: `/home/evo/projects/ComfyUI/` (Port 8188)
- **n8n**: `/home/evo/projects/n8n/` (Port 5678)
- **04_Intelligence**: `/home/evo/projects/04_Intelligence/`
- **Evolution-Content-Builder**: `/home/evo/projects/Evolution-Content-Builder/` (Port 8000)
- **evolution-studios-engine**: `/home/evo/projects/evolution-studios-engine/` (Port 3000)
- **Brand_Voice**: `/home/evo/projects/Brand_Voice/`
- **Local_LLM**: `/home/evo/projects/Local_LLM/` (Port 8002)
- **evolution-email-builder**: `/home/evo/projects/evolution-email-builder/` (Port 5174)
- **evolution-studio-mcp**: `/home/evo/projects/evolution-studio-mcp/`
- **firecrawl**: `/home/evo/projects/firecrawl/`

## GPU Configuration
- **GPU Model**: NVIDIA RTX 3060 12GB
- **CUDA Version**: 12.x (via WSL2 NVIDIA CUDA support)
- **GPU Allocation**:
  - ComfyUI: Uses CUDA for AI image generation
  - FFmpeg: Can use NVENC for GPU-accelerated encoding
  - llama.cpp: Uses CPU (can be configured for GPU)

## CPU Configuration
- **CPU Model**: AMD Ryzen (WSL2 virtualized)
- **Cores**: 8 (allocated from Windows)
- **RAM**: 16GB (allocated from Windows)

## Storage Configuration
### Primary Storage
- **WSL2 Root**: `/home/evo/` - SSD
- **Projects Directory**: `/home/evo/projects/` - SSD

### Large File Storage
- **Scratch Space**: `/mnt/scratch/` - HDD (for large video files)
- **Assets Directory**: `/home/evo/projects/Evolution-Content-Factory/assets/` - SSD

## Docker Containers
### Running Containers (via docker-compose)
```
evo-orchestrator      Up       0.0.0.0:8000->8000/tcp
evo-researcher        Up       0.0.0.0:8001->8001/tcp
evo-writer            Up
evo-clip-agent        Up
evo-editor            Up
evo-voice-agent       Up
```

### Container Details
- **evostables_orchestrator**: FastAPI API server
- **evostables_researcher**: Web scraping service
- **evostables_writer**: Script generation service
- **evostables_clip-agent**: YouTube clip downloader
- **evostables_editor**: FFmpeg video renderer
- **evostables_voice-agent**: ElevenLabs voiceover service

## Background Services
### cron Jobs
- No active cron jobs configured

### System Services
- **Docker Engine**: Running (WSL2 integration)
- **n8n**: Running on port 5678
- **ComfyUI**: Running on port 8188

## Environment Variables
### Global Variables
- **WSL2_DISTRO_NAME**: Ubuntu
- **PATH**: `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Windows/System32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0:/mnt/c/Windows/System32/OpenSSH`

### Project-Specific Variables
- **Evolution-3.1**: `.env.local` (not committed to git)
- **Evolution-Content-Factory**: `.env` (contains API keys)
- **Evolution-Research-Engine**: `config/` directory

## Network Configuration
- **WSL2 Network**: NAT with Windows host
- **Host Access**: http://localhost:<port> from Windows browser
- **Container Network**: evo-network (Docker bridge network)

## Security
- **Firewall**: Windows Firewall configured to allow WSL2 ports
- **API Keys**: Stored in .env files (not committed to git)
- **Docker Containers**: Running in bridge network with limited exposure
