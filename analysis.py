import paramiko
import requests
import time
import os

# --- Configuration ---

# Azure VM SSH credentials
hostname = 'your-vm-ip'                  # Replace with public IP or DNS
username = 'azureuser'
private_key_path = 'path/to/key.pem'     # Replace with your private key path

# JMeter paths on VM
jmeter_command = '/home/azureuser/apache-jmeter-5.6.2/bin/jmeter -n -t /home/azureuser/test_plan.jmx -l /home/azureuser/results.jtl'
remote_jtl_path = '/home/azureuser/results.jtl'
local_jtl_path = 'results.jtl'

# Azure OpenAI API details
azure_openai_endpoint = 'https://<your-resource>.openai.azure.com/openai/deployments/<deployment-id>/chat/completions?api-version=2024-05-01'
api_key = 'your-azure-openai-api-key'

# --- Step 1: Trigger JMeter test ---

def trigger_jmeter_test():
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, pkey=key)

    print("Running JMeter test on VM...")
    stdin, stdout, stderr = ssh.exec_command(jmeter_command)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print("Errors:", err)

    ssh.close()

# --- Step 2: Download JTL result file ---

def download_jtl_file():
    print("Downloading JTL file from VM...")
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, pkey=key)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_jtl_path, local_jtl_path)
    sftp.close()
    transport.close()
    print("Downloaded to:", local_jtl_path)

# --- Step 3: Analyze with Azure OpenAI ---

def analyze_results_with_openai():
    print("Reading JMeter results...")
    with open(local_jtl_path, 'r') as file:
        jtl_data = file.read()

    prompt = f"Analyze the following JMeter test results:\n\n{jtl_data[:8000]}"  # Limit to 8000 chars if needed

    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a performance test analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    print("Sending to Azure OpenAI...")
    response = requests.post(azure_openai_endpoint, headers=headers, json=payload)
    result = response.json()["choices"][0]["message"]["content"]
    print("AI Analysis:\n", result)

# --- Main ---

trigger_jmeter_test()
time.sleep(10)  # Wait to ensure JMeter finishes (adjust as needed)
download_jtl_file()
analyze_results_with_openai()
