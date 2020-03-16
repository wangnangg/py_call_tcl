import os
import subprocess
import sys


def read_until(f, c):
    res = bytearray()
    max_read = 256
    more = f.read1(max_read)
    while len(more) > 0:
        for i in range(0, len(more)):
            if more[i] == 0:
                res.extend(more[0:i])
                return res, more[i+1:]
        res.extend(more)
        more = f.read1(max_read)
    eof = f.read()
    raise RuntimeError('ending symbol not found in %s!' % more)
    


class Tcl:
    def __init__(self, shell_fname):
        proxy_script = os.path.join(os.path.dirname(__file__), 'main.tcl')
        self.proc = subprocess.Popen([shell_fname, proxy_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        




if __name__ == '__main__':
    t = Tcl('tclsh')
    print('--expecting error---')
    out, err, code = t.eval(r"putaas {hello}")
    print("out:%s\nerr:%s\ncode:%d\n" % (out, err, code))
    print('--expecting hello---')
    out, err, code = t.eval(r"puts {hello}")
    print("out:%s\nerr:%s\ncode:%d\n" % (out, err, code))
