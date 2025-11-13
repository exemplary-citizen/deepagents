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
    model: str | None = None,
    provider: str | None = None,
    api_base: str | None = None,
    api_key: str | None = None,
):
    """Create the appropriate model based on CLI arguments or environment variables.

    Args:
        model: Override model name (e.g., "gpt-4", "claude-sonnet-4-5-20250929")
        provider: Override provider ("openai", "anthropic", or "custom")
        api_base: Custom API base URL for OpenAI-compatible APIs
        api_key: Override API key

    Returns:
        ChatModel instance (OpenAI or Anthropic)

    Raises:
        SystemExit if no API key is configured or invalid configuration
    """
    # Determine API keys (CLI override or environment)
    openai_key = api_key if api_key and provider in ["openai", "custom", None] else os.environ.get("OPENAI_API_KEY")
    anthropic_key = api_key if api_key and provider == "anthropic" else os.environ.get("ANTHROPIC_API_KEY")

    # If provider is explicitly set, use that provider
    if provider == "anthropic":
        if not anthropic_key:
            console.print("[bold red]Error:[/bold red] ANTHROPIC_API_KEY not set.")
            console.print("\nPlease set it with:")
            console.print("  export ANTHROPIC_API_KEY=your_api_key_here")
            console.print("\nOr use --api-key flag.")
            sys.exit(1)

        from langchain_anthropic import ChatAnthropic

        model_name = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
        console.print(f"[dim]Using Anthropic model: {model_name}[/dim]")
        return ChatAnthropic(
            model_name=model_name,
            max_tokens=20000,
            api_key=anthropic_key,
        )

    elif provider in ["openai", "custom"] or provider is None:
        # OpenAI or custom OpenAI-compatible API
        if not openai_key:
            # If no explicit provider and no OpenAI key, try Anthropic
            if provider is None and anthropic_key:
                from langchain_anthropic import ChatAnthropic

                model_name = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
                console.print(f"[dim]Using Anthropic model: {model_name}[/dim]")
                return ChatAnthropic(
                    model_name=model_name,
                    max_tokens=20000,
                    api_key=anthropic_key,
                )

            # No API key available
            console.print("[bold red]Error:[/bold red] No API key configured.")
            console.print("\nPlease set one of the following:")
            console.print("  - OPENAI_API_KEY     (for OpenAI models)")
            console.print("  - ANTHROPIC_API_KEY  (for Claude models)")
            console.print("  - Use --api-key flag with --provider")
            console.print("\nExample:")
            console.print("  export OPENAI_API_KEY=your_api_key_here")
            console.print("\nOr add it to your .env file.")
            sys.exit(1)

        from langchain_openai import ChatOpenAI

        # Determine model name
        if provider == "custom" and not model:
            console.print("[bold red]Error:[/bold red] --model is required when using --provider custom")
            sys.exit(1)

        model_name = model or os.environ.get("OPENAI_MODEL", "gpt-5-mini")

        # Build ChatOpenAI kwargs
        kwargs = {
            "model": model_name,
            "temperature": 0.7,
            "api_key": openai_key,
        }

        # Add custom base_url if provided
        if api_base:
            kwargs["base_url"] = api_base
            console.print(f"[dim]Using custom OpenAI-compatible API: {api_base}[/dim]")
            console.print(f"[dim]Model: {model_name}[/dim]")
        elif provider == "custom":
            console.print("[bold red]Error:[/bold red] --api-base is required when using --provider custom")
            sys.exit(1)
        else:
            console.print(f"[dim]Using OpenAI model: {model_name}[/dim]")

        return ChatOpenAI(**kwargs)

    else:
        console.print(f"[bold red]Error:[/bold red] Unknown provider: {provider}")
        sys.exit(1)
