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
- __spinner_type:__ One of `['sb', 'db']`. With `'sb'` progress bar will print spinner 
consisting of 1 Braille pattern. `'db'` - 2 Braille patterns. Default is `'sb'`. 
- __use_spinner:__ If True the spinner will be shown. Default is True.
- __new_line_at_end:__ If True the caret will go to the new line at the end.
Default it True.
- __use_eta:__ If True the information about approximate remaining time will be 
printed. Default is False.
- __eta_format:__ The format of ETA. Similar to the __time_format__. Default is 
'mm:ss'.

```python
from awesome_progress_bar import ProgressBar

bar = ProgressBar(100)
# Progress: ⡆ |=>                              00:01                                |   1.00% Complete

bar = ProgressBar(100, prefix='Prefix', suffix='Suffix', bar_length=70)
# Prefix: ⡆ |=>                 00:01                   |   1.00% Suffix

bar = ProgressBar(100, fill='#', use_time=False, bar_length=70)
# Progress: ⡆ |#>                                     |   3.00% Complete

bar = ProgressBar(100, time_format='hh mm:ss', bar_length=70)
# Progress: ⡆ |>              00 00:01                |   1.00% Complete

bar = ProgressBar(100, bar_length=70, use_eta=True, spinner_type='db')
# Progress: ⢌⡱ |===>           00:03                |  10.00% ETA: 00:33
```

#### Progress

Each iteration user should call
```python
bar.iter(append='')
```

In the thread mode progress bar's state is updating by itself every __update_period__
seconds. In this mode `bar.iter()` doesn't print anything and it used only for tracking
the progress. In the mode without thread `bar.iter()` prints the bar every time user 
call it.

Parameters:
- __append:__ A string to append after the bar

```python
bar = ProgressBar(100, bar_length=70)
bar.iter(' appended text')
# Progress: ⠁ |>                                   00:00                                     |   1.00% appended text
```

#### Attention!

If you want to use thread mode and your code may accept exceptions (including
KeyboardInterrupt) you must handle them using `stop` function. Otherwise the progress bar
may not stop printing.

```python
from awesome_progress_bar import ProgressBar
import time

bar = ProgressBar(100)
try:
    for x in range(100):
        bar.iter()
        time.sleep(0.1)
except:
    bar.stop()
``` 

---

Feel free to suggest ideas to improve this package in the GitHub's Issues section.

![](https://img.shields.io/badge/@Yoskutik-444?logo=github&style=flat-square) 