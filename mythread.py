import threading
import time
import subprocess
status=subprocess.run(['git','status'])
print(status)