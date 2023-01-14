#!/bin/bash

./setup.sh
sleep 2

cd ../..

pytest -m e2e

cd -

./teardown.sh