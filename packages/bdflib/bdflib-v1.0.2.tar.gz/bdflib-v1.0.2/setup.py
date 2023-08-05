#!/usr/bin/python
from distutils.core import setup
import subprocess
from os.path import dirname, join

def guess_version():
	git_repo = join(dirname(__file__), ".git")

	try:
		version_number = subprocess.check_output([
				'git', '--git-dir', git_repo,
				'describe',
				# We only want to know about tags
				'--tags',
				# Tags that look like version numbers
				'--match', 'v*',
			]).strip()
	except (OSError, subprocess.CalledProcessError):
		# Git isn't installed, or this is run outside a git repo.
		version_number = "0.0_unknown"

	return version_number

setup(
		name='bdflib',
		version=guess_version(),
		description="Library for working with BDF font files.",
		author="Timothy Allen",
		author_email="screwtape@froup.com",
		url='https://gitlab.com/Screwtapello/bdflib/wikis/home',
		packages=['bdflib', 'bdflib.test'],
		scripts=[
			'bin/bdflib-embolden',
			'bin/bdflib-fill',
			'bin/bdflib-merge',
			'bin/bdflib-passthrough',
		],
	)
