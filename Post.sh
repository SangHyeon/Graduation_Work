#!/usr/bin/env bash

curl -XPUT http://localhost:9200/currency/ -d ' {
    "mappings" : {
        "dollar" : {
            "properties" : {
                "date" : { 
                    "type" : "date",
                    "format" : "yyyy.MM.dd"
                },
                "price" : { "type" : "double" }
            }
        }
    }
} '


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
