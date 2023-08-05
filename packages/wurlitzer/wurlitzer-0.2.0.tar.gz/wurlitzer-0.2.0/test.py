# coding: utf-8
from __future__ import print_function

import io
import time
import mock

from wurlitzer import (
    libc, pipes, STDOUT, PIPE, c_stderr_p, c_stdout_p,
    sys_pipes, sys_pipes_forever,
    stop_sys_pipes,
    Wurlitzer,
)

def printf(msg):
    """Call C printf"""
    libc.printf((msg + '\n').encode('utf8'))

def printf_err(msg):
    """Cal C fprintf on stderr"""
    libc.fprintf(c_stderr_p, (msg + '\n').encode('utf8'))

def test_pipes():
    with pipes(stdout=PIPE, stderr=PIPE) as (stdout, stderr):
        printf(u"Hellø")
        printf_err(u"Hi, stdérr")
    
    assert stdout.read() == u"Hellø\n"
    assert stderr.read() == u"Hi, stdérr\n"

def test_pipe_bytes():
    with pipes(encoding=None) as (stdout, stderr):
        printf(u"Hellø")
        printf_err(u"Hi, stdérr")
    
    assert stdout.read() == u"Hellø\n".encode('utf8')
    assert stderr.read() == u"Hi, stdérr\n".encode('utf8')

def test_forward():
    stdout = io.StringIO()
    stderr = io.StringIO()
    with pipes(stdout=stdout, stderr=stderr) as (_stdout, _stderr):
        printf(u"Hellø")
        printf_err(u"Hi, stdérr")
        assert _stdout is stdout
        assert _stderr is stderr
    
    assert stdout.getvalue() == u"Hellø\n"
    assert stderr.getvalue() == u"Hi, stdérr\n"

def test_pipes_stderr():
    stdout = io.StringIO()
    with pipes(stdout=stdout, stderr=STDOUT) as (_stdout, _stderr):
        printf(u"Hellø")
        libc.fflush(c_stdout_p)
        printf_err(u"Hi, stdérr")
        assert _stdout is stdout
        assert _stderr is None
    
    assert stdout.getvalue() == u"Hellø\nHi, stdérr\n"

def test_flush():
    stdout = io.StringIO()
    w = Wurlitzer(stdout=stdout, stderr=STDOUT)
    with w:
        printf_err(u"Hellø")
        time.sleep(1)
        assert stdout.getvalue().strip() == u"Hellø"

def test_sys_pipes():
    stdout = io.StringIO()
    stderr = io.StringIO()
    with mock.patch('sys.stdout', stdout), mock.patch('sys.stderr', stderr), sys_pipes():
        printf(u"Hellø")
        printf_err(u"Hi, stdérr")
    
    assert stdout.getvalue() == u"Hellø\n"
    assert stderr.getvalue() == u"Hi, stdérr\n"

def test_redirect_everything():
    stdout = io.StringIO()
    stderr = io.StringIO()
    with mock.patch('sys.stdout', stdout), mock.patch('sys.stderr', stderr):
        sys_pipes_forever()
        printf(u"Hellø")
        printf_err(u"Hi, stdérr")
        stop_sys_pipes()
    assert stdout.getvalue() == u"Hellø\n"
    assert stderr.getvalue() == u"Hi, stdérr\n"


