from awesome_progress_bar import ProgressBar
import time

total = 133
bar = ProgressBar(total)
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter()
except:
    bar.stop()
bar.wait()
time_passed = bar.get_time_passed()
print(f'Total time passed: {time_passed}')
# Progress: |==================================== 00:15 =====================================| 100.00%
# Total time passed: 00:15

bar = ProgressBar(total, 'Prefix', 'Suffix', use_eta=True)
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter()
except:
    bar.stop()
bar.wait()
time_passed = bar.get_time_passed(False)
print(f'Total seconds passed: {time_passed:.4f}')
# Prefix: |================================== 00:15 ==================================| 100.00% Suffix
# Total seconds passed: 14.5497


# No need to use try/catch without thread
bar = ProgressBar(total, use_thread=False, time_format='hh, mm ss')
for x in range(total):
    time.sleep(0.1)
    bar.iter()
# Progress: |================================== 00, 00 15 ===================================| 100.00%
