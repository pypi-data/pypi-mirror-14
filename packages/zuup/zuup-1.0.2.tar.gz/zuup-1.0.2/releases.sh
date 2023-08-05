#!/bin/bash

set -e
set -x

version=$1

status=$(git status -sz)
[ -z "$status" ] || false
git checkout master
git push 
git tag -s $version -m "Release version ${version}"
git checkout $version
git clean -fd
rm -rf zuup.egg-info build dist
tox -epep8,py27,py34
tox -r -evenv python setup.py sdist bdist_wheel

set +x
echo
echo "release: zuup ${version}"
echo
echo "SHA1sum: "
sha1sum dist/*
echo "MD5sum: "
md5sum dist/*
echo
echo "uploading..."
echo
set -x

git push --tags
twine upload -r pypi -s dist/zuup-${version}.tar.gz dist/zuup-${version}-py2.py3-none-any.whl
git checkout master
