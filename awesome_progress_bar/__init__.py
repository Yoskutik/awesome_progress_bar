import time
import threading
import shutil


class ProgressBar:
    _spinners = {
        'db': ('⠁ |⠉ |⠉⠁|⠈⠉| ⠙| ⠸| ⢰| ⣠|⢀⣀|⣀⡀|⣄ |⡆ |⠇ |⠃ |'
               '⠁ |⠉ |⠉⠁|⠈⠉| ⠙| ⠸| ⢰| ⣠|⢀⣀|⣀⡀|⣄ |⡆ |⠇ |⠃ |'
               '⠁ |⠉ |⠈⠁|⠈⠑|⠈⠱|⠈⡱|⢈⡱|⢌⡱|⢎⡱|⢎⡱|⢎⡱|'
               '⢆⡱|⢆⡰|⢆⡠|⢆⡀|⢆ |⠆ |⠂ |  ').split('|'),
        'sb': '⠁⠉⠙⠸⢰⣠⣄⡆⠇⠃',
        's': '|/-\\',
    }

    def __init__(self,
                 total,
                 prefix='Progress',
                 suffix='',
                 fill='=',
                 bar_length=None,
                 update_period=0.1,
                 use_time=True,
                 time_format='mm:ss',
                 use_thread=True,
                 spinner_type='sb',
                 use_spinner=True,
                 last_char='\n',
                 use_eta=False,
                 eta_format=None):
        """
        :param total: Total amount of iterations.
        :type total: int
        :param prefix: Short message that well be printed before the progress bar.
                       Default is 'Progress'.
        :type prefix: str
        :param suffix: Short message that well be printed after the progress bar.
                       Default is 'Complete'.
        :type suffix: str
        :param fill: A character that will be used as progress bar filler.
        :type fill: str
        :param bar_length: The length of the whole string (including prefix, spinner,
                           progress bar, percents and suffix). Default is equal to the
                           minimum between terminal's width and 100.
        :type bar_length: int
        :param update_period: The duration of pause between iterations in seconds.
                              Default is 0.1. Works only if use_thread is True.
        :type update_period: float
        :param use_time: If True there will be an information about elapsed time in the
                         center of the progress bar written in time_format format.
                         Default is True.
        :type use_time: bool
        :param time_format: String, that should include hh, mm or/and ss. hh will be
                            replaced with amount of elapsed hours, mm - minutes, ss -
                            seconds. Default is 'mm:ss'.
        :type time_format: str
        :param use_thread: If True ProgressBar will create extra thread.
        :type use_thread: bool
        :param spinner_type: One of ['sb', 'db', 's']. With 'sb' progress bar will print
        spinner consisting of 1 Braille pattern. 'db' - 2 Braille patterns. 's' - a slash
        Default is 'sb'.
        :type use_spinner: str
        :param use_spinner: If True the spinner will be shown.
        :type use_spinner: bool
        :param last_char: Something, that will be printed after the progress is done.
        Default is '\n'
        :type last_char: str
        :param use_eta: If True the information about approximate remaining time
        will be printed. Default is False.
        :type use_eta: bool
        :param eta_format: The format of ETA. Similar to the time_format. Default is
        equal to the time_format.
        :type eta_format: str
        """
        self.total = total
        self.prefix = f'{prefix}: ' if prefix else ''
        self.suffix = f' {suffix}' if suffix else ''
        self.bar_length = bar_length if bar_length else min(shutil.get_terminal_size((101, 0)).columns - 1, 100)
        self.update_period = update_period
        self.stopped = False
        self.use_time = use_time
        self.time_format = time_format
        self.use_eta = use_eta
        self.eta_format = eta_format if eta_format else time_format

        self._initial_time = time.time()
        self._iteration = 0
        self._fill = fill
        self._spinner_index = 0
        self._use_thread = use_thread
        self._time_passed = ''
        self._use_spinner = use_spinner
        self._spinner_states = ProgressBar._spinners[spinner_type]
        self._append = ''
        self._last_char = last_char
        self._eta = ''

        if self._use_thread:
            self._thread = threading.Thread(target=self._tick_n_print)
            self._thread.start()

    def __del__(self):
        self.stopped = True
        self._last_time = time.time()

    @staticmethod
    def _format_time_string(seconds, time_format):
        s = f'{seconds % 60:0>2}' if 'mm' in time_format or 'hh' in time_format else f'{seconds:0>2}'
        m = f'{seconds // 60 % 60:0>2}' if 'hh' in time_format else f'{seconds // 60:0>2}'
        h = f'{seconds // 60 // 60:0>2}'
        return h, m, s

    def _tick_n_print(self):
        while not self.stopped:
            self._time_passed = self.get_time_passed()
            progress = self._get_progress_string()
            if self._iteration != self.total:
                print(f'\r{progress}', end='')
            else:
                print(f'\r{progress}', end=self._last_char if self._iteration == self.total else '')
                self.stopped = True
                self._last_time = time.time()
            time.sleep(self.update_period)

    def get_time_passed(self, return_str=True):
        diff = (self._last_time if self.stopped else time.time()) - self._initial_time
        if not return_str:
            return diff
        diff = round(diff)
        h, m, s = self._format_time_string(diff, self.time_format)
        time_passed = self.time_format.replace('hh', h).replace('mm', m).replace('ss', s)
        if self.use_eta and 1 < self._iteration < self.total:
            return f'{time_passed}/{self._eta}'
        elif self.use_eta and self._iteration == 1:
            return f'{time_passed}/{self._eta}'
        else:
            return time_passed

    def _get_progress_string(self):
        percent = f"{100 * self._iteration / self.total:>6.2f}"

        if self._use_spinner and self._iteration < self.total:
            spinner = f'{self._spinner_states[self._spinner_index]} '
            self._spinner_index = (self._spinner_index + 1) % len(self._spinner_states)
        else:
            spinner = ''

        length = self.bar_length - len(self.prefix + percent + self.suffix + spinner) - 4
        filled_length = int(length * self._iteration // self.total)
        bar = self._fill * filled_length + ('>' if filled_length + 1 <= length else '') + \
            ' ' * (length - filled_length - 1)
        if self.use_time:
            n = int((len(bar) - len(self._time_passed) - 2) / 2)
            bar = f'{bar[:n]} {self._time_passed} {bar[n + len(self._time_passed) + 2:]}'

        return f'{self.prefix}{spinner}|{bar}| {percent}%{self.suffix}{self._append}'

    def iter(self, append=''):
        """
        If in thread process just increases the iteration.
        Otherwise increases it and prints the string.
        :param append: A string to append after the bar
        :type append: str
        """
        self._iteration += 1
        self._append = append

        if self.use_eta:
            diff = time.time() - self._initial_time
            total_needed = int(round(diff * self.total / self._iteration))
            h, m, s = self._format_time_string(total_needed, self.eta_format)
            self._eta = self.eta_format.replace("hh", h).replace("mm", m).replace("ss", s)

        if not self._use_thread:
            self._time_passed = self.get_time_passed()
            progress = self._get_progress_string()
            print(f'\r{progress}', end=self._last_char if self._iteration == self.total else '')

    def stop(self):
        """
        Stops the bar. There's no need to use it without thread mode.
        """
        if not self.stopped:
            self.stopped = True
            self._last_time = time.time()
            if self._iteration < self.total:
                print()
            self._thread.join()

    def wait(self):
        """
        Blocks the program until bar is dead.
        """
        if self._thread.is_alive():
            self._thread.join()
