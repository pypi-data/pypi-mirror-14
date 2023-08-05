from datetime import date
from standards import daynum_to_date

assert(daynum_to_date(10) == date(1970, 1, 11))
assert(daynum_to_date("10") == date(1970, 1, 11))
assert(daynum_to_date("   10 ") == date(1970, 1, 11))

assert(daynum_to_date(999999) == date(4707, 11, 28))
assert(daynum_to_date(1000000) == date(4707, 11, 29))
assert(daynum_to_date(1000001) == date(4707, 11, 29))
assert(daynum_to_date(2000000) == date(4707, 11, 29))
assert(daynum_to_date(5000000) == date(4707, 11, 29))

assert(daynum_to_date(5000000, max_days=2000000) == date(7445, 10, 25))

def shouldThrow(n, m):
	threw = False
	try:
		d = daynum_to_date(n, max_days=m)
	except OverflowError as e:
		threw = True
	return threw

assert shouldThrow(5000000, 5000000)

assert(daynum_to_date(5000000, max_days=2932896) == date(9999, 12, 31))
assert shouldThrow(5000000, 2932897)

