start:
	briefcase dev

test:
	briefcase dev --test

test-r:
	briefcase dev --test -r

ruff:
	ruff check && ruff format --diff
