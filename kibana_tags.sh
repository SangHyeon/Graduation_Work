#!/bin/bash

curl -XDELETE 'http://localhost:9200/words'

curl -XPUT http://localhost:9200/words/ -d ' {
    "mappings" : {
        "word" : {
            "properties" : {
                "tag" : { "type" : "string" },
                "freq" : { "type" : "integer" }
            }
        }
    }
} '

while read A B
do
    curl -XPOST http://localhost:9200/words/word -d ' {
        "tag" : "'$A'",
        "freq" : "'$B'"
    } '
done < words_data.txt
