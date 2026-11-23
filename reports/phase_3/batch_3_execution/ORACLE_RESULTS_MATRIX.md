# PHASE 3 BATCH 3 — ORACLE RESULTS MATRIX

**Document ID:** P3-B3-MAT-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Batch:** Phase 3 Batch 3 — DEF-01 (Component Load-Factor Scaling)  
**Directive Reference:** P3-B3-AUTH-003  
**Date:** 19 November 2026  
**Status:** 9/9 ORACLES PASSED  

---

## 1. Executive Summary

This matrix documents the verification results for the nine acceptance oracles (**OR-B3-01 through OR-B3-09**) frozen in `BATCH_3_DEF_01_IMPLEMENTATION_READINESS.md` and mandated by Directive `P3-B3-AUTH-003`.

All nine oracles passed on their first formal execution with zero tolerance violations and zero oracle modifications.

---

## 2. Oracle Results Matrix

| Oracle ID | Load Type & Fixture | Nominal Force ($F_{\text{nom}}$) | Load Factor ($\gamma$) | Case Factor ($\gamma_{\text{case}}$) | Target Vertical Reaction ($\sum R_{y,\text{exp}}$) | Observed Vertical Reaction ($\sum R_{y,\text{obs}}$) | Expected Centroid ($\bar{x}_{\text{exp}}$) | Observed Centroid ($\bar{x}_{\text{obs}}$) | Tolerance Limit | Observed Delta ($|\Delta R_y|$) | Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **OR-B3-01** | Point Load on 4-Node Mesh | $100.000\text{ kN}$ | $1.35$ | $1.00$ | $135.000000\text{ kN}$ | $135.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $1.35 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-02** | Uniform Line Load (4-Node) | $200.000\text{ kN}$ | $1.35$ | $1.00$ | $270.000000\text{ kN}$ | $270.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $2.70 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-03** | Uniform Patch Load (4-Node) | $400.000\text{ kN}$ | $1.35$ | $1.00$ | $540.000000\text{ kN}$ | $540.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $5.40 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-04** | Multi-Load Superposition ($P_1 + P_2$) | $60.0 + 100.0\text{ kN}$ | $\begin{aligned}\gamma_1 &= 1.35\\\gamma_2 &= 1.75\end{aligned}$ | $1.00$ | $256.000000\text{ kN}$ | $256.000000\text{ kN}$ | $11.8359\text{ m}$ | $11.8359\text{ m}$ | $2.56 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-05** | Multi-Axle Vehicle (CompoundLoad) | $40.0 + 60.0\text{ kN}$ | $0.80$ | $1.00$ | $80.000000\text{ kN}$ | $80.000000\text{ kN}$ | $10.4000\text{ m}$ | $10.4000\text{ m}$ | $8.00 \times 10^{-5}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-06** | Direct Beam-Element Line Load | $160.000\text{ kN}$ | $1.35$ | $1.00$ | $216.000000\text{ kN}$ | $216.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $2.16 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-07** | Zero-Factor Relief Load ($P_1 + P_2$) | $150.0 + 80.0\text{ kN}$ | $\begin{aligned}\gamma_1 &= 1.35\\\gamma_2 &= 0.00\end{aligned}$ | $1.00$ | $202.500000\text{ kN}$ | $202.500000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $2.02 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-08** | Negative / Reversible Load ($P$) | $120.000\text{ kN}$ | $-1.20$ | $1.00$ | $-144.000000\text{ kN}$ | $-144.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $1.44 \times 10^{-4}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |
| **OR-B3-09** | Dual Compounded Scaling | $50.000\text{ kN}$ | $0.80$ | $1.10$ | $44.000000\text{ kN}$ | $44.000000\text{ kN}$ | $10.0000\text{ m}$ | $10.0000\text{ m}$ | $4.40 \times 10^{-5}\text{ kN}$ | $0.000000\text{ kN}$ | **PASS** |

---

## 3. Mathematical Verification Notes

1. **Newtonian Statics Residuals:**
   Across all nine oracles, the reaction sum $\sum R_y$ matched analytical predictions with absolute numerical error $|\Delta R_y| < 10^{-12}\text{ kN}$, outperforming the allowable tolerance limit by more than six orders of magnitude.
2. **Centroid Invariance:**
   For all symmetric loads (OR-B3-01, OR-B3-02, OR-B3-03, OR-B3-06, OR-B3-08, OR-B3-09), $\bar{x} \equiv 10.0000\text{ m}$. For asymmetric compound loads (OR-B3-04 with distinct factors $1.35$ and $1.75$), the observed centroid $\bar{x}_{\text{obs}} = 11.835938\text{ m}$ matched the exact theoretical center of gravity $\frac{60(1.35)(5) + 100(1.75)(15)}{256} = 11.8359375\text{ m}$.
3. **Zero-Factor Relief (OR-B3-07):**
   When $P_2 = 80\text{ kN}$ was assigned $\gamma_2 = 0.00$, the grillage engine completely relieved $P_2$ without floating-point division by zero, yielding $\sum R_y = 202.500000\text{ kN}$ centered exactly at $x = 10.0000\text{ m}$ ($P_1$'s position).
4. **Negative Factor Uplift (OR-B3-08):**
   Reversing the load direction via $\gamma = -1.20$ produced net negative support reactions (uplift) $\sum R_y = -144.000000\text{ kN}$ with correct directional sign preservation.
5. **Dual Compounding (OR-B3-09):**
   Combining component factor $\gamma_{\text{load}} = 0.80$ with case factor $\gamma_{\text{case}} = 1.10$ produced exactly $\sum R_y = 50.0 \times (0.80 \times 1.10) = 44.000000\text{ kN}$, verifying multiplicative scaling.
