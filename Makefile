start:
	briefcase dev

test:
	briefcase dev --test

test-r:
	briefcase dev --test -r

ruff:
	ruff check && ruff format --diff

format:
	ruff check --fix && ruff format

# Briefcase for android
android-create:
	briefcase create android

android-build:
	briefcase build android

update: android-create android-build
