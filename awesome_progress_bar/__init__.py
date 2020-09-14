import time
import threading
import shutil


class ProgressBar:
    """
    An awesome console progress bar. ProgressBar have 2 mods of work. I recommend
    to run it in the thread mode. This way progress bar would have constant FPS.

    Attention!
    In case you are using thread mode be aware you are excepting KeyboardInterrupt
    exception:

    bar = ProgressBar(100)
    try:
        bar.iter()
    except KeyboardInterrupt:
        bar.stop()
    """
    _spinner_states = ('⠁ |⠉ |⠉⠁|⠈⠉| ⠙| ⠸| ⢰| ⣠|⢀⣀|⣀⡀|⣄ |⡆ |⠇ |⠃ |'
                      '⠁ |⠉ |⠉⠁|⠈⠉| ⠙| ⠸| ⢰| ⣠|⢀⣀|⣀⡀|⣄ |⡆ |⠇ |⠃ |'
                      '⠁ |⠉ |⠈⠁|⠈⠑|⠈⠱|⠈⡱|⢈⡱|⢌⡱|⢎⡱|⢎⡱|⢎⡱|'
                      '⢆⡱|⢆⡰|⢆⡠|⢆⡀|⢆ |⠆ |⠂ |  ').split('|')

    def __init__(self,
                 total,
                 prefix='Progress',
                 suffix='Complete',
                 fill='=',
                 bar_length=None,
                 update_period=0.1,
                 use_time=True,
                 time_format='mm:ss',
                 use_thread=True):
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
        """
        self.total = total
        self.prefix = f'{prefix}: ' if prefix else ''
        self.suffix = f' {suffix}' if suffix else ''
        self.bar_length = bar_length if bar_length else min(shutil.get_terminal_size((101, 0)).columns - 1, 100)
        self.update_period = update_period
        self.stopped = False
        self.use_time = use_time
        self.time_format = time_format

        self._initial_time = time.time()
        self._iteration = 0
        self._fill = fill
        self._spinner_index = 0
        self._use_thread = use_thread
        self._time_passed = ''

        if self._use_thread:
            self._thread = threading.Thread(target=self._tick_n_print)
            self._thread.start()

    def _tick_n_print(self):
        while not self.stopped:
            self._time_passed = self._get_time_passed()
            progress = self._get_progress_string()
            if self._iteration != self.total:
                print(f'\r{progress}', end='')
            else:
                print(f'\r{progress}')
                self.stop()
            time.sleep(self.update_period)

    def _get_time_passed(self):
        now = time.time()
        diff = int(now - self._initial_time)
        s = f'{diff % 60:0>2}'
        m = f'{diff // 60 % 60:0>2}'
        h = f'{diff // 60 // 60:0>2}'
        return self.time_format.replace('hh', h).replace('mm', m).replace('ss', s)

    def _get_progress_string(self):
        percent = f"{100 * self._iteration / self.total:>6.2f}"
        length = self.bar_length - len(self.prefix) - len(percent) - len(self.suffix) - 7
        filled_length = int(length * self._iteration // self.total)
        bar = self._fill * filled_length + ('>' if filled_length + 1 <= length else '') + \
            ' ' * (length - filled_length - 1)
        if self.use_time:
            n = int((len(bar) - len(self._time_passed) - 2) / 2)
            bar = f'{bar[:n]} {self._time_passed} {bar[n + len(self._time_passed) + 2:]}'

        spinner = ProgressBar._spinner_states[self._spinner_index]
        self._spinner_index = (self._spinner_index + 1) % len(ProgressBar._spinner_states)
        return f'{self.prefix}{spinner} |{bar}| {percent}%{self.suffix}'

    def iter(self):
        """
        If in thread process just increases the iteration.
        Otherwise increases it and prints the string.
        """
        self._iteration += 1
        if not self._use_thread:
            self._time_passed = self._get_time_passed()
            progress = self._get_progress_string()
            print(f'\r{progress}', end='' if self._iteration < self.total else '\n')

    def stop(self):
        """
        Stops the bar. There's no need to use it without thread mode.
        """
        self.stopped = True
        if self._iteration < self.total:
            print()
