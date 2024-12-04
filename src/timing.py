# src/timing.py

import time
from datetime import datetime, timedelta
from functools import wraps

class TimingStats:
    def __init__(self):
        self.start_time = time.time()
        self.steps = {}
        self.current_step = None
        
    def add_step(self, step_name, duration, success=True):
        self.steps[step_name] = {
            'duration': duration,
            'success': success,
            'start_time': datetime.now() - timedelta(seconds=duration)
        }
        
    def get_total_time(self):
        return time.time() - self.start_time
    
    def print_summary(self):
        print("\n=== Timing Summary ===")
        total_duration = 0
        
        print("\nDetailed steps:")
        for step, info in self.steps.items():
            duration = info['duration']
            status = "✓" if info['success'] else "✗"
            start_time = info['start_time'].strftime('%Y-%m-%d %H:%M:%S')
            print(f"{status} {step:25} - Started: {start_time} - Duration: {timedelta(seconds=int(duration))}")
            total_duration += duration
            
        print(f"\nTotal execution time: {timedelta(seconds=int(self.get_total_time()))}")
        
    def log_to_file(self, filename="timing_log.csv"):
        """Записать статистику в CSV файл"""
        if not hasattr(self, '_header_written'):
            with open(filename, 'w') as f:
                f.write("timestamp,step,duration,success\n")
            self._header_written = True
            
        with open(filename, 'a') as f:
            for step, info in self.steps.items():
                f.write(f"{info['start_time']},{step},{info['duration']},{info['success']}\n")

# Создаем глобальный экземпляр
timing_stats = TimingStats()

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Информация о начале выполнения
        start_time = time.time()
        print(f"\n{'='*50}")
        print(f"Starting {func.__name__} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Выполнение функции
            result = func(*args, **kwargs)
            
            # Расчет времени выполнения
            duration = time.time() - start_time
            timing_stats.add_step(func.__name__, duration, success=True)
            
            # Информация о завершении
            print(f"\nCompleted {func.__name__} in {timedelta(seconds=int(duration))}")
            timing_stats.log_to_file()  # Логируем в файл
            
            return result
            
        except Exception as e:
            # В случае ошибки
            duration = time.time() - start_time
            timing_stats.add_step(f"{func.__name__} (failed)", duration, success=False)
            print(f"\nError in {func.__name__} after {timedelta(seconds=int(duration))}")
            timing_stats.log_to_file()  # Логируем в файл
            raise e
            
    return wrapper

def get_estimated_time(current, total, elapsed_time):
    """Рассчитать оставшееся время"""
    if current == 0:
        return "calculating..."
    
    avg_time = elapsed_time / current
    remaining = total - current
    eta = remaining * avg_time
    
    return str(timedelta(seconds=int(eta)))