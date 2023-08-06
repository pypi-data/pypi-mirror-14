from setuptools import setup, Command


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name = "gflow",
    packages = ["gflow"],
    scripts = ["scripts/gflow"],
    version = "0.1",
    description = "Command line tool for running Galaxy workflows.",
    long_description = long_descr,
    author = "Alex MacLean",
    author_email = "maclean199@gmail.com",
    url = "https://github.com/AAFC-MBB/gflow",
    download_url = "https://github.com/AAFC-MBB/gflow/archive/0.1.tar.gz",
    keywords = ['Galaxy', 'Workflow', 'Python', 'Bioblend'],
    cmdclass = {'test': PyTest},
)
