import os
import glob
import json
import requests

def parse_test_results(directory):
    suggestions = []
    for file in glob.glob(f"{directory}/*.xml") + glob.glob(f"{directory}/*.txt"):
        with open(file, 'r') as f:
            content = f.read()
            if "error" in content.lower() or "failure" in content.lower():
                # Fetch metrics from Prometheus
                metrics = requests.get(f"{os.getenv('PROMETHEUS_URL')}/api/v1/query?query=rate(http_requests_total[5m])").json()
                suggestion = {
                    "file": file,
                    "issue": "Test failure detected",
                    "suggestion": "Add null check or optimize endpoint",
                    "metrics": metrics.get('data', {}).get('result', []),
                    "proposed_fix": "/* Example: if (obj == null) return; */"
                }
                # Placeholder for xAI API
                response = requests.post(
                    "https://api.x.ai/v1/analyze",
                    headers={"Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"},
                    json={"log": content, "metrics": suggestion["metrics"]}
                )
                suggestion.update(response.json().get("suggestion", {}))
                suggestions.append(suggestion)
    return suggestions

def create_pr_suggestion(suggestions):
    with open("suggestions.json", "w") as f:
        json.dump(suggestions, f, indent=2)
    print("Suggestions written to suggestions.json. Create PR manually or use GitHub/GitLab API.")

def main():
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else "test-results"
    suggestions = parse_test_results(directory)
    create_pr_suggestion(suggestions)

if __name__ == "__main__":
    main()
