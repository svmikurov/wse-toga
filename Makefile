start:
	briefcase dev

test:
	briefcase dev --test

test-r:
	briefcase dev --test -r

ruff:
	ruff check && ruff format --diff

# Android
android-create:
	briefcase create android

android-build:
	briefcase build android

android-update:
	briefcase build android

update: android-update android-build
