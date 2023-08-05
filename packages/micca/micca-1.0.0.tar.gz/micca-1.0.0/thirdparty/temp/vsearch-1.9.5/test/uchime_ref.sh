#!/bin/bash

cd ../test

P=$1

INPUT=../../vsearch-data/simm/simm.m1.fa
DB=../../vsearch-data/simm/simm_sp.fa

#INPUT=../../vsearch-data/PR2-18S-rRNA-V4.derep.fsa
#DB=../../vsearch-data/PR2-18S-rRNA-V4.ref.fsa

THREADS=0

UCHIME=$(which uchime)
USEARCH=$(which usearch)
VSEARCH=../bin/vsearch

MINH=0.28
MINDIV=0.8

if [ "$P" == "u" ]; then
    PROG=$USEARCH
else
    if [ "$P" == "v" ]; then
        PROG=$VSEARCH
    else
        if [ "$P" == "o" ]; then
            PROG=$UCHIME
        else
            echo You must specify u or v or o as first argument
            exit
        fi
    fi
fi

if [ "$P" == "o" ]; then

    CMD="/usr/bin/time $PROG \
        --input $INPUT \
        --db $DB \
        --uchimeout $P.uchimeout \
        --uchimealns $P.uchimealns \
        --minh $MINH \
        --mindiv $MINDIV"

else

    CMD="/usr/bin/time $PROG \
      --uchime_ref $INPUT \
      --db $DB \
      --strand plus \
      --chimeras $P.chimeras \
      --nonchimeras $P.nonchimeras \
      --uchimealns $P.uchimealns \
      --uchimeout $P.uchimeout \
      --minh $MINH \
      --mindiv $MINDIV"

fi
    
echo uchime_ref test
echo
echo Running command: $CMD
echo

$CMD
