#!/bin/sh

Xvfb :1 & xvfb-run sonic-pi 2 >/dev/null &
