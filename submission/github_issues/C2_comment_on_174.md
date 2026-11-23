Independent confirmation on `dev` @ `d74f56d`. With a line + patch case built using `add_load(..., load_factor=1.35)`, the maximum factored force equals the unfactored one: **26,331.90 N, a ratio of 1.00000** instead of 1.35.

My fix (commit `f555075`, `patches/0006-*`) multiplies point, line, patch and nodal magnitudes by `load_dict["factor"]` inside `_distribute_load_types_to_model`, without mutating the load objects. After the fix:

- the ratio is 1.35000;
- 9 hand-calculated cases pass, including mixed 1.35/1.75 factors, a zero factor, a negative factor, and a case factor combined with a load factor.
