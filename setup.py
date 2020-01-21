from subprocess import call

import setuptools
from setuptools import Command, find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


class RunTests(Command):
    description = "run tests"
    user_options = [
        ("container=", "c", "Container id"),
        ("no-warnings", "n", "Supress warnings"),
        ("no-coverage", "p", "Supress coverage"),
    ]

    def initialize_options(self):
        self.container = None
        self.no_coverage = False
        self.no_warnings = False

    def finalize_options(self):
        if self.container is None:
            raise Exception("Parameter --container is missing.")

    def run(self):
        cmd = ["docker", "exec", "-it", self.container, "env", "TERM=xterm", "py.test", "--verbose"]
        if not self.no_coverage:
            cmd += ["--cov=mystripeapp", "--cov-report", "term-missing:skip-covered"]
        if self.no_warnings:
            cmd += ["--disable-pytest-warnings"]
        errno = call(cmd)
        raise SystemExit(errno)


setuptools.setup(
    name="mystripeapp",
    version="0.0.0",
    author="Holden Rehg",
    description="Sample Flask + Stripe application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    packages=setuptools.find_packages(exclude=["docs", "tests*"]),
    python_requires=">=3.3",
    extras_require={"test": ["coverage", "pytest", "pytest-cov"]},
    cmdclass={"test": RunTests},
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
)
