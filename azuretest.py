import subprocess

az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"


try:
    subprocess.run([az_path, "--version"], check=True)
except Exception as e:
    print(f"Failed to run az CLI: {e}")