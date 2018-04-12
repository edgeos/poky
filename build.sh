#!/usr/bin/env bash

set -e

NAME="poky"
REG="registry.gear.ge.com/predix_edge"

versionsDir="$(dirname "$(readlink -f "$BASH_SOURCE")")/versions"
cd "$versionsDir"

declare archs="$@"

[[ "$1" ]] || {
	archs="$(ls -d -- */)"
}

for arch in $archs; do
	arch=${arch%/}
	cd "$versionsDir/$arch"

	versions=( */ )
	versions=( "${versions[@]%/}" )

	for version in "${versions[@]}"; do
		echo "$arch/$version"
		cd "$versionsDir/$arch/$version"
		docker build --force-rm -t "$REG/$NAME-$arch:$version" \
			--build-arg http_proxy=$http_proxy \
			--build-arg https_proxy=$https_proxy \
			--build-arg no_proxy=$no_proxy \
			.
	done
done
