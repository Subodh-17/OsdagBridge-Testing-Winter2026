I reproduced this on `dev` @ `d74f56d`. A regression test covering 74 pass/fail combinations (per component, single-girder failures, mixed DCRs) shows the narrative disagreeing with the real status in **64 of the 74** cases.

A fix that derives the narrative and the "Overall Design Status" row from the component DCRs is in commit `12493c9`, file `patches/0002-*` in my submission repository. With it, all 74 cases agree.
