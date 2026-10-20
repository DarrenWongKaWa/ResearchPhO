"""Recompute every derivable answer of the exam; writes check_answers.json.

Run beside the TeX files:  python3 check_answers.py
Needs numpy and scipy.
"""
from __future__ import annotations
import json
import numpy as np
from scipy import integrate, special, stats

rng = np.random.default_rng(7)
out: dict = {}

def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))

# ---------------- Problem 1 ----------------
p1 = {}
# A.1 Gaussian orbitals, delta impurity: ratios
a, b = 4.0, 1.0
phi = lambda x, j: (np.pi * b**2) ** -0.25 * np.exp(-(x - j * a) ** 2 / (2 * b**2))
X = 0.0
p1["A1_site_bond_over_onsite"] = phi(X, 0) * phi(X, 1) / phi(X, 0) ** 2
assert close(p1["A1_site_bond_over_onsite"], np.exp(-a**2 / (2 * b**2)))
p1["A1_site_neighbour_onsite_over_onsite"] = phi(X, 1) ** 2 / phi(X, 0) ** 2
assert close(p1["A1_site_neighbour_onsite_over_onsite"], np.exp(-a**2 / b**2))
X = a / 2
p1["A1_mid_bond_over_onsite"] = phi(X, 0) * phi(X, 1) / phi(X, 0) ** 2
assert close(p1["A1_mid_bond_over_onsite"], 1.0)
assert close(phi(X, 0) ** 2, np.exp(-a**2 / (4 * b**2)) / (np.sqrt(np.pi) * b))
# A.2 binary alloy cumulants and matching variance
c, W = 0.1, 1.0
Delta = W / np.sqrt(12 * c * (1 - c))
k2 = c * (1 - c) * Delta**2
k3 = c * (1 - c) * (1 - 2 * c) * Delta**3
samples = np.where(rng.random(4_000_000) < c, Delta, 0.0)
assert abs(samples.var() - k2) < 3e-3 and abs(stats.moment(samples, 3) - k3) < 3e-3
assert close(k2, W**2 / 12)
p1["A2_Delta_over_W_c0.1"] = Delta
p1["A2_kappa3_over_W3_c0.1"] = k3
# B.1 position disorder -> bond covariances
s, M = 0.1, 200000
u = rng.normal(0, s, M + 1)
dJ = u[1:] - u[:-1]  # J'=1
p1["B1_var"] = dJ.var()
p1["B1_cov1"] = np.mean(dJ[:-1] * dJ[1:])
p1["B1_cov2"] = np.mean(dJ[:-2] * dJ[2:])
assert abs(p1["B1_var"] - 2 * s**2) < 1e-3 and abs(p1["B1_cov1"] + s**2) < 1e-3 and abs(p1["B1_cov2"]) < 1e-3
# B.2 mean shifts for r^-3 and r^-6 at s=0.03a (second order) + exact check
s = 0.03
dd = rng.normal(0, s, 2_000_000) - rng.normal(0, s, 2_000_000)
p1["B2_meanshift_J_2nd"] = 12 * s**2
p1["B2_meanshift_V_2nd"] = 42 * s**2
p1["B2_meanshift_J_mc"] = float(np.mean((1 + dd) ** -3) - 1)
p1["B2_meanshift_V_mc"] = float(np.mean((1 + dd) ** -6) - 1)
p1["B2_rms_dJ_over_J"] = 3 * np.sqrt(2) * s
p1["B2_rms_dV_over_V"] = 6 * np.sqrt(2) * s
assert abs(p1["B2_meanshift_J_mc"] - 12 * s**2) < 1.5e-3
# C.1 Born rate at E=J, mean free path, localization length
J, Wd = 1.0, 1.0
E = J
nu = 1 / (np.pi * np.sqrt(4 * J**2 - E**2))
rate = 2 * np.pi * (Wd**2 / 12) * nu          # hbar = 1
tau = 1 / rate
p1["C1_tau"] = tau
p1["C1_Gamma_over_J"] = 1 / (2 * tau)
assert close(p1["C1_Gamma_over_J"], 1 / (12 * np.sqrt(3)))
v = np.sqrt(4 * J**2 - E**2)
p1["C1_ell_over_a"] = v * tau
p1["C1_xi_over_a"] = 24 * (4 * J**2 - E**2) / Wd**2
p1["C1_xi_over_ell"] = p1["C1_xi_over_a"] / p1["C1_ell_over_a"]
p1["C1_exp_minus_2L_over_xi_L1000"] = float(np.exp(-2 * 1000 / p1["C1_xi_over_a"]))
# numerical check of the Born rate: survival probability of a plane wave, L=3000, W=0.5
def survival_rate(L=3000, W=0.5, nsamp=6, tmax=60.0):
    kk = 2 * np.pi * round(L / 3) / L     # E = -2 cos k ~ J
    ts = np.linspace(0, tmax, 31)
    ps = np.zeros_like(ts)
    for _ in range(nsamp):
        eps = rng.uniform(-W / 2, W / 2, L)
        H = np.diag(eps) - np.eye(L, k=1) - np.eye(L, k=-1)
        H[0, -1] = H[-1, 0] = -1
        e, V = np.linalg.eigh(H)
        psi0 = np.exp(1j * kk * np.arange(L)) / np.sqrt(L)
        c0 = V.T @ psi0
        amp = np.array([np.sum(np.abs(c0) ** 2 * np.exp(-1j * e * t)) for t in ts])
        ps += np.abs(amp) ** 2 / nsamp
    sel = (ts > 5) & (ps > 0.05)
    slope = np.polyfit(ts[sel], np.log(ps[sel]), 1)[0]
    return -slope
