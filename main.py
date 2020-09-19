from awesome_progress_bar import ProgressBar
import time
import random

total = 37
bar = ProgressBar(total=total, suffix='', use_thread=False)
try:
    for x in range(total):
        bar.iter(' asd')
        time.sleep(0.1)
        # time.sleep(random.randint(5, 10) / 4)
except KeyboardInterrupt:
    bar.stop()