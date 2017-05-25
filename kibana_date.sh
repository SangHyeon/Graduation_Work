#!/bin/bash

while read A B C
do
    curl -XPOST http://localhost:9200/currency/dollar -d ' {
        "date" : "'$C'",
        "price" : "'$A'"
    } '
done < usd.txt
