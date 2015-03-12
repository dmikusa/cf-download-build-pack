import shutil
import tempfile
import os.path
import json
from nose.tools import eq_
from build_pack_utils import BuildPack


class BaseTestCompile(object):
    def initialize(self, app):
        self.build_dir = tempfile.mkdtemp(prefix='build-')
        self.cache_dir = tempfile.mkdtemp(prefix='cache-')
        os.rmdir(self.build_dir)  # delete otherwise copytree complains
        os.rmdir(self.cache_dir)  # cache dir does not exist normally
        shutil.copytree('tests/data/%s' % app, self.build_dir)

    def copy_build_pack(self, bp_dir):
        # simulate clone, makes debugging easier
        os.rmdir(bp_dir)
        shutil.copytree('.', bp_dir,
                        ignore=shutil.ignore_patterns(".git",
                                                      "binaries",
                                                      "env",
                                                      "tests"))

    def cleanup(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        for name in os.listdir(os.environ['TMPDIR']):
            if name.startswith('httpd-') and name.endswith('.gz'):
                os.remove(os.path.join(os.environ['TMPDIR'], name))
            if name.startswith('nginx-') and name.endswith('.gz'):
                os.remove(os.path.join(os.environ['TMPDIR'], name))
            if name.startswith('php-') and name.endswith('.gz'):
                os.remove(os.path.join(os.environ['TMPDIR'], name))

    def assert_exists(self, *args):
        eq_(True, os.path.exists(os.path.join(*args)),
            "Does not exists: %s" % os.path.join(*args))


class TestApp1(BaseTestCompile):
    def setUp(self):
        BaseTestCompile.initialize(self, 'app-1')

    def tearDown(self):
        BaseTestCompile.cleanup(self)

    def test_setup(self):
        eq_(True, os.path.exists(self.build_dir))
        eq_(False, os.path.exists(self.cache_dir))

    def test_compile(self):
        bp = BuildPack({
            'BUILD_DIR': self.build_dir,
            'CACHE_DIR': self.cache_dir
        }, '.')
        self.copy_build_pack(bp.bp_dir)
        try:
            output = ''
            output = bp._compile()
            self.assert_exists(self.build_dir, 'snake')
            self.assert_exists(self.build_dir, 'snake', 'snake.html')
            self.assert_exists(self.build_dir, '.bp')
            self.assert_exists(self.build_dir, '.procs')
            self.assert_exists(self.build_dir, 'start.sh')
            # check release command
            with open(os.path.join(self.build_dir, '.procs')) as fp:
                procs = [l.strip() for l in fp.readlines()]
            eq_(1, len(procs))
            eq_(True, procs[0].startswith('web:'))
        except Exception, e:
            print str(e)
            if hasattr(e, 'output'):
                print e.output
            if output:
                print output
            raise
        finally:
            if os.path.exists(bp.bp_dir):
                shutil.rmtree(bp.bp_dir)

class TestApp2(BaseTestCompile):
    def setUp(self):
        BaseTestCompile.initialize(self, 'app-2')

    def tearDown(self):
        BaseTestCompile.cleanup(self)

    def test_setup(self):
        eq_(True, os.path.exists(self.build_dir))
        eq_(False, os.path.exists(self.cache_dir))

    def test_compile(self):
        bp = BuildPack({
            'BUILD_DIR': self.build_dir,
            'CACHE_DIR': self.cache_dir
        }, '.')
        self.copy_build_pack(bp.bp_dir)
        try:
            output = ''
            output = bp._compile()
            self.assert_exists(self.build_dir, 'META-INF')
            self.assert_exists(self.build_dir, 'WEB-INF')
            self.assert_exists(self.build_dir, '.bp')
            self.assert_exists(self.build_dir, '.profile.d/bp_env_vars.sh')
            self.assert_exists(self.build_dir, '.procs')
            self.assert_exists(self.build_dir, '.java-buildpack')
            self.assert_exists(self.build_dir, '.java-buildpack.log')
            self.assert_exists(self.build_dir, 'start.sh')
            # check release command
            with open(os.path.join(self.build_dir, '.procs')) as fp:
                procs = [l.strip() for l in fp.readlines()]
            eq_(1, len(procs))
            eq_(True, procs[0].startswith('web:'))
            eq_(True, procs[0].find('http.port=$PORT') >= 0)
            eq_(True, procs[0].find('MetaspaceSize=64M') >= 0)
            eq_(True, procs[0].find('OnOutOfMemoryError') >= 0)
        except Exception, e:
            print str(e)
            if hasattr(e, 'output'):
                print e.output
            if output:
                print output
            raise
        finally:
            if os.path.exists(bp.bp_dir):
                shutil.rmtree(bp.bp_dir)

class TestApp3(BaseTestCompile):
    def setUp(self):
        BaseTestCompile.initialize(self, 'app-3')

    def tearDown(self):
        BaseTestCompile.cleanup(self)

    def test_setup(self):
        eq_(True, os.path.exists(self.build_dir))
        eq_(False, os.path.exists(self.cache_dir))

    def test_compile(self):
        bp = BuildPack({
            'BUILD_DIR': self.build_dir,
            'CACHE_DIR': self.cache_dir
        }, '.')
        self.copy_build_pack(bp.bp_dir)
        try:
            output = ''
            output = bp._compile()
            self.assert_exists(self.build_dir, 'httpd')
            self.assert_exists(self.build_dir, 'php')
            self.assert_exists(self.build_dir, 'htdocs')
            self.assert_exists(self.build_dir, '.bp')
            self.assert_exists(self.build_dir, '.profile.d/bp_env_vars.sh')
            self.assert_exists(self.build_dir, '.procs')
            self.assert_exists(self.build_dir, 'start.sh')
            # check release command
            with open(os.path.join(self.build_dir, '.procs')) as fp:
                procs = [l.strip() for l in fp.readlines()]
            eq_(3, len(procs))
            eq_(True, procs[0].startswith('httpd:'))
            eq_(True, procs[1].startswith('php-fpm:'))
            eq_(True, procs[2].startswith('web:'))
        except Exception, e:
            print str(e)
            if hasattr(e, 'output'):
                print e.output
            if output:
                print output
            raise
        finally:
            if os.path.exists(bp.bp_dir):
                shutil.rmtree(bp.bp_dir)