born_W05 = 2 * np.pi * (0.25 / 12) * nu
p1["C1_check_rate_numeric_W0.5"] = survival_rate()
p1["C1_check_rate_born_W0.5"] = born_W05
assert abs(p1["C1_check_rate_numeric_W0.5"] / born_W05 - 1) < 0.12
# numerical check of the localization length at E=J, W=0.5 (transfer matrix)
def lyapunov(E=1.0, W=0.5, n=2_000_000):
    psi0, psi1, acc = 0.0, 1.0, 0.0
    eps = rng.uniform(-W / 2, W / 2, n)
    for i in range(n):
        psi2 = (eps[i] - E) * psi1 - psi0
        psi0, psi1 = psi1, psi2
        if abs(psi1) > 1e10:
            acc += np.log(abs(psi1)); psi0 /= abs(psi1); psi1 /= abs(psi1)
    return (acc + np.log(abs(psi1))) / n
xi_num = 1 / lyapunov(n=400_000)
p1["C1_check_xi_numeric_W0.5"] = xi_num
p1["C1_check_xi_formula_W0.5"] = 24 * 3 / 0.25
assert abs(xi_num / (72 / 0.25) - 1) < 0.1
# C.2 tau_tr/tau_q for Gaussian correlated disorder
for kl in (3.0,):
    al = kl**2
    num = integrate.quad(lambda th: np.exp(-al * (1 - np.cos(th))), 0, 2 * np.pi)[0]
    den = integrate.quad(lambda th: np.exp(-al * (1 - np.cos(th))) * (1 - np.cos(th)), 0, 2 * np.pi)[0]
    p1["C2_ratio_exact_kFlambda3"] = num / den
    p1["C2_ratio_smallangle_kFlambda3"] = 2 * al
    bessel = special.i0e(al) / (special.i0e(al) - special.i1e(al))
    assert close(num / den, bessel, 1e-6)
# C.3 Heisenberg time at E=J, L=1000 (hbar=J=1)
p1["C3_tH_L1000"] = 2 * np.pi * 1000 * nu
p1["C3_tau_W1"] = tau
p1["C3_level_spacing"] = 1 / (1000 * nu)
# two-site formula check
e1, e2, Jh = 0.3, -0.2, 0.7
h = np.array([[e1, -Jh], [-Jh, e2]])
t = 2.3
ev, V = np.linalg.eigh(h)
U = V @ np.diag(np.exp(-1j * ev * t)) @ V.T
D = e1 - e2
P2 = 4 * Jh**2 / (D**2 + 4 * Jh**2) * np.sin(np.sqrt(D**2 + 4 * Jh**2) * t / 2) ** 2
assert close(abs(U[1, 0]) ** 2, P2, 1e-10)
# D.1 noise rates
hbar = 6.582119569e-13  # meV s
w0 = 10 / hbar
Xs = 0.1  # meV
def wrate(tc):
    S = 2 * tc / (1 + (w0 * tc) ** 2)   # times sigma^2
    return Xs**2 * S / hbar**2
