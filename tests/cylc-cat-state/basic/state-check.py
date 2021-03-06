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
# -----------------------------------------------------------------------------

import os
import sqlite3
import sys
from cylc.cylc_subproc import procopen


def main(argv):

    if len(argv) != 2:
        print("Incorrect number of args", sys.stderr)
        sys.exit(1)

    sname = argv[0]
    rundir = argv[1]
    command = "cylc cat-state " + sname

    p = procopen(command, usesh=True, stdoutpipe=True, stderrpipe=True)
    state, err = (f.decode() for f in p.communicate())

    if p.returncode > 0:
        print(err, sys.stderr)
        sys.exit(1)

    db = (os.sep).join([rundir, sname, "log", "db"])
    cnx = sqlite3.Connection(db)
    cur = cnx.cursor()

    state = state.split("\n")
    states_begun = False

    qbase = "select status from task_states where name==? and cycle==?"

    error_states = []

    for line in state:
        if states_begun and line != '':
            line2 = line.split(':')
            task_and_cycle = line2[0].strip().split(".")
            status = line2[1].split(',')[0].strip().split("=")[1]
            # query db and compare result
            res = []
            try:
                cur.execute(qbase, [task_and_cycle[0], task_and_cycle[1]])
                next_ = cur.fetchmany()
                while next_:
                    res.append(next_[0])
                    next_ = cur.fetchmany()
            except Exception:
                sys.stderr.write("unable to query suite database\n")
                sys.exit(1)
            if not res[0][0] == status:
                error_states.append(
                    line + ": state retrieved " + str(res[0][0]))
        elif line == "Begin task states":
            states_begun = True

    cnx.close()

    if error_states:
        print(
            "The following task states were not consistent with the database:",
            sys.stderr
        )
        for line in error_states:
            print(line, sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
