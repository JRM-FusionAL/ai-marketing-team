"""Base agent class for all marketing team members."""

import anthropic
from typing import Optional
from rich.console import Console

console = Console()
client = anthropic.Anthropic()
MODEL = "claude-opus-4-6"


class MarketingAgent:
    """Base class for all marketing agents."""

    def __init__(self, name: str, role: str, system_prompt: str, emoji: str = "🤖"):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.emoji = emoji

    def think(self, task: str, context: str = "", max_tokens: int = 4096) -> str:
        """Run the agent on a task, returning its response."""
        messages = [{"role": "user", "content": task}]
        if context:
            messages = [
                {"role": "user", "content": f"Context from previous team members:\n\n{context}\n\n---\n\nYour task: {task}"}
            ]

        console.print(f"\n[bold]{self.emoji} {self.name}[/bold] [{self.role}] is working...", style="cyan")

        full_text = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            system=self.system_prompt,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_text += text

        print("\n")
        return full_text

    def __repr__(self):
        return f"<{self.role}: {self.name}>"
