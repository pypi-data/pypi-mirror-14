#!/usr/bin/env bash

# The usage
USAGE="$0 -e|--exclude SAMPLE[,SAMPLE,SAMPLE,...] -i|--impute2 FILE -s|--sample FILE"


# Parsing the arguments
while [[ $# > 1 ]]
do
    key="$1"

    case $key in
        -e|--exclude)
            SAMPLES="$2"
            shift
            ;;

        -i|--impute2)
            I_FN="$2"
            shift
            ;;

        -s|--sample)
            SAMPLE_FN="$2"
            shift
            ;;

        *)
            >&2 echo "$1: unknown option"
            exit 1
            ;;
    esac
    shift
done


# Checking we have samples
if [ -z "$SAMPLES" ]
then
    >&2 echo "missing -e|--exclude"
    >&2 echo $USAGE
    exit 1
fi


# Checking we have IMPUE2 file
if [ -z "$I_FN" ]
then
    I_FN=/dev/stdin
fi


# Checking we have sample file
if [ -z "$SAMPLE_FN" ]
then
    >&2 echo "missing -s|--sample"
    >&2 echo $USAGE
    exit 1
elif [ ! -e "$SAMPLE_FN" ]
then
    >&2 echo "$SAMPLE_FN: no such file"
    exit 1
fi


# Creating the REGEX
REGEX="($(echo $SAMPLES | sed -e "s/,/)|(/g"))"


# Finding the columns for each sample
COLS=$(
    egrep -nw $REGEX <(sed -e 1,2d $SAMPLE_FN \
        | cut -d " " -f 2) \
        | cut -d ":" -f 1 \
        | sort -n -u
)

# Checking we have samples
if [ -z "$COLS" ]
then
    >&2 echo "no samples to extract"
    exit 1
fi


# Creating the cut string
CUT_STRING=$(
    for COL in $COLS
    do
        STARTCOL=$(( ((COL -1) * 3) + 6 ))
        echo $STARTCOL
        echo $(( STARTCOL + 1 ))
        echo $(( STARTCOL + 2 ))
    done | tr "\n" "," | sed -e "s/,$//"
)


# Cutting
cut -d " " -f $CUT_STRING --complement $I_FN
