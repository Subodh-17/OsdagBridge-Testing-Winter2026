A related symptom on `dev` @ `d74f56d`: `designer.py:401` sets `n_girders = geom.n_l`. That value is 6 for a 4-girder bridge because it includes the two overhang edge lines, so `BridgeConfig` also reports 6 girders.

Commit `eaba076` (`patches/0003-*` in my submission repository) binds the count to `bridge._girder_count()`. This fixes only the designer's girder count, not the section assignment of the edge lines described in this issue.
