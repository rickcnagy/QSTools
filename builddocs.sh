#!/bin/sh

# this script is called from .git/hooks/pre-commit to build docs at each commit


source ~/.bash_profile
wd=$(pwd);

'./utility/readme_generator.py' "$wd/api" "API Scripts"
git add api/README.md

'./utility/readme_generator.py' "$wd/gui" "GUI Scripts"
git add gui/README.md
