#!/bin/bash

the_date=$( date +%F )
git log --pretty="%ae" --since=yesterday $1 | sort | uniq | while read author; do
    git log --author=$author --since=yesterday $1 #> "$the_date"_"$author".txt
done
