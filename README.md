# Multi-Model Comparison Tool

A robust Python command-line utility built to evaluate and compare the responses, speed (latency), and cost metrics of four distinct LLMs simultaneously using the OpenRouter API.

## 🚀 Features
- **Multi-Model Querying**: Ask a single question to 4 models (`GPT-5.5`, `Claude 4.8 Opus`, `Gemini 2.5 Pro`, `Qwen 3.7`) concurrently.
- **Performance Analytics**: Calculates exact network latency in seconds.
- **Token Cost Breakdown**: Extracts input/output token usage and applies live-pricing calculations.
- **Fail-Safe Isolation**: Built with robust try/except blocks so a single model API failure won't crash the entire pipeline.

## 🛠️ Setup Instructions

1. **Clone and Navigate:**
   ```bash
   git clone [https://github.com/Vyshnavi-279/Multimodel.git](https://github.com/Vyshnavi-279/Multimodel.git)
   cd Multimodel
