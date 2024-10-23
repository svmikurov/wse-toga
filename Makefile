start:
	briefcase dev

test:
	briefcase dev --test

test-r:
	briefcase dev --test -r

ruff:
	ruff check && ruff format --diff

# Briefcase
android-create:
	briefcase create android

android-build:
	briefcase build android

android: android-create android-build
