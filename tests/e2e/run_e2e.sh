#!/bin/bash

./setup.sh
sleep 2

pytest test_*.py

./teardown.sh