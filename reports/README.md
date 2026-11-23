# Reports: what to read

The **authoritative summary** is the technical report: `submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`, with its source in `reports/SUBMISSION_TECHNICAL_REPORT.md`.

Everything else in this folder is the dated working record, kept unedited for traceability. Where a later document corrects an earlier one, the later one governs.

| Topic | Current document |
|:--|:--|
| Defect register: all 20 entries, locations, oracles | `phase_3/PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV3.md` |
| Batch 1 closure (DEF-12, DEF-08, DEF-11) | `phase_3/PHASE_3_BATCH_1_CLOSURE_REPORT.md` |
| Batch 2 closure (DEF-18) | `phase_3/PHASE_3_BATCH_2_CLOSURE_RECORD.md` |
| Batch 3 closure (DEF-01) | `phase_3/PHASE_3_BATCH_3_CLOSURE_RECORD.md` |
| Batch status across Phase 3 | `phase_3/PHASE_3_CLOSURE_LEDGER.md` |
| Phase 2 regression suite and evidence controls | `PHASE_2_FINAL_CLOSURE_AUDIT.md`, `PHASE_2_13_TEST_RESULTS.md` |
| Follow-up moving-load fix (`bbfe14c`) | Report §5.1; `testing/evidence/phase_3/full_design_check/` |

## Superseded, historical only

- The Phase 3 planning documents **without** a `_REV3` suffix, and the `_REV2` set, are earlier drafts. The independent audits in `phase_3/CLAUDE_INDEPENDENT_*` reject them for errors.
- The independent audit files (`CLAUDE_*`, `*_INDEPENDENT_AUDIT*`) are reviews written during the work by an AI reviewer used as an independent checker. Their verdicts refer to the documents as they stood at the time.
- `PHASE_3_CLOSURE_LEDGER.md` predates the follow-up commit `bbfe14c`. The current lineage is: Batches 1–3 (`418fd75` … `f555075`), then `bbfe14c` (report §5.1).
