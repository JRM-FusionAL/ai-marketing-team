"""
AI Marketing Team — Multi-Agent Orchestrator
============================================
A complete AI marketing team powered by Claude Opus 4.6.

Each specialist agent runs sequentially, building on the previous agent's output,
simulating how a real marketing team collaborates on a campaign.

Usage:
    python main.py                          # Interactive mode
    python main.py --product "your product" # Single campaign run
    python main.py --mode full              # Run all 6 agents
    python main.py --mode quick             # CMO + Copywriter only
    python main.py --save                   # Save outputs to campaigns/
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv

# Force UTF-8 output on Windows
import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

load_dotenv()

from agents import (
    create_cmo,
    create_copywriter,
    create_seo_specialist,
    create_social_manager,
    create_analyst,
    create_email_marketer,
)

app = typer.Typer(help="AI Marketing Team — your on-demand marketing department")
console = Console(force_terminal=True)


# ──────────────────────────────────────────────
# Campaign Runner
# ──────────────────────────────────────────────

class MarketingTeam:
    """Orchestrates the full marketing team workflow."""

    def __init__(self, save_outputs: bool = False):
        self.save_outputs = save_outputs
        self.outputs: dict[str, str] = {}
        self.agents = {
            "cmo": create_cmo(),
            "copywriter": create_copywriter(),
            "seo": create_seo_specialist(),
            "social": create_social_manager(),
            "analyst": create_analyst(),
            "email": create_email_marketer(),
        }

    def _save(self, campaign_name: str):
        """Save all outputs to a campaign folder."""
        slug = campaign_name.lower().replace(" ", "-")[:40]
        ts = datetime.now().strftime("%Y%m%d-%H%M")
        folder = Path("campaigns") / f"{ts}-{slug}"
        folder.mkdir(parents=True, exist_ok=True)

        for role, content in self.outputs.items():
            (folder / f"{role}.md").write_text(content, encoding="utf-8")

        summary = {
            "campaign": campaign_name,
            "generated_at": datetime.now().isoformat(),
            "agents_used": list(self.outputs.keys()),
        }
        (folder / "summary.json").write_text(json.dumps(summary, indent=2))

        console.print(f"\n[green]✓ Campaign saved to:[/green] [bold]{folder}[/bold]")

    def run_full_campaign(self, product: str, extra_context: str = "") -> dict[str, str]:
        """
        Run the full 6-agent marketing campaign pipeline.

        Flow:
          CMO → Strategy brief
          SEO → Keyword & content strategy (uses CMO brief)
          Copywriter → Landing page + ad copy (uses CMO + SEO)
          Social → Platform content calendar (uses CMO + Copy)
          Email → Nurture sequence (uses CMO + Copy)
          Analyst → Metrics framework (uses everything)
        """
        base_info = f"Product/Service: {product}"
        if extra_context:
            base_info += f"\n\nAdditional context: {extra_context}"

        console.print(Panel(
            f"[bold green]Launching AI Marketing Team[/bold green]\n"
            f"Product: [cyan]{product}[/cyan]\n"
            f"Agents: CMO → SEO → Copywriter → Social → Email → Analyst",
            title="🚀 Campaign Start",
            border_style="green",
        ))

        # 1. CMO — Campaign strategy
        cmo_task = f"""Create a comprehensive marketing campaign brief for:

{base_info}

Include: campaign objective, target personas, positioning, messaging pillars, channel mix, and KPIs."""
        self.outputs["01_cmo_strategy"] = self.agents["cmo"].think(cmo_task)

        # 2. SEO — Keyword & content strategy
        seo_task = f"""Based on the campaign brief, create a detailed SEO strategy for:

{base_info}

Provide: keyword clusters (primary/secondary/long-tail), search intent analysis, content brief for the top 3 priority pages, and technical SEO checklist."""
        self.outputs["02_seo_strategy"] = self.agents["seo"].think(
            seo_task, context=self.outputs["01_cmo_strategy"]
        )

        # 3. Copywriter — Hero copy, landing page, ads
        copy_task = f"""Write conversion-optimized copy for:

{base_info}

Deliver:
1. Hero section copy (headline, subheadline, CTA)
2. Full landing page copy (problem → solution → features → social proof → CTA)
3. 3 Google Search ad variations (headlines + descriptions)
4. 3 Meta/Facebook ad variations (primary text + headline + CTA)
5. A tagline and brand voice guide (3-5 sentences)"""
        self.outputs["03_copywriter"] = self.agents["copywriter"].think(
            copy_task,
            context=self.outputs["01_cmo_strategy"] + "\n\n" + self.outputs["02_seo_strategy"],
        )

        # 4. Social Media — Content calendar
        social_task = f"""Create a 4-week social media content calendar for:

