#!/usr/bin/env bash

while read A B C
do
    echo "${A} ${B} ${C}"
    curl -XPOST http://localhost:9200/info/new_dollar/1 -d ' {
        "new_price" : "'$A'",
        "weight" : "'$B'",
        "new_date" : "'$C'"
    } '
done < usd.txt
