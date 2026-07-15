import subprocess
# Desired Application path
path = r"C:\Users\sutha\AppData\Local\Programs\Antigravity\Antigravity.exe"
def run_appication():
    # subprocess.Popen(["cmd", "/c", "start", "", "Brave"])
    subprocess.run([path])
    #