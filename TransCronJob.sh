#!/bin/bash

posturl="http://127.0.0.1:8095/mycronjob/"
curl -d "" $posturl

sleep 1
postMergeurl="http://127.0.0.1:8095/myMergejob/"
curl -d "" $postMergeurl
