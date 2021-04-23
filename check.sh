#!/bin/bash

main() {
	if [[ $# -gt 0 ]] ; then
		if [[ $# -eq 1 && "$1" == "--docker" ]] ; then
			run_in_docker
		else
			echo "Usage: $0 [--docker]" >&2
			exit 1
		fi
	else
		commands=("isort" "pflake8" "pytest")
		for x in "${commands[@]}" ; do
			if ! command -V "$x" &>/dev/null ; then
				(
					echo "Could not find '$x' command. Did you mean to run this in the docker container?"
					echo ""
					echo "Usage: $0 [--docker]"
				) >&2
				exit 1
			fi
		done

		run
	fi
}

run_in_docker() {
	echo running in docker
	docker-compose run --rm test
}

run() {
	try ./src/manage.py makemigrations --check --dry-run
	try isort src --check --diff
	try pflake8 src
	try pytest

	if [[ "${#failures}" -ne 0 ]] ; then
		echo -e "\e[1;31mThe following checks failed:\e[0m"
		for cmd in "${failures[@]}" ; do
			echo "  - $cmd"
		done
		return 1
	fi
}

try() {
	echo -e "\e[1m$@\e[0m"
	$@ || mark_fail "$1"
	echo ""
}

failures=()
mark_fail() {
	failures+=("$1")
}

main "$@"
