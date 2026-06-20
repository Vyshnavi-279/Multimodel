# Spec — Multi-Model Comparison Tool

## Goal
[cite_start]Ask one question to four LLMs via OpenRouter and show each answer with its speed and cost[cite: 75].

## Input
- A single question (string). [cite_start]Hardcode first; later read from input[cite: 75].

## Output (per model)
- [cite_start]answer text, latency (seconds), tokens (in/out), cost (USD)[cite: 75].

## Models (OpenRouter IDs)
- openai/gpt-5.5
- anthropic/claude-opus-4.8
- google/gemini-3.1-pro
- qwen/qwen-3.7

## Pipeline
1. [cite_start]Load OPENROUTER_API_KEY from .env[cite: 75].
2. [cite_start]For each model: send the question, time the call, read token usage[cite: 75].
3. Calculate cost = (in_tokens * in_price) + (out_tokens * out_price).
4. [cite_start]Print all four results side-by-side[cite: 75].

## Error handling
- [cite_start]Wrap each model call in try/except; on failure, log it and continue[cite: 75].