{base_info}

Include ready-to-post content for:
- LinkedIn (3x/week): thought leadership, company posts, engagement posts
- Instagram (4x/week): caption + hashtags + creative brief
- X/Twitter (5x/week): standalone tweets + thread concept
- TikTok/Reels (2x/week): video concept, hook, script outline

Also include: influencer outreach strategy and community management guidelines."""
        self.outputs["04_social"] = self.agents["social"].think(
            social_task,
            context=self.outputs["01_cmo_strategy"] + "\n\n" + self.outputs["03_copywriter"],
        )

        # 5. Email — Nurture sequence
        email_task = f"""Create a complete email marketing program for:

{base_info}

Deliver:
1. Welcome sequence (5 emails) — for new subscribers/leads
2. Sales sequence (3 emails) — for bottom-of-funnel leads
3. Re-engagement sequence (2 emails) — for cold subscribers
4. Monthly newsletter template

For each email include: subject line (3 variations), preview text, full body copy, CTA, and estimated performance benchmarks."""
        self.outputs["05_email"] = self.agents["email"].think(
            email_task,
            context=self.outputs["01_cmo_strategy"] + "\n\n" + self.outputs["03_copywriter"],
        )

        # 6. Analyst — Measurement framework
        analyst_task = f"""Build a complete marketing measurement framework for:

{base_info}

Provide:
1. KPI dashboard (metric, target, measurement method, tool)
2. Attribution model recommendation
3. A/B testing roadmap (top 5 tests to run first)
4. Monthly reporting template
5. 90-day performance benchmarks and optimization triggers"""
        full_context = "\n\n---\n\n".join([
            self.outputs["01_cmo_strategy"],
            self.outputs["02_seo_strategy"],
            self.outputs["04_social"],
        ])
        self.outputs["06_analytics"] = self.agents["analyst"].think(
            analyst_task, context=full_context
        )

        if self.save_outputs:
            self._save(product)

        self._print_summary()
        return self.outputs

    def run_quick_campaign(self, product: str) -> dict[str, str]:
        """CMO strategy + copywriter only — fast campaign start."""
        console.print(Panel(
            f"[bold yellow]Quick Campaign Mode[/bold yellow]\n"
            f"Product: [cyan]{product}[/cyan]\n"
            f"Agents: CMO + Copywriter",
            title="⚡ Quick Start",
            border_style="yellow",
        ))

        base_info = f"Product/Service: {product}"

        cmo_task = f"Create a marketing campaign brief for: {base_info}"
        self.outputs["01_cmo_strategy"] = self.agents["cmo"].think(cmo_task)

        copy_task = f"""Write hero copy, landing page copy, and 3 ad variations for: {base_info}"""
        self.outputs["03_copywriter"] = self.agents["copywriter"].think(
            copy_task, context=self.outputs["01_cmo_strategy"]
        )

        if self.save_outputs:
            self._save(product)

        return self.outputs

    def ask_agent(self, agent_name: str, question: str, context: str = "") -> str:
        """Ask a specific agent a question directly."""
        agent_map = {
            "cmo": "cmo", "chief": "cmo", "strategy": "cmo",
            "copy": "copywriter", "writer": "copywriter",
            "seo": "seo", "search": "seo",
            "social": "social", "instagram": "social", "linkedin": "social",
            "email": "email", "mail": "email",
            "analyst": "analyst", "analytics": "analyst", "data": "analyst",
        }
        key = agent_map.get(agent_name.lower(), agent_name.lower())
        if key not in self.agents:
            console.print(f"[red]Unknown agent: {agent_name}[/red]")
            console.print(f"Available: {', '.join(self.agents.keys())}")
            return ""
        return self.agents[key].think(question, context=context)

    def _print_summary(self):
        table = Table(title="Campaign Deliverables", border_style="green")
        table.add_column("Agent", style="cyan")
        table.add_column("Deliverable", style="white")
        table.add_column("File", style="dim")

        deliverables = [
            ("📊 CMO", "Campaign strategy + brief", "01_cmo_strategy.md"),
            ("🔍 SEO", "Keyword research + content briefs", "02_seo_strategy.md"),
            ("✍️ Copywriter", "Landing page + ad copy", "03_copywriter.md"),
            ("📱 Social", "4-week content calendar", "04_social.md"),
            ("📧 Email", "Welcome + nurture sequences", "05_email.md"),
            ("📈 Analyst", "KPI dashboard + A/B roadmap", "06_analytics.md"),
        ]
        for agent, deliverable, file in deliverables:
            if any(file.split(".")[0] in k for k in self.outputs.keys()):
                table.add_row(agent, deliverable, file)

        console.print("\n")
        console.print(table)


# ──────────────────────────────────────────────
# CLI Commands
# ──────────────────────────────────────────────

@app.command()
def campaign(
    product: str = typer.Option(None, "--product", "-p", help="Product or service to market"),
    mode: str = typer.Option("full", "--mode", "-m", help="full | quick"),
    save: bool = typer.Option(False, "--save", "-s", help="Save outputs to campaigns/"),
    context: str = typer.Option("", "--context", "-c", help="Additional context about your product"),
):
    """Run a full AI marketing team campaign."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not set.[/red]")
        console.print("Add it to a .env file or set it in your environment.")
        raise typer.Exit(1)

    if not product:
        product = Prompt.ask("[bold cyan]What product or service are you marketing?[/bold cyan]")

    team = MarketingTeam(save_outputs=save)

    if mode == "quick":
        team.run_quick_campaign(product)
    else:
        team.run_full_campaign(product, extra_context=context)


