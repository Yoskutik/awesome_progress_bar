from awesome_progress_bar import ProgressBar
import time

total = 13
bar = ProgressBar(total)
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter()
except:
    bar.stop()
bar.wait()
# Progress: |================================ 00:01 ================================| 100.00% Complete


bar = ProgressBar(total, 'Prefix', 'Suffix')
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter()
except:
    bar.stop()
bar.wait()
# Prefix: |================================== 00:01 ==================================| 100.00% Suffix


# No need to use try/catch without thread
bar = ProgressBar(total, use_thread=False, time_format='hh, mm ss')
for x in range(total):
    time.sleep(0.1)
    bar.iter()
# Progress: |============================== 00, 00 01 ==============================| 100.00% Complete
