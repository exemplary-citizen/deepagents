# deepagents cli

This is the CLI for deepagents

## Usage

### Basic Usage

```bash
deepagents
```

This will start an interactive coding session with the default agent and model configuration.

### Model and Provider Configuration

You can override the model and provider using CLI flags:

#### Using OpenAI Models

```bash
# Use a specific OpenAI model
deepagents --model gpt-4 --provider openai

# Model override with environment API key
export OPENAI_API_KEY=your_key_here
deepagents --model gpt-4o
```

#### Using Anthropic Models

```bash
# Use a specific Claude model
deepagents --model claude-sonnet-4-5-20250929 --provider anthropic

# With API key override
deepagents --model claude-opus-4-20250514 --provider anthropic --api-key your_key_here
```

#### Using OpenAI-Compatible APIs (OpenRouter, etc.)

Many providers offer OpenAI-compatible APIs. You can use them with the `--provider custom` flag:

```bash
# Using OpenRouter
export OPENROUTER_API_KEY=your_key_here
deepagents \
  --provider custom \
  --model meta-llama/llama-3-70b-instruct \
  --api-base https://openrouter.ai/api/v1 \
  --api-key $OPENROUTER_API_KEY

# Using another OpenAI-compatible provider
deepagents \
  --provider custom \
  --model your-model-name \
  --api-base https://your-provider.com/v1 \
  --api-key your_api_key
```

### CLI Flags

- `--agent NAME` - Agent identifier for separate memory stores (default: agent)
- `--model MODEL` - Override the model name (e.g., gpt-4, claude-sonnet-4-5-20250929)
- `--provider PROVIDER` - LLM provider: openai, anthropic, or custom (for OpenAI-compatible APIs)
- `--api-base URL` - Custom API base URL for OpenAI-compatible APIs
- `--api-key KEY` - Override API key (useful for testing with different keys)
- `--auto-approve` - Auto-approve tool usage without prompting
- `--sandbox TYPE` - Remote sandbox for code execution: none (default), modal, daytona, or runloop
- `--sandbox-id ID` - Existing sandbox ID to reuse
- `--sandbox-setup PATH` - Path to setup script to run in sandbox after creation

### Environment Variables

Default model configuration is controlled by environment variables:

- `OPENAI_API_KEY` - API key for OpenAI (required for OpenAI models)
- `OPENAI_MODEL` - Default OpenAI model (default: gpt-5-mini)
- `ANTHROPIC_API_KEY` - API key for Anthropic (required for Claude models)
- `ANTHROPIC_MODEL` - Default Anthropic model (default: claude-sonnet-4-5-20250929)
- `TAVILY_API_KEY` - API key for web search (optional)

CLI flags take precedence over environment variables.

## Development

### Running Tests

To run the test suite:

```bash
uv sync --all-groups

make test
```
