#!/usr/bin/env python3

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2019 NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Utility for "cylc cat-state" and "cylc dump"."""


def dump_to_stdout(states, sort_by_cycle=False):
    """Print states in "cylc dump" format to STDOUT.

    states = {
        "task_id": {
            "name": name,
            "label": point,
            "state": state,
            "spawned": True|False},
        # ...
    }
    """
    lines = []
    for item in states.values():
        if item['spawned'] in [True, "True", "true"]:
            spawned = 'spawned'
        else:
            spawned = 'unspawned'
        if sort_by_cycle:
            values = [item['label'], item['name'], item['state'], spawned]
        else:
            values = [item['name'], item['label'], item['state'], spawned]
        lines.append(', '.join(values))

    lines.sort()
    for line in lines:
        print(line)
