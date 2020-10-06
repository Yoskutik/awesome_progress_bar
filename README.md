# Awesome progress bar
![](https://img.shields.io/pypi/v/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/dm/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/l/awesome-progress-bar?color=blue&style=flat-square)
![](https://img.shields.io/pypi/pyversions/awesome-progress-bar?style=flat-square)

[<img width="800" src="https://github.com/Yoskutik/awesome_progress_bar/raw/master/preview.gif" />]

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

#### Parameters:

<table>
    <tr>
        <td><b>total</b></td>
        <td>Amount of iterations</td>
    </tr>
    <tr>
        <td><b>prefix</b></td>
        <td>A short message before the progress bar. Default is <code>'Progress'</code></td>
    </tr>
    <tr>
        <td><b>suffix</b></td>
        <td>A short message after the progress bar. Default is <code>''</code></td>
    </tr>
    <tr>
        <td><b>fill</b></td>
        <td>A character that will be used as progress bar filler. Default is <code>'='</code></td>
    </tr>
    <tr>
        <td><b>bar_length</b></td>
        <td>The length of the whole string (including prefix, spinner, progress bar, percents and 
        suffix). Default is equal to the minimum between terminal's width and 100</td>
    </tr>
    <tr>
        <td><b>update_period</b></td>
        <td>The duration of pause between iterations in seconds. Default is <code>0.1</code>. Works 
        only if <b>use_thread</b> is <code>True</code></td>
    </tr>
    <tr>
        <td><b>use_time</b></td>
        <td>If <code>True</code> there will be an information about elapsed time in the center of 
        the progress bar written in <b>time_format</b> format. Default is <code>True</code></td>
    </tr>
    <tr>
        <td><b>time_format</b></td>
        <td>String, that should include <code>'hh'</code>, <code>'mm'</code> or/and <code>'ss'</code>. 
        <code>'hh'</code> will be replaced with amount of elapsed hours, <code>'mm'</code> - minutes, 
        <code>'ss'</code> - seconds. Default is <code>'mm:ss'</code></td>
    </tr>
    <tr>
        <td><b>use_thread</b></td>
        <td>If <code>True</code> ProgressBar will create extra thread. Default is <code>True</code></td>
    </tr>
    <tr>
        <td><b>spinner_type</b></td>
        <td>One of <code>['sb', 'db', 's']</code>. With <code>'sb'</code> progress bar will print 
        spinner consisting of 1 Braille pattern. <code>'db'</code> - 2 Braille patterns. 
        <code>'s'</code> - a slash. Default is <code>'sb'</code></td>
    </tr>
    <tr>
        <td><b>use_spinner</b></td>
        <td>If <code>True</code> the spinner will be shown. Default is <code>True</code></td>
    </tr>
    <tr>
        <td><b>last_char</b></td>
        <td>Something, that will be printed after the progress is done. Default is <code>'\n'</code></td>
    </tr>
    <tr>
        <td><b>use_eta</b></td>
        <td>If <code>True</code> the information about approximate remaining time will be printed. 
        Default is <code>False</code></td>
    </tr>
    <tr>
        <td><b>eta_format</b></td>
        <td>The format of ETA. Similar to the <b>time_format</b>. Default is equal to the 
        <b>time_format</b></td>
    </tr>
</table>

## Methods

<table>
    <tr>
        <td><b>iter(append='')</b></td>
        <td>
            <p>Used for tracking the progress.</p>
            <ul>
                <li>In the thread mode only increases the number of iteration.</li>
                <li>Without extra thread <code>bar.iter()</code> prints the bar each time user call it.</li>
            </ul>
            Parameters:
            <ul>
                <li><b>append:</b> A string to append after the bar. The appended text doesn't effect 
                on the progress bar width. </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td><b>get_time_passed (return_str=True)</b></td>
        <td>
            <p>Returns the time spent.</p>
            <p>
                If the progress is done returns bar's operating time. If not - returns the time elapsed 
                from the progress start.
            </p>
            Parameters:
            <ul>
                <li><b>return_str:</b> If <code>True</code> returns time in the <b>time_format</b>
                format. If not returns just amount of seconds</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td><b>stop()</b></td>
        <td>
            <p>Stops the bar in the thread mode.</p>
            <p>
                If the bar doesn't call the <code>iter</code> function the required number of times, the 
                created thread will run until you call the <stop>stop</stop> function.
            </p>
        </td>
    </tr>
    <tr>
        <td><b>wait()</b></td>
        <td>
            <p>Blocks the program until bar is dead.</p>
            <p>
                The bar updates every <b>update_period</b> seconds in the thread mode. Hence, there can 
                be a small delay between last calling <code>bar.iter()</code> and next try for printing 
                something. So, if you want to print anything after the progress is done be aware to use
                <code>bar.wait()</code>  
            </p>
        </td>
    </tr>
</table>

\* `stop()` and `wait()` are needed only in the thread mode.

## Examples

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

# Progress: |=========== 00:15 ============| 100.00% Appended
# Bar is done
```
```python
from awesome_progress_bar import ProgressBar

bar = ProgressBar(100, prefix='Prefix', suffix='Suffix', use_eta=True, bar_length=70)
# Prefix: ⠇ |==>             00:00/00:14                |   5.26% Suffix

bar = ProgressBar(100, fill='#', use_time=False, bar_length=50, use_spinner=False)
# Progress: |##########>                   |  33.83%

bar = ProgressBar(100, time_format='hhh mmmin sss', bar_length=70, spinner_type='s')
# Progress: - |=======>         00h 00min 02s                  |  16.54%

bar = ProgressBar(100, bar_length=70, spinner_type='db')
# Progress: ⢈⡱ |===========>         00:04                     |  24.81%
```

See more [here](https://github.com/Yoskutik/awesome_progress_bar/blob/master/examples.py).
 
---

Feel free to suggest ideas to improve this package in the GitHub's Issues section.

![](https://img.shields.io/badge/@Yoskutik-444?logo=github&style=flat-square) 