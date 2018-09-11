#!/usr/bin/env sh
mkdir coverage
aws s3 cp --recursive s3://com-gavinroy-travis/pamqp/${TRAVIS_BUILD_NUMBER}/ coverage
cd coverage
coverage combine
cd ..
mv coverage/.coverage .
coverage report