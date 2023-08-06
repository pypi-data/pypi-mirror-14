#!/usr/bin/env python
import sys, os
from bisect import bisect_right, insort_right
from walt.common.evloop import EventLoop
from walt.node.const import SERVER_LOGS_FIFO

"""
Read a serial device connected to a sensor mote and
manage logs.
The sensor mote should define a set of logging
statements using LOGDEF directives, and optionaly
a set of variables using LOGVAR.
Then, serial log lines matching the LOGDEF directives
will be formatted appropriately and forwarded to the
walt log engine.

Directives format:
LOGDEF <logstream> <prefix> <separator> <py-format-str>
LOGVAR <var-name> <value>

Example:
[...]
LOGDEF vizwalt ;T: : {nodeid}:TxStart:{}
LOGVAR nodeid af4e
[...]
;T:aabbccddeeff
[...]
;T:gghhiijjkkll

This will cause the following walt log entries:

stream   line
------   ----
vizwalt  af4e:TxStart:aabbccddeeff
vizwalt  af4e:TxStart:gghhiijjkkll

"""
class SensorLogsMonitor(object):
    def __init__(self, serial_dev_path):
        self.f = open(serial_dev_path, 'r', 0)
        self.logs_out = open(SERVER_LOGS_FIFO, 'w')
        self.logdefs = []
        self.logvars = {}

    # let the event loop know what we are reading on
    def fileno(self):
        return self.f.fileno()

    # when the event loop detects an event for us,
    # read the log line and process it
    def handle_event(self, ts):
        rawline = self.f.readline()
        if rawline == '':  # empty read
            return False # remove from loop => exit
        rawline = rawline.strip()
        words = rawline.split()
        if len(words) == 0:
            return
        first = words[0]
        if first == 'LOGDEF':
            prefix = words[2]
            logdef = (prefix, dict(
                        stream = words[1],
                        sep = words[3],
                        formatting = ' '.join(words[4:])))
            insort_right(self.logdefs, logdef)
        elif first == 'LOGVAR':
            self.logvars[words[1]] = words[2]
        elif len(self.logdefs) > 0:
            # adding a char ('*') ensures that i will point
            # after the matching prefix, even if (rawline == prefix)
            i = bisect_right(self.logdefs, (rawline + '*',))
            if i > 0 and rawline.startswith(self.logdefs[i-1][0]):
                d = self.logdefs[i-1][1]
                self.forward_log(ts=ts, rawline=rawline, **d)
    def forward_log(self, ts, rawline, stream, sep, formatting):
        logargs = rawline.split(sep)[1:]
        logline = formatting.format(*logargs, **self.logvars)
        logout = 'TSLOG %(ts)f %(stream)s %(line)s\n' % dict( \
            ts = ts,
            stream = stream,
            line = logline
        )
        print logout.strip()
        self.logs_out.write(logout)
        self.logs_out.flush()

    def close(self):
        self.logs_out.close()
        self.f.close()

def run():
    if len(sys.argv) != 2:
        print 'Usage: %s <serial_dev_path>' % sys.argv[0]
        sys.exit()
    serial_dev_path = sys.argv[1]
    if not os.path.exists(serial_dev_path):
        print 'No such file of directory: %s' % serial_dev_path
        sys.exit()
    sensor_logs_monitor = SensorLogsMonitor(serial_dev_path)
    ev_loop = EventLoop()
    ev_loop.register_listener(sensor_logs_monitor)
    ev_loop.loop()

if __name__ == "__main__":
    run()

