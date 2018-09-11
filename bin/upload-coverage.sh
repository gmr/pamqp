#!/usr/bin/env sh
if [ "${TRAVIS_REPO_SLUG}" = "gmr/pamqp" ];
then
    echo "Uploading coverage for ${TRAVIS_PYTHON_VERSION} to S3"
    aws s3 cp .coverage "s3://com-gavinroy-travis/pamqp/$TRAVIS_BUILD_NUMBER/.coverage.${TRAVIS_PYTHON_VERSION}"
fi