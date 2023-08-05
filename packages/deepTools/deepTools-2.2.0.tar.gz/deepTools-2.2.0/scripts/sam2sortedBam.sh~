#!/bin/sh
if [ -z "$1" ]
then
    echo "$0: Usage $0: <file.sam> <file (without bam ending)>"
    exit 3
fi

if [ ! -r $1 ]
then
    echo $0: File $1 does not exists.
    exit 1
fi

/package/samtools/samtools view -uS $1 | /package/samtools/samtools sort - $2
/package/samtools/samtools index  $2.bam

