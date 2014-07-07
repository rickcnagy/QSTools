#!/bin/sh

# this script is called from .git/hooks/pre-commit to build docs at each commit


source ~/.bash_profile
wd=$(pwd);

# params: directory, name
function build_doc {
	dir="$wd$1"
	name=$2
	'./utility/readme_generator.py' "$dir" $name
	if [ $? != 0 ]; then
		echo "Doc build failed for dir: $dir" > ./build.log
		exit 1;
	fi
}

function finished {
	d=$(date)
	echo "Docs built successfully on $d" > ./build.log
}

build_doc '/api' 'API Scripts'
build_doc '/gui' 'GUI Scripts'
build_doc '/gui/Report Cards' 'Report Card GUI Scripts'
build_doc '/gui/Transcripts' 'Transcript GUI Scripts'
finished
