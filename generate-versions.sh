#!/usr/bin/env bash
set -eo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

archs='amd64'

declare -A rels=(
	[amd64]='pyro'
)

declare -A pokyVersion=(
	[amd64-pyro]='2.3.2'
)

declare -A ubuntuVersion=(
	[amd64-pyro]='16.04'
)

for arch in $archs; do
	for rel in ${rels[$arch]}; do
		dockerfilePath="versions/$arch/${rel}"

		mkdir -p $dockerfilePath
		cp poky-deps.tar.gz $dockerfilePath/poky-deps.tar.gz

		sed -e s~#{ARCH}~"$arch"~g \
			-e s~#{POKY_VERSION}~"${pokyVersion[$arch-$rel]}"~g \
			-e s~#{UBUNTU_VERSION}~"${ubuntuVersion[$arch-$rel]}"~g \
			Dockerfile.template > $dockerfilePath/Dockerfile
	done
done
