"""Answer checks for the public example: picture data and teaching algebra.

No many-body time simulation is performed. Run beside the TeX files:
    python3 check_answers.py
Requires numpy and scipy. Document checks: ../../researchpho/scripts/check_booklets.py
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm, expm_frechet

import figures as fig

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261017)
results: dict = {}

def check(name: str, value: float, tol: float = 1e-10) -> None:
    results[name] = {"max_abs_error": float(value), "tolerance": float(tol), "passed": bool(value <= tol)}
    if value > tol:
        raise AssertionError((name, value, tol))


def comm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def herm(n: int) -> np.ndarray:
    a = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return (a + a.conj().T) / 2


# ---------------- pictures: single-particle geometry ----------------
c0 = fig.centres(0.0, 2)
start = c0[np.argmin(abs(c0))]
path = fig.track(start, 2, 2)
band1 = fig.track(fig.centres(0.0, 1)[np.argmin(abs(fig.centres(0.0, 1)))], 1, 1)
per = fig.STEPS_PER_PERIOD
results["pictures"] = {
    "band1_shift_per_period_cells": round(float(band1[-1] - band1[0]), 4),
    "flavor_shift_first_period_cells": round(float(path[per] - path[0]), 4),
    "flavor_shift_second_period_cells": round(float(path[2 * per] - path[per]), 4),
    "flavor_shift_two_periods_cells": round(float(path[-1] - path[0]), 4),
}
check("picture_band1_winding", abs(results["pictures"]["band1_shift_per_period_cells"] - 2), 1e-3)
check("picture_flavor_two_cycle_return", abs(results["pictures"]["flavor_shift_two_periods_cells"] + 1), 1e-3)
gaps = [np.linalg.eigvalsh(fig.bloch(k, p)) for k in np.linspace(-np.pi, np.pi, 61) for p in np.linspace(0, 2 * np.pi, 121)]
results["pictures"]["min_outer_gap_on_grid"] = round(float(min(e[2] - e[1] for e in gaps)), 4)
assert results["pictures"]["min_outer_gap_on_grid"] > 7 / 5

# ---------------- M.1: Fourier matrix ----------------
mx = 0.0
for _ in range(10):
    n_cells = 3
    phi = rng.uniform(-np.pi, np.pi)
    kval = rng.uniform(-2, 2)
    t = 1 + kval * np.cos(phi + 4 * np.pi * np.arange(5) / 5)
    H = np.zeros((5 * n_cells, 5 * n_cells), complex)
    for r in range(n_cells):
        for a in range(5):
            x = 5 * r + a
            y = (x + 1) % (5 * n_cells)
            H[y, x] -= t[a]
            H[x, y] -= t[a]
    ks = 2 * np.pi * np.arange(n_cells) / n_cells
    U = np.zeros_like(H)
    for r in range(n_cells):
        for m, k in enumerate(ks):
            for a in range(5):
                U[5 * r + a, 5 * m + a] = np.exp(1j * k * r) / np.sqrt(n_cells)
    expected = np.zeros_like(H)
    for m, k in enumerate(ks):
        b = np.zeros((5, 5), complex)
        for a in range(4):
            b[a + 1, a] = b[a, a + 1] = -t[a]
        b[0, 4] = -t[4] * np.exp(-1j * k)
        b[4, 0] = -t[4] * np.exp(1j * k)
        expected[5 * m:5 * m + 5, 5 * m:5 * m + 5] = b
    mx = max(mx, np.max(abs(U.conj().T @ H @ U - expected)))
check("M1_Fourier_matrix", mx)
results["M1_dimensions_N4"] = [math.comb(20, 4), math.comb(8, 4), 2 ** 4]

# ---------------- B.4: gauge covariance and determinant example ----------------
mx = 0.0
for _ in range(20):
    Y = np.linalg.qr(rng.normal(size=(5, 2)) + 1j * rng.normal(size=(5, 2)))[0]
    Lam = expm(-1j * herm(2))
    v = rng.normal(size=2) + 1j * rng.normal(size=2)
    v /= np.linalg.norm(v)
    v2, Y2 = Lam.conj().T @ v, Y @ Lam
    mx = max(mx, np.max(abs(Y2 @ Y2.conj().T - Y @ Y.conj().T)),
             np.max(abs(np.outer(Y2 @ v2, (Y2 @ v2).conj()) - np.outer(Y @ v, (Y @ v).conj()))))
check("B4_gauge_covariance", mx)
sx = np.array([[0, 1], [1, 0]], complex)
check("B4_determinant_counterexample", abs(np.linalg.det(1j * sx) - 1))

# ---------------- C.3: product frame ----------------
mx = 0.0
for _ in range(15):
    n, t0 = 5, rng.uniform(0.1, 1)
    A, H, B, C = herm(n), herm(n), 1j * herm(n), 1j * herm(n)
    Smat = 0.1 * (np.sin(t0) * B + np.cos(0.7 * t0) * C)
    dS = 0.1 * (np.cos(t0) * B - 0.7 * np.sin(0.7 * t0) * C)
    W = expm(-1j * A * t0)
    dW = -1j * A @ W
    Uc, dUc = expm_frechet(Smat, dS, compute_expm=True)
    U, dU = W @ Uc, dW @ Uc + W @ dUc
    direct = U.conj().T @ H @ U - 1j * U.conj().T @ dU
    Kw = W.conj().T @ H @ W - 1j * W.conj().T @ dW
    split = Uc.conj().T @ Kw @ Uc - 1j * Uc.conj().T @ dUc
    mx = max(mx, np.max(abs(direct - split)))
check("C3_product_frame", mx)

# ---------------- C.4: teaching chain ----------------
N, Jz, h, g = 4, 0.7, 0.2, 0.31
I2, sz = np.eye(2), np.diag([1.0, -1.0])


def embed(op: np.ndarray, j: int) -> np.ndarray:
    a = np.array([[1.0]])
    for k in range(N):
        a = np.kron(a, op if k == j else I2)
    return a


Z = [embed(sz, j) for j in range(N)]
X = [embed(sx, j) for j in range(N)]
H = -Jz * sum(Z[j] @ Z[(j + 1) % N] for j in range(N)) - h * sum(Z) - g * sum(X)
psi = np.zeros(2 ** N, complex)
psi[-1] = 1
res = (H - (-N * Jz + N * h) * np.eye(2 ** N)) @ psi
check("C4_source_norm", abs(np.vdot(res, res).real - N * g * g))
qj = (np.eye(2 ** N) + Z[0]) / 2
dt = 1e-5
psit = expm(-1j * H * dt) @ psi
check("C4_local_initial_coefficient", abs(np.vdot(psit, qj @ psit).real / dt ** 2 - g * g), 1e-8)

# ---------------- E.3: partial trace and difference equations ----------------
def ptr(a: np.ndarray) -> np.ndarray:
    return np.trace(a.reshape(2, 3, 2, 3), axis1=1, axis2=3)


mx = 0.0
for _ in range(20):
    Kx, Kb, Kbd, R = herm(2), herm(3), herm(6), herm(6)
    Kr = np.kron(Kx, np.eye(3)) + np.kron(np.eye(2), Kb) + Kbd
    states = []
    for _j in range(2):
        M = rng.normal(size=(6, 6)) + 1j * rng.normal(size=(6, 6))
        D = M @ M.conj().T
        states.append(D / np.trace(D))
    rho, sigma = states
    left = ptr(comm(Kr, sigma))
    right = comm(Kx, ptr(sigma)) + ptr(comm(Kbd, sigma))
    diff = comm(Kr + R, rho) - comm(Kr, sigma)
    mx = max(mx, np.max(abs(left - right)), np.max(abs(diff - (comm(Kr, rho - sigma) + comm(R, rho)))))
check("E3_local_and_difference_equations", mx)

# ---------------- F.1 and F.3 arithmetic ----------------
T, delta, delta0, eta, alpha, I0 = 1.0, 0.005, 0.001, 1e-5, 1e-5, 1.0
check("F1_t_cert_over_T", abs(T + (delta - delta0 - 2 * T * eta) / (2 * I0 * alpha * T) - 200), 1e-9)
choices = []
for value, error in [(-0.497, 0.001), (-0.494, 0.0015), (-0.494, 0.0005)]:
    d = abs(value + 0.5)
    choices.append("inside" if d + error <= delta else "outside" if d - error > delta else "undetermined")
assert choices == ["inside", "undetermined", "outside"]
results["F3_added_data_classification"] = choices
# ---------------- Appendix D: toolbox examples ----------------
sy = np.array([[0, -1j], [1j, 0]])
sz2 = np.diag([1.0, -1.0]).astype(complex)
id2 = np.eye(2)
mx = 0.0
for _ in range(10):  # 3-site ring with a seam: det h(k) = -2 t0 t1 t2 cos k
    t0, t1, t2, kval = rng.uniform(-2, 2, size=4)
    hk = -np.array([[0, t0, t2 * np.exp(-1j * kval)], [t0, 0, t1], [t2 * np.exp(1j * kval), t1, 0]])
    mx = max(mx, abs(np.linalg.det(hk) - (-2 * t0 * t1 * t2 * np.cos(kval))))
check("toolbox_three_site_seam_determinant", mx)
mx = 0.0
for n_cells in (4, 9):  # dimer ring: eigenvalues of P exp(2 pi i x/N) P
    pos = np.array([r + s_ / 2 for r in range(n_cells) for s_ in (0, 1)])
    hop = np.zeros((2 * n_cells, 2 * n_cells))
    for r in range(n_cells):
        hop[2 * r, 2 * r + 1] = hop[2 * r + 1, 2 * r] = -1.0
    vals, vecs = np.linalg.eigh(hop)
    low = vecs[:, vals < 0]
    proj = low.conj().T @ np.diag(np.exp(2j * np.pi * pos / n_cells)) @ low
    lam = np.sort_complex(np.linalg.eigvals(proj))
    want = np.sort_complex(np.cos(np.pi / (2 * n_cells)) * np.exp(2j * np.pi * (np.arange(n_cells) + 0.25) / n_cells))
    mx = max(mx, np.max(abs(lam - want)))
check("toolbox_projected_position_dimer", mx)
mx = 0.0
for _ in range(10):  # Pauli exponential and the rotation sense of exp(-i theta d.sigma/2)
    d = rng.normal(size=3)
    d /= np.linalg.norm(d)
    xval = rng.uniform(-3, 3)
    ds = d[0] * sx + d[1] * sy + d[2] * sz2
    mx = max(mx, np.max(abs(expm(1j * xval * ds) - (id2 * np.cos(xval) + 1j * ds * np.sin(xval)))))
theta = 0.7
plus_x = np.array([1, 1]) / np.sqrt(2)
turned = expm(-1j * theta * sz2 / 2) @ plus_x
bloch = [np.vdot(turned, op @ turned).real for op in (sx, sy, sz2)]
mx = max(mx, abs(bloch[0] - np.cos(theta)), abs(bloch[1] - np.sin(theta)), abs(bloch[2]))
mx = max(mx, np.max(abs(expm(1j * np.pi / 2 * sx) - 1j * sx)))
check("toolbox_pauli_exponential", mx)
w, w2, tval = 1.3, 0.4, 0.9  # frame turning about z: K = (w - w2)/2 sigma_z
U = expm(-1j * w2 * tval * sz2 / 2)
dU = -1j * w2 / 2 * sz2 @ U
check("toolbox_frame_change", np.max(abs(U.conj().T @ (w / 2 * sz2) @ U - 1j * U.conj().T @ dU - (w - w2) / 2 * sz2)))
pairs = [frozenset(c) for c in itertools.combinations(range(1, 5), 2)]
ref = frozenset({1, 2})
classes = [len(ref - c) for c in pairs]
assert (classes.count(0), classes.count(1), classes.count(2)) == (1, 4, 1)
results["toolbox_two_fermions_four_orbitals"] = {"reference": 1, "single": 4, "double": 1}
check("toolbox_two_spin_commutator", np.max(abs(comm(np.kron(sx, sx), np.kron(sz2, id2)) + 2j * np.kron(sy, sx))))
theta = 0.83
S = -1j * theta / 2 * sx
check("toolbox_commutator_series", np.max(abs(expm(-S) @ sz2 @ expm(S) - (sz2 * np.cos(theta) + sy * np.sin(theta)))))
mx = 0.0
for theta in np.linspace(0, np.pi / 2, 7):  # trace norm of rho - |0><0| for a pure qubit state
    psi = np.array([np.cos(theta), np.sin(theta)])
    diff = np.outer(psi, psi) - np.diag([1.0, 0.0])
    mx = max(mx, abs(np.sum(abs(np.linalg.eigvalsh(diff))) - 2 * np.sin(theta)),
             abs(np.trace(diff @ sz2).real + 2 * np.sin(theta) ** 2))
mx = max(mx, abs(np.sum(abs(np.linalg.eigvalsh(id2 / 2 - np.diag([1.0, 0.0])))) - 1))
check("toolbox_trace_norm", mx)
bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
prod = np.kron([1, 0], [1, 1]) / np.sqrt(2)
mx = 0.0
for vec, rho1, expect in ((bell, id2 / 2, 0.0), (prod, np.diag([1.0, 0.0]), 1.0)):
    rho = np.outer(vec, vec.conj())
    red = np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)
    mx = max(mx, np.max(abs(red - rho1)), abs(np.trace(rho @ np.kron(sz2, id2)).real - expect))
check("toolbox_partial_trace", mx)
q1, q2 = np.kron(np.diag([0.0, 1.0]), id2), np.kron(id2, np.diag([0.0, 1.0]))
left = np.eye(4) - (np.eye(4) - q1) @ (np.eye(4) - q2)
check("toolbox_commuting_projectors", np.max(abs(np.diag(left) - [0, 1, 1, 1])) + np.max(abs(np.diag(q1 + q2) - [0, 1, 1, 2])))

results["scope"] = ("Single-particle picture data and finite-matrix teaching algebra. "
                    "Not a pump simulation or a physical lifetime.")
(ROOT / "check_answers.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
