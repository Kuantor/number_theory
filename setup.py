"""Build script: compile the Cython core into a native extension.

Package metadata lives in ``pyproject.toml``; this file only declares the
compiled extension so the ``.pyx`` source is turned into a binary and left
out of the wheel.
"""
from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("number_theory._core", ["number_theory/_core.pyx"]),
]

setup(
    ext_modules=cythonize(
        extensions,
        # Emit the generated C outside the package tree so it never lands in
        # the wheel — only the compiled binary ships.
        build_dir="build/cython",
        compiler_directives={"language_level": "3"},
    ),
)
