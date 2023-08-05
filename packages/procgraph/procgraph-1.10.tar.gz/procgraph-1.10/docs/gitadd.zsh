#!/bin/zsh
cd $1
git add **/*
git commit -a -m "added"
exit 0