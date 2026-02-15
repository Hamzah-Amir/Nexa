import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="nexa_log.json"):
        self.logfile = log_file
        if not os.path.exists(self.logfile):
            with open(self.logfile, 'w') as f:
                json.dump([], f)
    
    def log(self, command, action, result=None):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "action": action,
            "result": result
        }
        
        # Read existing Logs
        with open(self.logfile, 'r') as f:
            logs = json.load(f)

        # Write new logs
        logs.append(log_entry)

        # Write back to the file
        with open(self.logfile, 'w') as f:
            json.dump(logs, f, indent=2)