import unittest
import time
import io
import re
from unittest.mock import patch
from awesome_progress_bar import ProgressBar


class TestNonThreadMode(unittest.TestCase):
    def test_prefix(self):
        with patch('sys.stdout', new=io.StringIO()) as out:
            total = 3
            bar = ProgressBar(total, use_thread=False)
            for x in range(total):
                bar.iter()
                self.assertTrue(out.getvalue().split('\r')[-1].startswith(bar.prefix))

    def test_suffix(self):
        with patch('sys.stdout', new=io.StringIO()) as out:
            total = 3
            bar = ProgressBar(total, use_thread=False)
            for x in range(total):
                bar.iter()
                self.assertTrue(out.getvalue().split('\r')[-1].endswith(bar.suffix))

    def test_length(self):
        def case(**kwargs):
            bar = ProgressBar(total, bar_length=length, use_thread=False, **kwargs)
            for x in range(total):
                bar.iter()
                printed = out.getvalue().split('\r')[-1].rstrip(bar._last_char)
                self.assertEqual(len(printed), length)

        total = 3
        length = 70

        with patch('sys.stdout', new=io.StringIO()) as out:
            case()
            case(prefix='Pre-pre-fixik', suffix='Suf-suf-suxik')
            case(use_time=True, use_eta=True)
            case(spinner_type='db', time_format='hh hours, mm minutes, ss seconds')
            case(last_char='qwe', use_time=False)

    def test_eta(self):
        with patch('sys.stdout', new=io.StringIO()) as out:
            bar = ProgressBar(300, use_thread=False, use_eta=True)
            for x in range(3):
                time.sleep(0.2)
                bar.iter()
            eta = re.findall(r'\d\d:\d\d', out.getvalue())[1]
            self.assertTrue(eta in [f'01:0{x}' for x in range(5)])

            bar = ProgressBar(5, use_eta=True, eta_format='hh hours, mm minutes, ss seconds', use_thread=False)
            bar.iter()
            self.assertTrue('/00 hours, 00 minutes, 00 seconds' in out.getvalue())

    def test_time(self):
        with patch('sys.stdout', new=io.StringIO()) as out:
            bar = ProgressBar(5, time_format='hh hours, mm minutes, ss seconds', use_thread=False)
            bar.iter()
            self.assertTrue('00 hours, 00 minutes, 00 seconds' in out.getvalue())
            bar = ProgressBar(5, time_format='hh hours, mm minutes, ss seconds', use_thread=False, use_eta=True)
            bar.iter()
            self.assertTrue('00 hours, 00 minutes, 00 seconds/00 hours, 00 minutes, 00 seconds' in out.getvalue())


if __name__ == '__main__':
    unittest.main()
