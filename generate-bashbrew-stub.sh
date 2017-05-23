#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

NAME="poky"

# get the most recent commit which modified any of "$@"
fileCommit() {
	git log -1 --format='format:%H' HEAD -- "$@"
}

# get the most recent commit which modified "$1/Dockerfile" or any file COPY'd from "$1/Dockerfile"
dirCommit() {
	local dir="$1"; shift
	(
		cd "$dir"
		fileCommit \
			Dockerfile \
			$(git show HEAD:./Dockerfile | awk '
				toupper($1) == "COPY" {
					for (i = 2; i < NF; i++) {
						print $i
					}
				}
			')
	)
}

# prints "$2$1$3$1...$N"
join() {
	local sep="$1"; shift
	local out; printf -v out "${sep//%/%%}%s" "$@"
	echo "${out#$sep}"
}

declare -A aliases=(
	[morty]='latest'
)

[[ "$1" ]] || {
	echo "must have 1 repo argument"
	exit 1
}

declare repo="$1"
declare self="$(basename "$BASH_SOURCE")"
cd "$(dirname "$(readlink -f "$BASH_SOURCE")")/versions/$repo"

cat <<-EOH
# this file is generated via https://github.build.ge.com/PredixEdgeLibrary/$NAME/$self
Maintainers: Adam McCann <mccann@ge.com> (@200018171)
GitRepo: https://github.build.ge.com/PredixEdgeLibrary/$NAME.git
EOH

versions=( */ )
versions=( "${versions[@]%/}" )

for version in "${versions[@]}"; do
	commit="$(dirCommit "$version")"

	fullVersion="$(git show "$commit":"versions/$repo/$version/Dockerfile" | awk '$1 == "ENV" && $2 == "POKY_VERSION" { gsub(/~/, "-", $3); print $3; exit }')"

	versionAliases=(
		$version
		$fullVersion
	)
	versionAliases+=(
		${aliases[$version]:-}
	)

	echo
	cat <<-EOE
		Tags: $(join ', ' "${versionAliases[@]}")
		GitCommit: $commit
		Directory: versions/$repo/$version
	EOE

done
