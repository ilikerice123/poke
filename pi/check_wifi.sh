#!/bin/bash
ping -q -w 1 -c 1 google.com > /dev/null && echo ok || echo error