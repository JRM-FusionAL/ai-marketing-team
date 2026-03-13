# AI Marketing Team

A complete AI-powered marketing department built on Claude Opus 4.6. Six specialized agents collaborate to produce full marketing campaigns — strategy, SEO, copy, social, email, and analytics.

## Team Members

| Agent | Name | Specialties |
|-------|------|-------------|
| 📊 CMO | Alex Rivera | Strategy, positioning, channel mix, KPIs |
| 🔍 SEO | Sam Chen | Keywords, content briefs, technical SEO |
| ✍️ Copywriter | Jordan Hayes | Landing pages, ads, taglines, brand voice |
| 📱 Social | Morgan Lee | LinkedIn, Instagram, TikTok, X, content calendars |
| 📧 Email | Casey Martinez | Sequences, newsletters, deliverability |
| 📈 Analyst | Taylor Kim | KPIs, A/B testing, attribution, dashboards |

## Setup

```bash
cd ai-marketing-team
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## Usage

```bash
# See the team
python main.py team

# Full campaign (all 6 agents)
python main.py campaign --product "your product or service"

# Quick campaign (CMO + Copywriter only)
python main.py campaign --product "your product" --mode quick

# Full campaign with extra context
python main.py campaign --product "B2B SaaS for HR teams" --context "Targeting mid-market companies, 200-2000 employees"

# Save outputs to campaigns/ folder
python main.py campaign --product "your product" --save

# Ask a specific agent directly
python main.py ask cmo "What channels should a new SaaS product focus on?"
python main.py ask copy "Write 5 headline variations for a project management tool"
python main.py ask seo "What keywords should we target for email automation software?"
python main.py ask social "Create a LinkedIn post announcing our product launch"
python main.py ask email "Write a subject line for a re-engagement campaign"
python main.py ask analyst "What A/B tests should we run first for a new landing page?"

# View platform integrations
python main.py platforms
```

## Platform Integrations

Copy `.env.example` to `.env` and add API keys to activate:

- **HubSpot** — CRM, email campaigns, landing pages
- **Mailchimp / Klaviyo** — Email marketing
- **Buffer** — Social media scheduling
- **Semrush** — Keyword data and competitive research
- **Google Analytics 4** — Web analytics

## Architecture

```
main.py                 # CLI + orchestrator
agents/
  base.py              # Base agent class (Claude API streaming)
  cmo.py               # Campaign strategy
  copywriter.py        # Copy + content
  seo.py               # SEO strategy
  social.py            # Social media
  email_marketer.py    # Email sequences
  analyst.py           # Analytics + measurement
tools/
  platform_tools.py    # Marketing platform integrations
campaigns/             # Saved campaign outputs
```

Each agent runs Claude Opus 4.6 with adaptive thinking, streaming responses, and a specialized system prompt. The CMO runs first and each subsequent agent receives the previous agents' outputs as context — simulating a real marketing team handoff.
