import argparse
import logging

import sys
from time import sleep

from tqdm import tqdm


def arguments(args=None):
    parser = argparse.ArgumentParser(description='Export all googlegroups messages.')
    parser.add_argument('group', help='Group name on the url.')
    parser.add_argument('-m', '--mode', choices=['csv', 'mbox'], default='mbox',
                        help='Export topic list to csv or all messages to mbox.')
    parser.add_argument('-c', '--cookies', help='Cookie header string.')
    parser.add_argument('-d', '--cachedir', default='webcache', dest='cache_dir')
    parser.add_argument('-t', '--cachedays', type=int, default=7, dest='cache_days')
    parser.add_argument('-f', '--cacheforever', action='store_true', default=False, dest='cache_forever')
    parser.add_argument('-w', '--workers', type=int, default=10)
    parser.add_argument('-v', '--verbose', type=int, choices=[1, 2], default=1)

    return parser.parse_args(args)


def verbosity(level):
    if level < 2:
        return

    root = logging.getLogger()
    console = logging.StreamHandler(sys.stdout)
    root.addHandler(console)
    root.setLevel(logging.DEBUG)


class ProgressBar(tqdm):
    def update(self, progress=0, total=None):
        if self.disable:
            return

        if total and total != self.total:
            self.total = total

        assert progress >= self.n
        offset = progress - self.n
        if offset > 0:
            super().update(offset)


def progressbar():
    return ProgressBar(leave=True, bar_format='[{elapsed}] {n_fmt} downloads from {total_fmt} requests')


def export_with_progress(exporter, group_name):
    exporter.export(group_name)

    with progressbar() as bar:
        for progress, total in exporter:
            bar.update(progress, total)

            sleep(0.01)

    print(exporter)

    exporter.close()