p1["D1_omega0"] = w0
p1["D1_wmax"] = Xs**2 / (hbar**2 * w0)
p1["D1_w_tc_1ns"] = wrate(1e-9)
p1["D1_w_tc_1fs"] = wrate(1e-15)
p1["D1_wt_1ps"] = {k: p1[k] * 1e-12 for k in ("D1_wmax", "D1_w_tc_1ns", "D1_w_tc_1fs")}
p1["D1_wt_10us"] = {k: p1[k] * 1e-5 for k in ("D1_wmax", "D1_w_tc_1ns", "D1_w_tc_1fs")}
assert close(wrate(1 / w0), p1["D1_wmax"])
# D.2 Lorentzian with puddles
chi0, wl, sm = 1.0, 10.0, 3.0
chi = lambda x: chi0 * wl**2 / (x**2 + wl**2)
p1["D2_meanshift_taylor"] = -sm**2 / wl**2
xs = rng.normal(0, sm, 2_000_000)
p1["D2_meanshift_mc"] = float(np.mean(chi(xs)) - 1)
p1["D2_flank_rel_rms_taylor"] = sm / wl
p1["D2_flank_rel_rms_mc"] = float(np.std(chi(wl + xs)) / chi(wl))
out["problem1"] = p1

# ---------------- Problem 2 ----------------
p2 = {}
# A.1 Berry curvature of massive Dirac from the d-vector formula vs numeric
vD, m = 1.0, 0.4
def omega_upper_numeric(kx, ky, dk=1e-5):
    def u(kx, ky):
        h = np.array([[m, vD * (kx - 1j * ky)], [vD * (kx + 1j * ky), -m]])
        e, V = np.linalg.eigh(h)
        return V[:, 1]
    # Fukui-type plaquette
    u1, u2, u3, u4 = u(kx, ky), u(kx + dk, ky), u(kx + dk, ky + dk), u(kx, ky + dk)
    prod = np.vdot(u1, u2) * np.vdot(u2, u3) * np.vdot(u3, u4) * np.vdot(u4, u1)
    return -np.angle(prod) / dk**2
kx0, ky0 = 0.3, -0.2
E0 = np.sqrt(vD**2 * (kx0**2 + ky0**2) + m**2)
p2["A1_Omega_numeric"] = omega_upper_numeric(kx0, ky0)
p2["A1_Omega_formula"] = -m * vD**2 / (2 * E0**3)
assert abs(p2["A1_Omega_numeric"] - p2["A1_Omega_formula"]) < 1e-4
# intrinsic integral: lower band all k + upper band k<kF
eF = 1.0
kF = np.sqrt(eF**2 - m**2) / vD
low = integrate.quad(lambda k: k * m * vD**2 / (2 * (vD**2 * k**2 + m**2) ** 1.5), 0, np.inf)[0] / (2 * np.pi)
up = integrate.quad(lambda k: -k * m * vD**2 / (2 * (vD**2 * k**2 + m**2) ** 1.5), 0, kF)[0] / (2 * np.pi)
p2["A1_int_f0_Omega"] = low + up
p2["A1_formula_m_over_4pi_eF"] = m / (4 * np.pi * eF)
assert close(low + up, m / (4 * np.pi * eF), 1e-8)
# B.2 Berry curvature dipole of tilted cone, first order in t
def Dx_numeric(t, n=1400):
    L = 2.2 * kF
    ks = np.linspace(-L, L, n)
    KX, KY = np.meshgrid(ks, ks, indexing="ij")
    Ek = np.sqrt(vD**2 * (KX**2 + KY**2) + m**2)
    eps = t * KX + Ek
    Om = -m * vD**2 / (2 * Ek**3)
    dOm = 3 * m * vD**4 * KX / (2 * Ek**5)       # d Omega / d kx
    f0 = (eps < eF).astype(float)
    dk = ks[1] - ks[0]
    return np.sum(f0 * dOm) * dk * dk / (2 * np.pi) ** 2
