#!/bin/bash
wget -O- "http://localhost:8983/solr/aiml/select?indent=true&wt=json&q=$1"
