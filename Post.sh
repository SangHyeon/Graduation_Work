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

curl -XPUT http://localhost:9200/info/ -d ' {
    "mappings" : {
        "new_dollar" : {
            "properties" : {
                "new_price" : { "type" : "double" },
                "weight" : { "type" : "double" },
                "new_date" : { 
                    "type" : "date", 
                    "format" : "yyyy.MM.dd"
                }
            }
        },
        "pred_dollar1" : {
            "properties" : {
                "pred1" : { "type" : "double" }
            }
        },
        "pred_dollar2" : {
            "properties" : {
                "pred2" : { "type" : "double" }
            }
        }
    }
} '

