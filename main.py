from awesome_progress_bar import ProgressBar
import time

total = 133
bar = ProgressBar(total, bar_length=70, spinner_type='s')
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter()
except:
    bar.stop()
bar.wait()
print('Bar is done')
