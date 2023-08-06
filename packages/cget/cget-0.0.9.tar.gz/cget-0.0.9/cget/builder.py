import click, os, multiprocessing

import cget.util as util

class Builder:
    def __init__(self, prefix, top_dir, exists=False):
        self.prefix = prefix
        self.top_dir = top_dir
        self.build_dir = self.get_path('build')
        self.exists = exists

    def get_path(self, *args):
        return os.path.join(self.top_dir, *args)

    def get_build_path(self, *args):
        return self.get_path('build', *args)

    def is_make_generator(self):
        return os.path.exists(self.get_build_path('Makefile'))

    def cmake(self, options=None, use_toolchain=False, **kwargs):
        if use_toolchain: self.prefix.cmd.cmake(options=util.merge({'-DCMAKE_TOOLCHAIN_FILE': self.prefix.toolchain}, options), **kwargs)
        else: self.prefix.cmd.cmake(options=options, **kwargs)

    def fetch(self, url):
        self.prefix.log("fetch:", url)
        f = util.retrieve_url(url, self.top_dir)
        if os.path.isfile(f):
            click.echo("Extracting archive {0} ...".format(f))
            util.extract_ar(archive=f, dst=self.top_dir)
        return next(util.get_dirs(self.top_dir))

    def configure(self, src_dir, defines=[], install_prefix=None):
        self.prefix.log("configure")
        util.mkdir(self.build_dir)
        args = [src_dir]
        if install_prefix is not None: args.insert(0, '-DCMAKE_INSTALL_PREFIX=' + install_prefix)
        for d in defines:
            args.append('-D{0}'.format(d))
        self.cmake(args=args, cwd=self.build_dir, use_toolchain=True)

    def build(self, target=None, config=None, cwd=None):
        self.prefix.log("build")
        args = ['--build', self.build_dir]
        if config is not None: args.extend(['--config', config])
        if target is not None: args.extend(['--target', target])
        if self.is_make_generator(): 
            args.extend(['--', '-j', str(multiprocessing.cpu_count())])
            if self.prefix.verbose: args.append('VERBOSE=1')
        self.cmake(args=args, cwd=cwd)

    def test(self, config='Release'):
        self.prefix.log("test")
        util.try_until(
            lambda: self.build(target='check', config=config),
            lambda: self.prefix.cmd.ctest((self.prefix.verbose and ['-VV'] or []) + ['-C', config], cwd=self.build_dir)
        )
