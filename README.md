# Awesome progress bar
![](https://img.shields.io/pypi/v/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/dm/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/l/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/pyversions/awesome-progress-bar?style=flat-square)

It's a progress bar for the terminal. But why it is awesome?
- It has thread mode. This way progress bar can run in the parallel.
- It's animated with ASCII characters.
- It also measures elapsed time.
- It's user-friendly and customizable.

Why does progress bar need to be run in the parallel mode?

The bar should be updated when it is time to. Imagine we are doing something in the `for`
loop and each iteration we update its state. But each iteration can take different amount
of time. And each iteration can be longer than 1 minute. And without threads the animation
would have non-constant amount of FPS.

<br />

# How to use

## Initialization

Parameters:
- __total:__ Amount of iterations.
- __prefix:__ A short message before the progress bar. Default is 'Progress'.
- __suffix:__ A short message after the progress bar. Default is 'Complete'.
- __fill:__ A character that will be used as progress bar filler.
- __bar_length:__ The length of the whole string (including prefix, spinner,
progress bar, percents and suffix). Default is equal to the minimum between 
terminal's width and 100.
- __update_period:__ The duration of pause between iterations in seconds.
Default is 0.1. Works only if __use_thread__ is True.
- __use_time:__ If True there will be an information about elapsed time in the
center of the progress bar written in time_format format. Default is True.
- __time_format:__ String, that should include hh, mm or/and ss. hh will be
replaced with amount of elapsed hours, mm - minutes, ss - seconds. Default is 
'mm:ss'.
- __use_thread:__ If True ProgressBar will create extra thread. Default is True.
- __spinner_type:__ One of `['sb', 'db', 's']`. With `'sb'` progress bar will print 
spinner consisting of 1 Braille pattern. `'db'` - 2 Braille patterns. `'s'` - a
slash. Default is `'sb'`. 
- __use_spinner:__ If True the spinner will be shown. Default is True.
- __new_line_at_end:__ If True the caret will go to the new line at the end.
Default it True.
- __use_eta:__ If True the information about approximate remaining time will be 
printed. Default is False.
- __eta_format:__ The format of ETA. Similar to the __time_format__. Default is 
'mm:ss'.

<br />

## Methods

- [iter(append)](#iter): Used for tracking the progress.
- [stop()](#stop): Stops the bar in the thread mode.
- [wait()](#wait): Blocks the program until bar is dead.

<br />

<h4 id="iter">bar.iter(append='')</h4>

Used for tracking the progress.
- In the thread mode only increases the number of iteration.
- Without extra thread `bar.iter()` prints the bar each time user call it.

Parameters:
- __append:__ A string to append after the bar. The appended text doesn't effect on
the progress bar width. 

<br />

<h4 id="stop">bar.stop()</h4>

Stops the bar if it run in the thread mode.

If the user doesn't stop the bar, it will update endlessly. Therefore, I recommend updating 
the bar using `bar.iter()` in the try/except block, and calling `bar.stop()` in the `except` 
or `finally` blocks.

<br />

<h4 id="wait">bar.wait()</h4>

Blocks the program until bar is dead.

The bar updates every __update_period__ seconds in the thread mode. Hence, there can be a small
delay between last calling `bar.iter()` and next try for printing something. So, if you want to
print anything after the progress is done be aware to use `bar.wait()`  

<br />

### Examples

```python
from awesome_progress_bar import ProgressBar
import time

total = 133
bar = ProgressBar(total, bar_length=50)
try:
    for x in range(total):
        time.sleep(0.1)
        bar.iter(' Appended')
except:
    bar.stop()
bar.wait()
print('Bar is done')

# Progress:   |====== 00:14 ======| 100.00% Complete Appended
# Bar is done
```
```python
from awesome_progress_bar import ProgressBar

bar = ProgressBar(100, prefix='Prefix', suffix='Suffix', bar_length=50)
# Prefix: ⡆ |=>       00:00         |   4.51% Suffix

bar = ProgressBar(100, fill='#', use_time=False, bar_length=50, use_spinner=False)
# Progress: |>                    |   3.01% Complete

bar = ProgressBar(100, time_format='hhh mmmin sss', use_eta=True, bar_length=70, spinner_type='s')
# Progress: \ |==>         00h 00min 01s            |   7.52% ETA: 00:12

bar = ProgressBar(100, bar_length=70, spinner_type='db')
# Progress: ⢈⡱ |=========>      00:03                 |  25.56% Complete
```
 
---

Feel free to suggest ideas to improve this package in the GitHub's Issues section.

![](https://img.shields.io/badge/@Yoskutik-444?logo=github&style=flat-square) 