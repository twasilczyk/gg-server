#!/bin/sh

protoc -I=. --python_out=. packets.proto
