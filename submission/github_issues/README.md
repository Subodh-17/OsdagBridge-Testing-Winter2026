# Issues to publish on Nidhikhare12/OsdagBridge (awaiting approval)

Duplicates were checked against the upstream tracker on 23 Nov 2026.

## New issues (3)

| # | Title | Body file |
|:-:|:--|:--|
| 1 | [Bug/Design] Bearing-stiffener web buckling capacity overstated ~3,400× (stiffener inertia used for r, no IS 800 buckling curve): 214,533 kN vs 63.4 kN | `01_bearing_stiffener_web_buckling.md` |
| 2 | [Bug/Analysis] ospgrillage line/patch loads not conserved: first-bay load point placed outside the mesh and silently dropped, segment length missing, patch corner cells counted twice (barrier load 37.5 % short) | `02_grillage_load_conservation.md` |
| 3 | [Bug/Analysis] Crash-barrier SIDL load case never enters the dead-load / ULS combinations (create_sidl_combination not called) | `03_barrier_sidl_not_in_uls.md` |

## Comments on existing issues (4), instead of duplicates

| Issue | Body file |
|:-:|:--|
| #65 | `C1_comment_on_65.md` |
| #174 | `C2_comment_on_174.md` |
| #113 | `C3_comment_on_113.md` |
| #140 | `C4_comment_on_140.md` |

## Deliberately not filed

| Defect | Reason |
|:--|:--|
| DEF-01 load factors | Already reported as #174 |
| DEF-08 executive summary | Already reported as #65 |
| DEF-11 girder count | Covered by #113 |
| DEF-19a impact factor | Already reported as #140 |
| DEF-05 wind | Already reported as #86 |
| DEF-06 temperature | Already reported as #92 |
| DEF-13 densities | Already reported as #41 / #20 |
| DEF-20 wearing-course width | Whether the full deck or only the carriageway should carry the wearing course is a design-intent question, not a proven bug |

## Commands (Windows, GitHub CLI `gh` logged in as Subodh-17)

Run these from `F:\FOSSEE internship\submission\github_issues`.

**Before running anything:** open each referenced issue (#65, #113, #140, #174) in the browser and run a last search for "stiffener", "line load", "SIDL", so that nothing filed in the last few hours is duplicated.

```bat
gh issue create -R Nidhikhare12/OsdagBridge --title "[Bug/Design] Bearing-stiffener web buckling capacity overstated ~3,400x (stiffener inertia used for r, no IS 800 buckling curve): 214,533 kN vs 63.4 kN" --body-file 01_bearing_stiffener_web_buckling.md
gh issue create -R Nidhikhare12/OsdagBridge --title "[Bug/Analysis] ospgrillage line/patch loads not conserved: first-bay point placed outside mesh and silently dropped, segment length missing, patch corners counted twice (barrier load 37.5% short)" --body-file 02_grillage_load_conservation.md
gh issue create -R Nidhikhare12/OsdagBridge --title "[Bug/Analysis] Crash-barrier SIDL load case never enters dead-load / ULS combinations (create_sidl_combination not called)" --body-file 03_barrier_sidl_not_in_uls.md
gh issue comment 65  -R Nidhikhare12/OsdagBridge --body-file C1_comment_on_65.md
gh issue comment 174 -R Nidhikhare12/OsdagBridge --body-file C2_comment_on_174.md
gh issue comment 113 -R Nidhikhare12/OsdagBridge --body-file C3_comment_on_113.md
gh issue comment 140 -R Nidhikhare12/OsdagBridge --body-file C4_comment_on_140.md
```

**Without `gh`:** open https://github.com/Nidhikhare12/OsdagBridge/issues/new, paste the title, then paste the body file's contents.
