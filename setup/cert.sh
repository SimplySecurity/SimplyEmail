#!/bin/bash

openssl req -new -x509 -keyout ../data/simplyemail.pem -out ../data/simplyemail.pem -days 365 -nodes -subj "/C=US" >/dev/null 2>&1

echo -e "\n\n [*] Certificate written to ../data/simplyemail.pem\n"