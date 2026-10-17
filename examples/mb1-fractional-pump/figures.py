"""Generate the numerical figure data embedded in the two booklets.

Single-particle geometry only: band energies of h(k, phi) and Wannier centres
of the lowest band and of the composite lowest-two-band group (Resta projected
position operator on a finite ring).  No interacting dynamics is simulated.

Usage (beside the TeX files):  python3 figures.py
The script rewrites the block between the GENERATED-FIGURE-DATA markers in both
two booklets, so each .tex file stays self-contained.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
TEX_FILES = ("questions.tex", "solutions.tex")
BEGIN = "% ==== BEGIN GENERATED FIGURE DATA (figures.py) ===="
END = "% ==== END GENERATED FIGURE DATA ===="

K_MOD = -1.5          # modulation amplitude K/J used throughout the booklet
N_CELLS = 24          # ring size for the projected-position centres
STEPS_PER_PERIOD = 400


def hoppings(phi: float) -> np.ndarray:
    return 1 + K_MOD * np.cos(phi + 4 * np.pi * np.arange(5) / 5)


def bloch(k: float, phi: float) -> np.ndarray:
    t = hoppings(phi)
    h = np.zeros((5, 5), complex)
    for s in range(4):
        h[s + 1, s] = h[s, s + 1] = -t[s]
    h[0, 4] = -t[4] * np.exp(-1j * k)
    h[4, 0] = -t[4] * np.exp(1j * k)
    return h


def ring(phi: float) -> np.ndarray:
    size = 5 * N_CELLS
    t = hoppings(phi)
    h = np.zeros((size, size))
    for j in range(size):
        h[(j + 1) % size, j] -= t[j % 5]
        h[j, (j + 1) % size] -= t[j % 5]
    return h


def centres(phi: float, n_bands: int) -> np.ndarray:
    """Wannier centres (in cells) from the projected position operator."""
    size = 5 * N_CELLS
    _, vecs = np.linalg.eigh(ring(phi))
    occ = vecs[:, : n_bands * N_CELLS]
    phase = np.exp(2j * np.pi * np.arange(size) / size)
    lam = np.linalg.eigvals(occ.conj().T @ (phase[:, None] * occ))
    return np.sort(np.angle(lam) * size / (2 * np.pi) / 5)


def track(start: float, n_bands: int, periods: int) -> np.ndarray:
    phis = np.linspace(0, 2 * np.pi * periods, STEPS_PER_PERIOD * periods + 1)
    x, path = start, [start]
    for phi in phis[1:]:
        c = centres(phi, n_bands)
        cand = np.concatenate([c - N_CELLS, c, c + N_CELLS])
        x = cand[np.argmin(abs(cand - x))]
        path.append(x)
    return np.array(path)


def coords(ts: np.ndarray, xs: np.ndarray, stride: int) -> str:
    pts = [f"({t:.3f},{x:.4f})" for t, x in zip(ts[::stride], xs[::stride])]
    if (len(ts) - 1) % stride:
        pts.append(f"({ts[-1]:.3f},{xs[-1]:.4f})")
    return " ".join(pts)


def wannier_block() -> tuple[str, str, dict]:
    periods = 2
    ts = np.linspace(0, periods, STEPS_PER_PERIOD * periods + 1)
    c0 = centres(0.0, 2)
    followed = c0[np.argmin(abs(c0))]
    starts = [x for x in c0 if -2.3 < x < 1.6]
    lines, summary = [], {}
    for x0 in starts:
        path = track(x0, 2, periods)
        same_flavor = abs(((x0 - followed) + 0.5) % 1 - 0.5) < 1e-6
        style = "flavA" if same_flavor else "flavB"
        if abs(x0 - followed) < 1e-9:
            style = "followed"
            summary["composite_start"] = float(path[0])
            summary["composite_after_T"] = float(path[STEPS_PER_PERIOD])
            summary["composite_after_2T"] = float(path[-1])
        lines.append(f"\\addplot[{style}] coordinates {{{coords(ts, path, 8)}}};")
    single = track(centres(0.0, 1)[np.argmin(abs(centres(0.0, 1)))], 1, periods)
    summary["band1_shift_per_period"] = float(single[STEPS_PER_PERIOD] - single[0])
    single_line = f"\\addplot[followed] coordinates {{{coords(ts, single, 8)}}};"
    return "\n".join(lines), single_line, summary


def band_block() -> tuple[str, str, dict]:
    ks = np.linspace(-np.pi, np.pi, 73)
    ek = np.array([np.linalg.eigvalsh(bloch(k, 0.0)) for k in ks])
    k_lines = []
    for n in range(5):
        style = "lowband" if n < 2 else "highband"
        k_lines.append(f"\\addplot[{style}] coordinates {{{coords(ks / np.pi, ek[:, n], 1)}}};")
    phis = np.linspace(0, 2 * np.pi, 121)
    kgrid = np.linspace(-np.pi, np.pi, 41)
    env = np.array([[np.linalg.eigvalsh(bloch(k, p)) for k in kgrid] for p in phis])
    lo, hi = env.min(axis=1), env.max(axis=1)
    p_lines = []
    for n in range(5):
        fill = "lowfill" if n < 2 else "highfill"
        upper = coords(phis / np.pi, hi[:, n], 2)
        lower_pts = [f"({p:.3f},{e:.4f})" for p, e in zip((phis / np.pi)[::-2], lo[::-2, n])]
        p_lines.append(f"\\addplot[{fill}] coordinates {{{upper} {' '.join(lower_pts)}}} -- cycle;")
    summary = {
        "min_outer_gap": float((env[..., 2] - env[..., 1]).min()),
        "max_abs_E3": float(abs(env[..., 2]).max()),
        "min_inner_gap": float((env[..., 1] - env[..., 0]).min()),
    }
    return "\n".join(k_lines), "\n".join(p_lines), summary


def main() -> None:
    comp, single, wsum = wannier_block()
    kplot, phiplot, bsum = band_block()
    block = "\n".join([
        BEGIN,
        "% Single-particle geometry at K/J=-3/2; regenerate with figures.py.",
        f"\\newcommand{{\\FigDataComposite}}{{%\n{comp}\n}}",
        f"\\newcommand{{\\FigDataBandOne}}{{%\n{single}\n}}",
        f"\\newcommand{{\\FigDataBandsK}}{{%\n{kplot}\n}}",
        f"\\newcommand{{\\FigDataBandsPhi}}{{%\n{phiplot}\n}}",
        END,
    ])
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    for name in TEX_FILES:
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text()
        if BEGIN not in text:
            raise SystemExit(f"marker missing in {name}")
        path.write_text(pattern.sub(lambda _: block, text))
    summary = {**wsum, **bsum}
    for key, value in summary.items():
        print(f"{key:28s} {value: .4f}")
    assert abs(summary["band1_shift_per_period"] - 2) < 1e-3
    assert abs(summary["composite_after_2T"] - summary["composite_start"] + 1) < 1e-3
    assert summary["min_outer_gap"] > 7 / 5


if __name__ == "__main__":
    main()
