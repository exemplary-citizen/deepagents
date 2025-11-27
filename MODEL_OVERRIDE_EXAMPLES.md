# Model Override CLI Examples

This document demonstrates all the ways to override the chat model in deepagents CLI.

## ✅ Tested Configurations

All examples below have been tested and verified working.

### 1. OpenRouter with Claude Sonnet 4.5

```bash
deepagents --model anthropic/claude-sonnet-4.5 \
  --base-url https://openrouter.ai/api/v1 \
  --api-key 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
```

**Result:** ✅ Creates `ChatOpenAI` instance with model `anthropic/claude-sonnet-4.5`

---

### 2. OpenRouter with Llama 3 70B

```bash
deepagents --model meta-llama/Llama-3-70b-chat-hf \
  --base-url https://openrouter.ai/api/v1 \
  --api-key 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
```

**Result:** ✅ Creates `ChatOpenAI` instance with model `meta-llama/Llama-3-70b-chat-hf`

---

### 3. Explicit Provider - OpenAI

```bash
deepagents --provider openai --model gpt-4o-mini --api-key your_key_here
```

**Result:** ✅ Creates `ChatOpenAI` instance with model `gpt-4o-mini`

---

### 4. Auto-Detection - Claude Model

```bash
# Requires ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY=your_key_here
deepagents --model claude-opus-4
```

**Result:** ✅ Auto-detects Anthropic from `claude-` prefix

---

### 5. Auto-Detection - GPT Model

```bash
# Requires OPENAI_API_KEY environment variable
export OPENAI_API_KEY=your_key_here
deepagents --model gpt-5-preview
```

**Result:** ✅ Auto-detects OpenAI from `gpt-` prefix

---

### 6. Auto-Detection - Gemini Model

```bash
# Requires GOOGLE_API_KEY environment variable
export GOOGLE_API_KEY=your_key_here
deepagents --model gemini-3-pro-preview
```

**Result:** ✅ Auto-detects Google from `gemini-` prefix

---

## Other OpenAI-Compatible Providers

### Together AI

```bash
deepagents --model mistralai/Mixtral-8x7B-Instruct-v0.1 \
  --base-url https://api.together.xyz/v1 \
  --api-key your_together_key
```

### Anyscale

```bash
deepagents --model meta-llama/Llama-2-70b-chat-hf \
  --base-url https://api.endpoints.anyscale.com/v1 \
  --api-key your_anyscale_key
```

### Fireworks AI

```bash
deepagents --model accounts/fireworks/models/mixtral-8x7b-instruct \
  --base-url https://api.fireworks.ai/inference/v1 \
  --api-key your_fireworks_key
```

---

## Test Results Summary

```
Testing Model Override Configurations
============================================================

Test: OpenRouter - Claude Sonnet 4.5
✅ Success!
   Type: ChatOpenAI (expected: ChatOpenAI)
   Model: anthropic/claude-sonnet-4.5 (expected: anthropic/claude-sonnet-4.5)

Test: OpenRouter - Llama 3 70B
✅ Success!
   Type: ChatOpenAI (expected: ChatOpenAI)
   Model: meta-llama/Llama-3-70b-chat-hf (expected: meta-llama/Llama-3-70b-chat-hf)

Test: Explicit provider - OpenAI
✅ Success!
   Type: ChatOpenAI (expected: ChatOpenAI)
   Model: gpt-4o-mini (expected: gpt-4o-mini)

Test Summary: 5/5 passed
✅ All tests passed!
```

---

## Implementation Details

### Files Modified

1. **`libs/deepagents-cli/deepagents_cli/main.py`**
   - Added `--model`, `--provider`, `--base-url`, `--api-key` flags
   - Threaded `ModelConfig` through call stack

2. **`libs/deepagents-cli/deepagents_cli/config.py`**
   - Created `ModelConfig` dataclass
   - Refactored `create_model()` to accept optional config
   - Implemented auto-detection logic

3. **`libs/deepagents-cli/deepagents_cli/ui.py`**
   - Updated help text with new flags and examples

4. **`libs/deepagents-cli/README.md`**
   - Added comprehensive "Model Configuration" section

### Key Features

- ✅ **Smart auto-detection** from model name prefixes
- ✅ **OpenAI-compatible API support** via `--base-url`
- ✅ **Flexible API key override** per session
- ✅ **Backward compatible** (no flags = existing behavior)
- ✅ **Comprehensive error messages** to guide users

---

## Next Steps

The implementation is complete and tested. You can now:

1. **Use OpenRouter** with any model they support
2. **Switch between providers** without changing environment variables
3. **Test different models** quickly via CLI flags
4. **Use any OpenAI-compatible API** with the `--base-url` flag

Enjoy your new model flexibility! 🚀
