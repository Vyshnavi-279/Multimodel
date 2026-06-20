from llm import ask, MODELS

QUESTION = "What is the capital of France?"

# Collect results, tolerating per-model failures
results = []
for model in MODELS:
    try:
        result = ask(QUESTION, model)
        result["model"] = model
        result["error"] = None
        results.append(result)
    except Exception as e:
        print(f"[ERROR] {model}: {e}")
        results.append({
            "model":     model,
            "answer":    "N/A",
            "latency":   0.0,
            "in_tokens": 0,
            "out_tokens": 0,
            "cost":      0.0,
            "error":     str(e),
        })

# Print comparison table
COL = {"model": 30, "latency": 10, "tokens": 20, "cost": 14}
DIVIDER = "-" * sum(COL.values())

print(f"\nQuestion: {QUESTION}\n")
print(DIVIDER)
print(
    f"{'Model':<{COL['model']}}"
    f"{'Latency':>{COL['latency']}}"
    f"{'Tokens':>{COL['tokens']}}"
    f"{'Cost (USD)':>{COL['cost']}}"
)
print(DIVIDER)

for r in results:
    tokens_str = f"{r['in_tokens']} in / {r['out_tokens']} out"
    print(
        f"{r['model']:<{COL['model']}}"
        f"{r['latency']:.2f}s{' ' * (COL['latency'] - 6)}"
        f"{tokens_str:>{COL['tokens']}}"
        f"${r['cost']:.6f}{' ' * (COL['cost'] - 9)}"
    )
    answer_preview = r["answer"].replace("\n", " ")[:72]
    if len(r["answer"]) > 72:
        answer_preview += "..."
    print(f"  {answer_preview}\n")

print(DIVIDER)
