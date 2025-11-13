# deepagents cli

This is the CLI for deepagents

## Usage

Start an interactive session with the default configuration:

```bash
deepagents
```

You can override the underlying chat model and provider without touching environment variables:

- `deepagents --model gpt-4o` – run with a different OpenAI model ID
- `deepagents --provider anthropic --model claude-3-opus` – force the Anthropic client and model
- `deepagents --provider openai --model meta/llama-3 --base-url https://openrouter.ai/api/v1` – use an OpenAI-compatible endpoint such as OpenRouter (ensure the matching API key is exported)

If you don’t pass a provider, the CLI auto-detects one based on available API keys (`OPENAI_API_KEY`, `OPENROUTER_API_KEY`, or `ANTHROPIC_API_KEY`).

## Development

### Running Tests

To run the test suite:

```bash
uv sync --all-groups

make test
```
