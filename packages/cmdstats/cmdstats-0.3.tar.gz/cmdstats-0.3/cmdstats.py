# -*- coding: utf-8 -*-
'''
File Name: cmdstats.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 2015年07月12日 星期日 20时45分02秒
'''
from __future__ import division

import abc
import commands
import argparse
import os
import sys
import time
import traceback
import collections

reload(sys)
sys.setdefaultencoding("utf-8")

__version__ = '0.3'

class ParseHistoryFile(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, filepath):
        self.filepath = filepath

    @abc.abstractmethod
    def parse_line(self, line):
        """Return line object"""

    @abc.abstractmethod
    def validate(self):
        """Return True if the filepath is valid."""

    def parse_lines(self):
        obs = []
        if not self.validate():
            return obs

        with open(self.filepath, 'r') as f:
            for line in f.readlines():
                try:
                    ob = self.parse_line(line.strip().encode("utf-8"))
                    obs.append(ob)
                except Exception as e:
                    continue
        return obs

class ParseZshHistoryFile(ParseHistoryFile):
    """Parse to history file of zsh"""

    def validate(self):
        if 'zsh' in self.filepath:
            return True
        return False

    def parse_line(self, line):
        ob = {}
        status = line.split(';')[0]
        command_full = ';'.join(line.split(';')[1:])
        ob["command"] = command_full.split(' ')[0]
        ob["run_time"] = status.split(':')[1]
        ob["status"] = status.split(':')[2]
        return ob


class ParseBashHistoryFile(ParseHistoryFile):
    """Parse to history file of bash"""

    def validate(self):
        if 'bash' in self.filepath:
            return True
        return False
    
    def parse_line(self, line):
        ob = {}
        ob["command"] = line.strip().split(' ')[0]
        return ob


parses = (ParseZshHistoryFile, ParseBashHistoryFile)


def stats(obs, limit=20):
    count = collections.Counter([o["command"] for o in obs])
    orders = collections.OrderedDict(
            sorted(count.items(), key=lambda t: t[1], reverse=True))
    shows = orders.items()[0:limit]
    
    number = 0
    data = []
    for cmd, cut in shows:
        number += 1
        data.append((number, 
            cmd[0:40] + '~' if len(cmd) > 40 else cmd, 
            round(cut / len(obs) * 100, 5), cut)) 
    return data


def show(data):
    message = ""
    for n, c, b, cmd in data:
        message += "%s\t%s\t%s%%\t%s\n" % (n, c, b, cmd.__repr__().strip("'"))
    return commands.getoutput("""echo '%s' | column -t """ % message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int,
            default=20, help="显示条数""[default: %(default)s]")
    args = parser.parse_args()
    
    home_dir = os.environ.get("HOME", None)
    if home_dir is None:
        raise Exception("No $HOME variable.")

    files = os.listdir(home_dir)
    
    obs = []
    for file in files:
        file = os.path.join(home_dir, file)
        if not file.endswith('history'):
            continue
        for parse in parses:
            p = parse(file)
            obs += p.parse_lines()

    data = stats(obs, limit=args.limit)
    sys.stdout.write(show(data) + '\n')


if __name__ == '__main__':
    main()
