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

---

### How to use

#### Initialization

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

```python
from awesome_progress_bar import ProgressBar

bar = ProgressBar(100)
# Progress: ⣷ |=>                              00:01                                |   1.00% Complete

bar = ProgressBar(100, prefix='Prefix', suffix='Suffix', bar_length=70)
# Prefix: ⣟ |=>                 00:01                   |   1.00% Suffix

bar = ProgressBar(100, fill='#', use_time=False, bar_length=70)
# Progress: ⣽ |#>                                     |   3.00% Complete

bar = ProgressBar(100, time_format='hh mm:ss', bar_length=70)
# Progress: ⣷ |>              00 00:01                |   1.00% Complete
```

#### Progress

Each iteration user should call
```python
bar.iter()
```

In the thread mode progress bar's state is updating by itself every __update_period__
seconds. In this mode `bar.iter()` doesn't print anything and it used only for tracking
the progress. In the mode without thread `bar.iter()` prints the bar every time user 
call it.

#### Attention!

In the thread mode you should handle KeyboardInterrupt exception with `bar.stop()` 
function:

```python
from awesome_progress_bar import ProgressBar
import time

bar = ProgressBar(100)
try:
    for x in range(100):
        bar.iter()
        time.sleep(0.1)
except KeyboardInterrupt:
    bar.stop()
``` 

Or you can also use `finally`.