tt = 0.02
Dx_formula = -3 * tt * m * (eF**2 - m**2) / (8 * np.pi * eF**4)
p2["B2_Dx_numeric_t0.02"] = Dx_numeric(tt)
p2["B2_Dx_formula_t0.02"] = Dx_formula
assert abs(p2["B2_Dx_numeric_t0.02"] / Dx_formula - 1) < 0.03
# check chi^in of the source paper equals -(e^3 tau/2hbar^2) Dx with the given tau (units e=hbar=1, h=2pi)
n_iV0sq = 0.37
tau_s = 4 * vD**2 * eF / (n_iV0sq * (eF**2 + 3 * m**2))
chi_in_paper = (1 / (2 * np.pi)) * tt * m / n_iV0sq * 3 * vD**2 * (eF**2 - m**2) / (2 * eF**3 * (eF**2 + 3 * m**2))
chi_ours = -(tau_s / 2) * Dx_formula
p2["B_check_chi_in_paper_vs_ours"] = [chi_in_paper, chi_ours]
assert close(chi_in_paper, chi_ours, 1e-10)
# C.2 ratios at eF = 2m
r = 2.0
p2["C2_sj_over_cd_eF2m"] = (r**2 - 25) / (3 * (r**2 + 3))
p2["C2_isk_over_cd_eF2m"] = -(r**2 - 1) * (13 * r**2 + 77) / (6 * (r**2 + 3) ** 2)
p2["C2_sj_zero_at_eF_over_m"] = 5.0
rr = np.linspace(1.0001, 200, 200000)
sj = (rr**2 - 25) / (3 * (rr**2 + 3)); isk = -(rr**2 - 1) * (13 * rr**2 + 77) / (6 * (rr**2 + 3) ** 2)
tot1, tot2 = 1 + sj + isk, 1 - sj - isk
p2["C2_total_theoryI_range"] = [float(tot1.min()), float(tot1.max())]
p2["C2_total_theoryII_range"] = [float(tot2.min()), float(tot2.max())]
p2["C2_totals_at_eF2m"] = [float(1 + p2["C2_sj_over_cd_eF2m"] + p2["C2_isk_over_cd_eF2m"]), float(1 - p2["C2_sj_over_cd_eF2m"] - p2["C2_isk_over_cd_eF2m"])]
assert tot1.max() < 0 and tot2.min() > 0
# C.3 illustrative data fit
sig = np.array([1.0, 2.0, 4.0]); y = np.array([0.9, 1.3, 2.1])
C1, C2 = np.polyfit(sig, y, 1)
p2["C3_C1"], p2["C3_C2"] = C1, C2
assert close(C1, 0.4) and close(C2, 0.5)
# D.1 moments
p2["D1_V1cubed"] = {"repulsive": 1.0, "attractive": -1.0, "mixed": 0.0}
out["problem2"] = p2

# ---------------- Problem 3 ----------------
p3 = {}
# A.2 log-average of uniform s in [1-W/2, 1+W/2]
def logavg(W):
    lo, hi = 1 - W / 2, 1 + W / 2
    F = lambda x: x * np.log(x) - x if x > 0 else 0.0
    return (F(hi) - F(lo)) / W
p3["A2_logavg_W1"] = logavg(1.0)
p3["A2_logavg_W2"] = logavg(2.0)
p3["A2_ln0.8"] = np.log(0.8)
p3["A2_edge_loc_length_W2"] = 1 / (np.log(0.8) - logavg(2.0))
from scipy.optimize import brentq
p3["A2_Wc"] = brentq(lambda W: logavg(W) - np.log(0.8), 1.0, 2.0)
# numerical check: zero mode recursion on a long chain
for W in (1.0, 2.0):
    sv = rng.uniform(1 - W / 2, 1 + W / 2, 200000)
    p3[f"A2_mc_logavg_W{W:g}"] = float(np.mean(np.log(sv)))
