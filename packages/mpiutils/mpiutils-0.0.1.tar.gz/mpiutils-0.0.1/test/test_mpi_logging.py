from nose.tools import assert_in, assert_equal
from tempfile import gettempdir
import logging
from socket import gethostname
from shutil import rmtree
import os
import sys

from mpiutils import masterworker
from mpiutils import mpi_logging

class TestIO(object):
    def setup(self):
        self.tempdir = os.path.join(gettempdir(), 'test_io')
        masterworker.checkmakedirs(self.tempdir)
        self.tempfilename = os.path.join(self.tempdir, 'tempfile')

    def teardown(self):
        try:
            rmtree(self.tempdir)
        except OSError:
            pass

    def test_io(self):
        tempfilename = self.tempfilename
        tempfile = mpi_logging.open(tempfilename, mode='w')
        tempfile.write(str(masterworker.rank())+'\n')
        tempfile.flush()
        contents = ''
        with open(tempfilename) as stillopen:
            contents = stillopen.read()
        assert_in(str(masterworker.rank())+'\n', contents)
        tempfile.close()
        with open(tempfilename) as nowclosed:
            ranks = [int(s.strip()) for s in nowclosed]
        assert_equal(set(ranks), set(range(masterworker.size())))
        tempfile = mpi_logging.open(tempfilename, 'a')
        tempfile.write(str(masterworker.rank())+'\n')
        tempfile.close()
        with open(tempfilename) as nowclosed:
            ranks = [int(s.strip()) for s in nowclosed]
        assert_equal(len(ranks), masterworker.size()*2)
        assert_equal(set(ranks), set(range(masterworker.size())))
        if masterworker.size() != 1:
            masterworker._comm.Barrier()

class TestMPIFileHandler(object):
    def setup(self):
        self.tempdir = os.path.join(gettempdir(), 'test_MPIFileHandler')
        masterworker.checkmakedirs(self.tempdir)
        self.tempfilename = os.path.join(self.tempdir, 'tempfile')

    def teardown(self):
        try:
            rmtree(self.tempdir)
        except OSError:
            pass

    def test_MPIFileHandler(self):
        tempfilename = self.tempfilename
        handler = mpi_logging.MPIFileHandler(tempfilename, 'w')
        host = gethostname()
        formatter = logging.Formatter(host+':%(message)s')
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        logging.warn('TEST')
        logging.getLogger().removeHandler(handler)
        handler.flush()
        handler.close()
        lines = {}
        with open(tempfilename) as tempfile:
            lines = set(tempfile.readlines())
        assert_equal(lines, set([host+':TEST\n']))
        if masterworker.size() != 1:
            masterworker._comm.Barrier()


def main():
    tester = TestIO()
    tester.setup()
    try:
        tester.test_io()
    finally:
        tester.teardown()
    tester = TestMPIFileHandler()
    tester.setup()
    try:
        tester.test_MPIFileHandler()
    finally:
        tester.teardown()

if __name__ == '__main__':
    sys.exit(main())

