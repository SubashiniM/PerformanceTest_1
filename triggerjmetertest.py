import paramiko

# Azure VM SSH credentials
hostname = 'your-vm-ip'  # Replace with public IP
username = 'azureuser'
private_key_path = 'path/to/private/key.pem'

# JMeter command to run
jmeter_command = '/home/azureuser/apache-jmeter-5.6.2/bin/jmeter -n -t /home/azureuser/test_plan.jmx -l /home/azureuser/results.jtl'

def trigger_jmeter_test():
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, pkey=key)

    stdin, stdout, stderr = ssh.exec_command(jmeter_command)
    print("Output:", stdout.read().decode())
    print("Errors:", stderr.read().decode())

    ssh.close()

trigger_jmeter_test()
