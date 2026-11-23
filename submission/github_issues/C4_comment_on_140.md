Root cause, for reference (`dev` @ `d74f56d`): `IRC6_2017.cl_208_3_impact_factor` (`utils/codes/irc6_2017.py`, about line 523) tests `if KEY_VEHICLE[1]:`. `KEY_VEHICLE[1]` is the constant string `'Class70R(T)'`, which is always true. So for spans of 9–45 m it returns 0.10 for every vehicle, including Class A.

The report shows a different value. `reports/chap3.py` (about lines 88–116) prints the Class A impact as 9/(13.5+L), which is 0.24 for L = 24 m. Analysis therefore uses 1.10 while the report states 1.24.
