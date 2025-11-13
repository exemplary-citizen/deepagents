"""Configuration, constants, and model creation for the CLI."""

import os
import sys
from pathlib import Path

import dotenv
from rich.console import Console

dotenv.load_dotenv()

# Color scheme
COLORS = {
    "primary": "#10b981",
    "dim": "#6b7280",
    "user": "#ffffff",
    "agent": "#10b981",
    "thinking": "#34d399",
    "tool": "#fbbf24",
}

# ASCII art banner
DEEP_AGENTS_ASCII = """
 ██████╗  ███████╗ ███████╗ ██████╗
 ██╔══██╗ ██╔════╝ ██╔════╝ ██╔══██╗
 ██║  ██║ █████╗   █████╗   ██████╔╝
 ██║  ██║ ██╔══╝   ██╔══╝   ██╔═══╝
 ██████╔╝ ███████╗ ███████╗ ██║
 ╚═════╝  ╚══════╝ ╚══════╝ ╚═╝

  █████╗   ██████╗  ███████╗ ███╗   ██╗ ████████╗ ███████╗
 ██╔══██╗ ██╔════╝  ██╔════╝ ████╗  ██║ ╚══██╔══╝ ██╔════╝
 ███████║ ██║  ███╗ █████╗   ██╔██╗ ██║    ██║    ███████╗
 ██╔══██║ ██║   ██║ ██╔══╝   ██║╚██╗██║    ██║    ╚════██║
 ██║  ██║ ╚██████╔╝ ███████╗ ██║ ╚████║    ██║    ███████║
 ╚═╝  ╚═╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝    ╚═╝    ╚══════╝
"""

# Interactive commands
COMMANDS = {
    "clear": "Clear screen and reset conversation",
    "help": "Show help information",
    "tokens": "Show token usage for current session",
    "quit": "Exit the CLI",
    "exit": "Exit the CLI",
}


# Maximum argument length for display
MAX_ARG_LENGTH = 150

# Agent configuration
config = {"recursion_limit": 1000}

# Rich console instance
console = Console(highlight=False)


class SessionState:
    """Holds mutable session state (auto-approve mode, etc)."""

    def __init__(self, auto_approve: bool = False) -> None:
        self.auto_approve = auto_approve
        self.exit_hint_until: float | None = None
        self.exit_hint_handle = None

    def toggle_auto_approve(self) -> bool:
        """Toggle auto-approve and return new state."""
        self.auto_approve = not self.auto_approve
        return self.auto_approve


def get_default_coding_instructions() -> str:
    """Get the default coding agent instructions.

    These are the immutable base instructions that cannot be modified by the agent.
    Long-term memory (agent.md) is handled separately by the middleware.
    """
    default_prompt_path = Path(__file__).parent / "default_agent_prompt.md"
    return default_prompt_path.read_text()


def create_model(
    *,
    model_override: str | None = None,
    provider_override: str | None = None,
    base_url_override: str | None = None,
    api_key_override: str | None = None,
):
    """Create the appropriate model based on available API keys.

    Returns:
        ChatModel instance (OpenAI or Anthropic)

    Raises:
        SystemExit if no API key is configured
    """
    openai_key_env = os.environ.get("OPENAI_API_KEY")
    anthropic_key_env = os.environ.get("ANTHROPIC_API_KEY")
    provider = None

    if provider_override:
        provider_candidate = provider_override.strip().lower()
        if provider_candidate not in {"openai", "anthropic"}:
            console.print(
                "[bold red]Error:[/bold red] Unsupported provider override "
                f"'{provider_override}'. Expected 'openai' or 'anthropic'."
            )
            sys.exit(1)
        provider = provider_candidate
    else:
        if base_url_override or api_key_override or openai_key_env:
            provider = "openai"
        elif anthropic_key_env:
            provider = "anthropic"

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        api_key = api_key_override or openai_key_env
        if api_key is None:
            console.print("[bold red]Error:[/bold red] No OpenAI-compatible API key configured.")
            console.print("\nProvide a key via one of the following methods:")
            console.print("  - Set OPENAI_API_KEY in your environment")
            console.print("  - Pass --api-key <key> on the CLI (optionally with --base-url)")
            console.print("\nTip: You can also run with --provider anthropic if you have that key configured.")
            sys.exit(1)

        model_name = model_override or os.environ.get("OPENAI_MODEL", "gpt-5-mini")
        base_url = base_url_override or os.environ.get("OPENAI_BASE_URL")
        if base_url:
            console.print(
                f"[dim]Using OpenAI-compatible model: {model_name}[/dim] "
                f"[dim](base_url={base_url})[/dim]"
            )
        else:
            console.print(f"[dim]Using OpenAI model: {model_name}[/dim]")

        kwargs = {
            "model": model_name,
            "temperature": 0.7,
            "api_key": api_key,
        }
        if base_url:
            kwargs["base_url"] = base_url

        return ChatOpenAI(**kwargs)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        anthropic_key = api_key_override or anthropic_key_env
        if anthropic_key is None:
            console.print("[bold red]Error:[/bold red] Anthropic provider selected but no API key configured.")
            console.print("Set ANTHROPIC_API_KEY or provide --api-key when selecting --provider anthropic.")
            sys.exit(1)

        model_name = model_override or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
        console.print(f"[dim]Using Anthropic model: {model_name}[/dim]")
        return ChatAnthropic(
            model_name=model_name,
            max_tokens=20000,
        )

    console.print("[bold red]Error:[/bold red] No API key configured.")
    console.print("\nPlease set one of the following environment variables:")
    console.print("  - OPENAI_API_KEY     (for OpenAI or any OpenAI-compatible model)")
    console.print("  - ANTHROPIC_API_KEY  (for Claude models)")
    console.print("\nExamples:")
    console.print("  export OPENAI_API_KEY=your_api_key_here")
    console.print(
        "  deepagents --provider openai --model meta/llama-3 --base-url https://your-host/api/v1 --api-key your_api_key_here"
    )
    console.print("\nOr add it to your .env file.")
    sys.exit(1)
