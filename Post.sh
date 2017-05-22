#!/usr/bin/env bash

curl -XPUT http://localhost:9200/currency/ -d ' {
    "mappings" : {
        "dollar" : {
            "properties" : {
                "date" : { "type" : "date" },
                "price" : { "type" : "long" }
            }
        }
    }
} '


curl -XPUT http://localhost:9200/words/ -d ' {
    "mappings" : {
        "word" : {
            "properties" : {
                "tag" : { "type" : "string" },
                "freq" : { "type" : "long" }
            }
        }
    }
} '
