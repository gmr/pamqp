#!/usr/bin/env sh
if [ "${TRAVIS_REPO_SLUG}" -eq "gmr/pamqp" ];
then
    aws s3 cp .coverage "s3://com-gavinroy-travis/pamqp/$TRAVIS_BUILD_NUMBER/.coverage.${TRAVIS_PYTHON_VERSION}"
fi