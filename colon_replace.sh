#!/bin/bash

#for mangakakalot_dl

if [ "$#" -eq "0" ]
  then
    cd .
else
    cd $1
fi

#Replace all colons with an underscore
for filename in *":"*; do
    mv -- "$filename" "${filename//:/_}"
done
