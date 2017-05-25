#!/usr/bin/env bash

while read A
do
    curl -XPOST http://localhost:9200/info/pred_dollar1/1 -d ' {
        "pred1" : "'$A'"
    } '
done < pred_usd_1.txt


while read A
do
    curl -XPOST http://localhost:9200/info/pred_dollar2/1 -d ' {
        "pred2" : "'$A'"
    } '
done < pred_usd_2.txt
