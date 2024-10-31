start:
	briefcase dev

# Test
test:
	export TOGA_BACKEND=toga_dummy && \
	briefcase dev --test

test-r:
	briefcase dev --test -r

ruff:
	ruff check && ruff format --diff

format:
	ruff check --fix && ruff format

check: ruff test

# Briefcase for android
android-create:
	briefcase create android

android-build:
	briefcase build android

update: android-create android-build
