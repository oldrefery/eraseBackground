# src/progress.py

import os
import json
import time

class ProgressTracker:
    def __init__(self, output_dir):
        self.progress_file = os.path.join(output_dir, 'progress.json')
        self.progress = self.load_progress()
        self.start_times = {}

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=4)

    def is_completed(self, step_name):
        return self.progress.get(step_name, {}).get('completed', False)

    def mark_started(self, step_name):
        self.start_times[step_name] = time.time()
        self.progress[step_name] = self.progress.get(step_name, {})
        self.progress[step_name]['started_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_times[step_name]))
        self.save_progress()

    def mark_completed(self, step_name):
        end_time = time.time()
        start_time = self.start_times.get(step_name, end_time)
        elapsed_time = end_time - start_time
        self.progress[step_name]['completed'] = True
        self.progress[step_name]['completed_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
        self.progress[step_name]['elapsed_time_sec'] = elapsed_time
        self.save_progress()