@app.command()
def ask(
    agent: str = typer.Argument(..., help="Agent to ask: cmo, copy, seo, social, email, analyst"),
    question: str = typer.Argument(..., help="Question to ask the agent"),
    context: str = typer.Option("", "--context", "-c", help="Additional context"),
):
    """Ask a specific marketing agent a question."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not set.[/red]")
        raise typer.Exit(1)

    team = MarketingTeam()
    team.ask_agent(agent, question, context=context)


@app.command()
def team():
    """Show the marketing team roster."""
    table = Table(title="🏢 AI Marketing Team", border_style="blue")
    table.add_column("Agent", style="cyan bold")
    table.add_column("Name", style="white")
    table.add_column("Role", style="yellow")
    table.add_column("Specialties", style="dim")

    members = [
        ("📊 CMO", "Alex Rivera", "Chief Marketing Officer", "Strategy, positioning, channel mix, KPIs"),
        ("🔍 SEO", "Sam Chen", "SEO Specialist", "Keywords, content briefs, technical SEO"),
        ("✍️ Copy", "Jordan Hayes", "Senior Copywriter", "Landing pages, ads, taglines, brand voice"),
        ("📱 Social", "Morgan Lee", "Social Media Manager", "LinkedIn, IG, TikTok, X, content calendars"),
        ("📧 Email", "Casey Martinez", "Email Marketing Specialist", "Sequences, newsletters, deliverability"),
        ("📈 Analyst", "Taylor Kim", "Marketing Analyst", "KPIs, A/B testing, attribution, dashboards"),
    ]
    for emoji_role, name, role, specs in members:
        table.add_row(emoji_role, name, role, specs)

    console.print(table)
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [cyan]python main.py campaign --product 'Your Product'[/cyan]  — Full campaign")
    console.print("  [cyan]python main.py campaign --mode quick[/cyan]               — Quick campaign")
    console.print("  [cyan]python main.py ask cmo 'What channels should I focus on?'[/cyan]")
    console.print("  [cyan]python main.py ask copy 'Write a headline for a B2B SaaS product'[/cyan]")
    console.print("  [cyan]python main.py ask seo 'Find keywords for project management software'[/cyan]")


@app.command()
def platforms():
    """Show available marketing platform integrations."""
    table = Table(title="🔌 Platform Integrations", border_style="magenta")
    table.add_column("Platform", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Env Variable", style="dim")
    table.add_column("Status", style="white")

    integrations = [
        ("HubSpot", "CRM + Email", "HUBSPOT_API_KEY", "✓ Ready (add key)"),
        ("Mailchimp", "Email", "MAILCHIMP_API_KEY", "✓ Ready (add key)"),
        ("Klaviyo", "Email", "KLAVIYO_API_KEY", "✓ Ready (add key)"),
        ("Buffer", "Social Scheduling", "BUFFER_API_KEY", "✓ Ready (add key)"),
        ("Semrush", "SEO Data", "SEMRUSH_API_KEY", "✓ Ready (add key)"),
        ("Google Analytics 4", "Analytics", "GOOGLE_APPLICATION_CREDENTIALS", "✓ Ready (add key)"),
        ("Meta Ads", "Paid Social", "META_ACCESS_TOKEN", "Coming soon"),
        ("Google Ads", "Paid Search", "GOOGLE_ADS_DEVELOPER_TOKEN", "Coming soon"),
    ]
    for platform, category, env_var, status in integrations:
        table.add_row(platform, category, env_var, status)

    console.print(table)
    console.print("\nAdd keys to [bold].env[/bold] in this directory to activate integrations.")


if __name__ == "__main__":
    app()