# B.1 bookkeeping
Q = {10: -1.00, 30: -0.99, 50: -0.62, 70: -1.01}
p3["B1_dN_11_30"] = Q[10] - Q[30]
p3["B1_dN_31_50"] = Q[30] - Q[50]
p3["B1_dN_51_70"] = Q[50] - Q[70]
# C.1 two-site toy: |h| independent of theta
for th in (0.1, 0.7, 1.3):
    e1, e2 = rng.normal(size=2)
    wA = np.array([np.cos(th), np.sin(th)]); wB = np.array([-np.sin(th), np.cos(th)])
    Mm = np.array([[np.sum(np.array([e1, e2]) * wA * wA), np.sum(np.array([e1, e2]) * wA * wB)],
                   [np.sum(np.array([e1, e2]) * wB * wA), np.sum(np.array([e1, e2]) * wB * wB)]])
    hz = (Mm[0, 0] - Mm[1, 1]) / 2; hx = Mm[0, 1]
    assert close(hz, (e1 - e2) * np.cos(2 * th) / 2) and close(hx, -(e1 - e2) * np.sin(2 * th) / 2)
    assert close(hz**2 + hx**2, (e1 - e2) ** 2 / 4)
# C.2 rounded table values
dA = np.array([0.0, 0.0, 0.03, 0.50, 0.47]); dB = np.array([0.47, 0.50, 0.03, 0.0, 0.0])
p3["C2_sum_d2_table"] = float(np.sum((dA - dB) ** 2))
p3["C2_rms_hz_over_W_table"] = float(np.sqrt(np.sum((dA - dB) ** 2) / 48))
prods = np.array([-0.013, 0.027, -0.013])
p3["C2_rms_hx_over_W_table"] = float(np.sqrt(np.sum(prods**2) / 12))
p3["C2_bias_to_mixing_ratio"] = p3["C2_rms_hz_over_W_table"] / p3["C2_rms_hx_over_W_table"]

# full model: flavor orbitals at several phases (clean chain K/J=-3/2, 24-cell ring)
K, N = -1.5, 24
L = 5 * N
def ring(phi_):
    tt_ = 1 + K * np.cos(phi_ + 4 * np.pi * np.arange(5) / 5)
    H = np.zeros((L, L))
    for j in range(L):
        H[(j + 1) % L, j] -= tt_[j % 5]; H[j, (j + 1) % L] -= tt_[j % 5]
    return H
def orbitals(phi_):
    _, vecs = np.linalg.eigh(ring(phi_)); occ = vecs[:, : 2 * N]
    ph = np.exp(2j * np.pi * np.arange(L) / L)
    Mx = occ.conj().T @ (ph[:, None] * occ)
    _, uu = np.linalg.eig(Mx)
    Uu, _, Vh = np.linalg.svd(uu); uu = Uu @ Vh
    w = occ @ uu
    x = np.angle(np.diag(uu.conj().T @ Mx @ uu)) * L / (2 * np.pi) / 5
    idx = np.argsort(x); return x[idx], w[:, idx]
model = []
for phi_ in np.linspace(0, 2 * np.pi, 9)[:-1]:
    x, w = orbitals(phi_)
    sel = [i for i in range(len(x)) if 0 <= x[i] < 1]
    i1, i2 = sel[0], sel[1]
    d = np.abs(w[:, i2]) ** 2 - np.abs(w[:, i1]) ** 2
    mix = np.conj(w[:, i2]) * w[:, i1]
    model.append({"phi_over_pi": phi_ / np.pi, "centres": [float(x[i1]), float(x[i2])],
                  "rms_hz_over_W": float(np.sqrt(np.sum(d**2) / 48)),
                  "rms_mix_over_W": float(np.sqrt(np.sum(np.abs(mix) ** 2) / 12))})
p3["C2_model_scan"] = model
assert all(0.13 < r_["rms_hz_over_W"] < 0.145 for r_ in model)
assert all(r_["rms_mix_over_W"] < 0.02 for r_ in model)
# followed orbital: start at centre near -0.109 cells, track one period
def track(start, steps=400):
    xcur = start
    for phi_ in np.linspace(0, 2 * np.pi, steps + 1)[1:]:
        c, _ = orbitals(phi_)
        cand = np.concatenate([c - N, c, c + N]); xcur = cand[np.argmin(abs(cand - xcur))]
    return xcur
