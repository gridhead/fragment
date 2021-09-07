"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

from click import style, echo


class StatusDecorator(object):
    def __init__(self):
        self.PASS = style("[ \u2713 ]", fg="green", bold=True)
        self.FAIL = style("[ \u2717 ]", fg="red", bold=True)
        self.WARN = style("[ ! ]", fg="yellow", bold=True)
        self.HEAD = style("[ \u2605 ]", fg="magenta", bold=True)
        self.STDS = "     "

    def success(self, request_message):
        echo(self.PASS + " " + request_message)

    def failure(self, request_message):
        echo(self.FAIL + " " + request_message)

    def warning(self, request_message):
        echo(self.WARN + " " + request_message)

    def section(self, request_message):
        echo(self.HEAD + " " + style(request_message, fg="magenta", bold=True))

    def general(self, request_message):
        echo(self.STDS + " " + request_message)
