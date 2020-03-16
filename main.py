import os
import subprocess
import sys


def read_until(f, c):
    res = bytearray()
    more = f.read1()
    while len(more) > 0:
        for i in range(0, len(more)):
            if more[i] == 0:
                res.extend(more[0:i])
                return res, more[i+1:]
        res.extend(more)
        more = f.read1()
    eof = f.read()
    raise RuntimeError('ending symbol not found in %s!' % more)
    


class Tclsh:
    def __init__(self, shell_fname, script_name):
        self.proc = subprocess.Popen([shell_fname, script_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def close(self):
        self.proc.stdin.close()
        return self.proc.wait()

    def eval(self, cmd):
        cmd = cmd.encode('utf-8')
        self.proc.stdin.write(cmd)
        self.proc.stdin.write(b'\0')
        self.proc.stdin.flush()
        
        out, reminder = read_until(self.proc.stdout, 0)
        assert(len(reminder) == 0)
        err, reminder = read_until(self.proc.stderr, 0)
        assert(len(reminder) == 0)
        err_msg = err.decode('utf-8')
        return out.decode('utf-8'), err_msg[0:-1], int(err_msg[-1])
        






t = Tclsh('tclsh', './main.tcl')
out, err, code = t.eval(r"putaas {hello}")
print(out, err, code)
for i in range(0, 1000):
    out, err, code = t.eval(r"puts {hello}")
    print("out:%s\n" % out, "err:%s\n" % err, code)
    out, err, code = t.eval(r"putaas {hello}")
    print("out:%s\n" % out, "err:%s\n" % err, code)