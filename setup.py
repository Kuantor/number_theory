"""Build script: compile the Cython core into a native extension.

Package metadata lives in ``pyproject.toml``; this file only declares the
compiled extension so the ``.pyx`` source is turned into a binary and left
out of the wheel.
"""
from setuptools import Extension, setup
from Cython.Build import cythonize

# Build against CPython's stable ABI (limited API), 3.11+, so a single
# `*-abi3-*` wheel works on 3.11, 3.12, 3.13, 3.14, ... instead of one wheel
# per Python version. The matching wheel tag is set in setup.cfg.
LIMITED_API_VERSION = "0x030B0000"  # CPython 3.11

extensions = [
    Extension(
        "number_theory._core",
        ["number_theory/_core.pyx"],
        define_macros=[("Py_LIMITED_API", LIMITED_API_VERSION)],
        py_limited_api=True,
    ),
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
