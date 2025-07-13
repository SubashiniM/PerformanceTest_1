import requests

azure_openai_endpoint = 'https://<your-resource>.openai.azure.com/openai/deployments/<deployment-id>/chat/completions?api-version=2024-05-01'
api_key = 'your-azure-openai-api-key'

headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

def analyze_results_with_openai(jmeter_output):
    prompt = f"Analyze this JMeter test result:\n\n{jmeter_output}"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a performance test analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(azure_openai_endpoint, headers=headers, json=payload)
    print("AI Analysis:", response.json()["choices"][0]["message"]["content"])

# Optional: Run after getting output
# analyze_results_with_openai("paste JMeter summary or sample output here")
