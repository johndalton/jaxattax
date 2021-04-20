#!/bin/bash

main() {
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

main
