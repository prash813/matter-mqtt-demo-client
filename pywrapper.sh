#! /bin/sh
export DEBUG="$(snapctl get debug)"
export NWIFACE="$(snapctl get nwiface)"
$SNAP/bin/python3 $SNAP/firstapp.py
