#!/bin/sh

# this script is called from .git/hooks/pre-commit to build docs at each commit


source ~/.bash_profile
wd=$(pwd);
diffed_files=$(git diff --cached --name-only)

# params: directory, name
function build_doc {
    dir="$wd$1"
    name=$2
    
    last_path=$(basename $dir)
    if [[ $diffed_files =~ .*$last_path.* ]]; then
        './utility/readme_generator.py' "$dir" "$name"
        if [ $? != 0 ]; then
            echo "Doc build failed for dir: $dir" > ./build.log
            exit 1;
        fi
        git add "./$1/README.md"
    fi
}

function docs_finished {
    d=$(date)
    echo "All docs built successfully on $d" > ./build.log
}

# build all docs
build_doc '/api' 'API Scripts'
build_doc '/gui' 'GUI Scripts'
build_doc '/gui/Transcripts' 'Transcript GUI Scripts'
build_doc '/utility' 'Utility Scripts'
build_doc '/modules' 'QSTools Modules'
build_doc '/modules/qs' '`qs` Python Package'
build_doc '/csv' 'CSV Scripts'
docs_finished

# fix all whitespace in Python files
while read -r filename; do
    if [[ $filename =~ .*\.py ]]; then
        reindent --nobackup ./$filename
        git add $filename
    fi
done <<< "$diffed_files"
