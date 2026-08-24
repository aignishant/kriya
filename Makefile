# `make` is not used in this project; ./o is the driver (plan §17.9, Day 0).
# This shim exists only so muscle memory and `make check` still reach the real gate.
check:
	@bash ./o check
