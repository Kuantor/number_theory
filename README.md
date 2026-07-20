# number_theory

[![CI](https://github.com/Kuantor/number_theory/actions/workflows/ci.yml/badge.svg)](https://github.com/Kuantor/number_theory/actions/workflows/ci.yml)

Lightweight, **dependency-free** Python number-theory library whose core is
compiled to a **source-less binary** (Cython → `.pyd` / `.so`), so it can be
shipped and used without distributing the algorithm source.

> **Status: v0.2.0.** GCD / LCM (Euclidean algorithm) implemented, now shipped as
> stable-ABI (`abi3`) wheels — one wheel per OS runs on **CPython 3.11+**. See the
> [roadmap board](https://github.com/orgs/Kuantor/projects/10) for what's next
> (primality, factorization, totient, modular arithmetic, …).

📖 **New here? Read the [User Guide](docs/USER_GUIDE.md)** — install, CLI + Python
usage, and troubleshooting.

## Install

From a released wheel (compiled binary only — no source for the core). The wheels
use Python's stable ABI, so one `abi3` wheel per OS works on **CPython 3.11+**:

```bash
pip install number_theory-0.2.0-cp311-abi3-win_amd64.whl
```

Or build the wheel yourself (requires a C compiler — MSVC on Windows, gcc/clang elsewhere):

```bash
pip install build
python -m build --wheel
# -> dist/number_theory-<ver>-<py>-<platform>.whl
```

## Usage

### Python API

```python
import number_theory as nt

nt.gcd(12, 18)            # 6
nt.lcm(4, 6)             # 12
nt.gcd_many(12, 18, 24)  # 6
nt.lcm_many(4, 6, 8)     # 24
nt.extended_gcd(240, 46) # (2, -9, 47)  ->  240*-9 + 46*47 == 2
```

All functions operate on Python `int`, so they keep arbitrary precision
(correct for arbitrarily large numbers).

### Command line

Installing the wheel also provides a `number-theory` command:

```bash
number-theory gcd 12 18 24     # 6
number-theory lcm 4 6 8        # 24
number-theory egcd 240 46      # 2 -9 47   (g x y, with a*x + b*y = g)

# equivalently, without the console script:
python -m number_theory gcd 1071 462
```

## API

| Function | Description |
| --- | --- |
| `gcd(a, b)` | Greatest common divisor (non-negative; `gcd(0, 0) == 0`). |
| `lcm(a, b)` | Least common multiple (non-negative; `lcm(x, 0) == 0`). |
| `extended_gcd(a, b)` | Returns `(g, x, y)` with `a*x + b*y == g`. |
| `gcd_many(*nums)` | GCD of two or more integers. |
| `lcm_many(*nums)` | LCM of two or more integers. |

## How the "source-less binary" works

- The algorithms live in `number_theory/_core.pyx` (Cython).
- The build compiles that to a native extension `_core.<abi>.pyd` (or `.so`).
- The built **wheel ships only the compiled binary** plus thin wrapper modules
  (`__init__.py`, `__main__.py`) and type stubs — the `.pyx` and the generated
  `.c` are kept out of the wheel. Consumers get the functionality as a binary.

## Development

```bash
pip install build pytest
python -m build --wheel
pip install dist/*.whl
pytest tests/          # run from outside the repo root so the compiled wheel is imported
```

## License

MIT — see [LICENSE](LICENSE).
