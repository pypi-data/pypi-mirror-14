from math import sin, pi
from itertools import cycle


class Colorer(object):

    escseq = "\x1b["
    endseq = "\x1b[0m"
    format = "{0}38;5;{1}m{2}{3}"

    def __init__(self):
        self.palette = cycle(self.palette_generator())

    def palette_generator(self):
        return map(self.calculate_color, range(0, 6 * 7 - 1))

    def calculate_color(self, iteration):
        iteration *= 1.0 / 6
        r = int(3 * sin(iteration) + 3)
        g = int(3 * sin(iteration + 2 * pi/3) + 3)
        b = int(3 * sin(iteration + 4 * pi/3) + 3)
        return 36 * r + 6 * g + b + 16

    def color(self, string):
        return self.format.format(
            self.escseq, next(self.palette), string, self.endseq
        )

colorer = Colorer()


def pytest_report_teststatus(report):
    if report.when == 'call':
        if hasattr(report, 'wasxfail'):
            if report.skipped:
                return "xfailed", colorer.color(u"x"), "xfail"
            elif report.failed:
                return "xpassed", colorer.color("p"), "XPASS"
        if report.passed:
            letter = colorer.color(u".")
        elif report.skipped:
            letter = colorer.color(u"s")
        elif report.failed:
            letter = colorer.color(u"F")
        return report.outcome, letter, report.outcome.upper()
