#!/bin/bash

while read A B
do
    curl -XPOST http://localhost:9200/currency/dollar -d ' {
        "date" : "'$A'",
        "price" : "'$B'"
    } '
done < elas_data.txt
