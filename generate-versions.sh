#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

archs='amd64'

declare -A rels=(
	[amd64]='1.0'
)

declare -A ubuntuVersion=(
	[amd64-1.0]='14.04'
)

for arch in $archs; do
	for rel in ${rels[$arch]}; do
		dockerfilePath="versions/$arch/${rel}"

		mkdir -p $dockerfilePath
		cp poky-deps.tar.gz $dockerfilePath/poky-deps.tar.gz

		sed -e s~#{ARCH}~"$arch"~g \
			-e s~#{UBUNTU_VERSION}~"${ubuntuVersion[$arch-$rel]}"~g \
			Dockerfile.template > $dockerfilePath/Dockerfile
	done
done