c0, _ = orbitals(0.0)
start = c0[np.argmin(abs(c0 + 0.109))]
end1 = track(start, 200)
p3["B2_single_period_displacements"] = [float(end1 - start)]
end2 = track(end1, 200)
p3["B2_single_period_displacements"].append(float(end2 - end1))
assert abs(sum(p3["B2_single_period_displacements"]) + 1) < 1e-2
# D.1 clean domain threshold
Ew, Vmax = 0.4, 0.01
p3["D1_ell_threshold"] = Ew / (2 * Vmax)
# D.2 random-field probabilities
sh = 0.05
p3["D2_ell_for_p_Phi(-1)"] = Ew**2 / (4 * sh**2)
p3["D2_p_ell4"] = float(stats.norm.cdf(-Ew / (2 * sh * 2)))
p3["D2_count_disjoint_4cell_segments_N1e4"] = 2500 * p3["D2_p_ell4"]
p3["D2_W_for_sigma_h_0.05"] = sh / 0.1401
# Monte Carlo check of p(4)
hs = rng.normal(0, sh, (400000, 4)).sum(axis=1)
p3["D2_p_ell4_mc"] = float(np.mean(Ew - 2 * hs < 0))
# D.3 first event vs macroscopic failure
Nc, r_, xi_, eps_ = 1e4, 1e-6, 10, 0.01
p3["D3_t1"] = 1 / (Nc * r_)
p3["D3_teps"] = eps_ / (r_ * xi_)
p3["D2_note"] = "W = sigma_h / 0.140"
out["problem3"] = p3

# ---------------- Toolbox (Appendix E) ----------------
tb = {}
xs_, ps_ = np.array([0.0, 1.0, 3.0]), np.array([0.5, 0.25, 0.25])
m1 = np.sum(ps_ * xs_); var_ = np.sum(ps_ * (xs_ - m1) ** 2); k3_ = np.sum(ps_ * (xs_ - m1) ** 3)
assert close(var_, 1.5) and close(k3_, 1.5) and close(np.sum(ps_ * xs_**3) - 3 * m1 * np.sum(ps_ * xs_**2) + 2 * m1**3, 1.5)
assert close(integrate.quad(lambda x: x**2, -0.5, 0.5)[0], 1 / 12)
assert abs(sum(np.exp(2j * np.pi * j / 3) for j in range(1, 4))) < 1e-12
assert close(integrate.quad(lambda x: x**2 * np.exp(-x**2 / 2), -np.inf, np.inf)[0] / integrate.quad(lambda x: np.exp(-x**2 / 2), -np.inf, np.inf)[0], 1.0)
sig2, tc = 1.3, 0.7
Sw = lambda w: 2 * sig2 * tc / (1 + (w * tc) ** 2)
assert close(integrate.quad(Sw, -np.inf, np.inf)[0] / (2 * np.pi), sig2, 1e-6)
xg = rng.normal(0, 0.3, 2_000_000); Fv = xg + xg**2
assert abs(Fv.mean() - 0.09) < 2e-3 and abs(Fv.var() - (0.09 + 2 * 0.09**2)) < 3e-3
assert close(integrate.quad(lambda k: k**3 * np.exp(-k**2), 0, np.inf)[0] * np.pi, np.pi / 2)
assert close(integrate.quad(lambda k: 2 * k**2 * np.exp(-k**2), -np.inf, np.inf)[0], np.sqrt(np.pi))
Mm2 = np.array([[3, 1 - 1j], [1 + 1j, 1]])
assert np.allclose(np.sort(np.linalg.eigvalsh(Mm2)), [2 - np.sqrt(3), 2 + np.sqrt(3)])
assert close(integrate.quad(np.log, 0, 1)[0], -1.0)
assert close(stats.norm.sf(2 / 2), 0.158655, 1e-4)
# Berry curvature of d=(kx,ky,1): integral of Omega_- over the plane / 2pi = 1/2
assert close(integrate.quad(lambda k: k / (2 * (k**2 + 1) ** 1.5), 0, np.inf)[0], 0.5)
tb["all_toolbox_checks"] = "passed"
out["toolbox"] = tb

def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(f"{float(o):.6g}")
    return o
with open("check_answers.json", "w") as fh:
    json.dump(clean(out), fh, indent=1)
print(json.dumps(clean(out), indent=1))
