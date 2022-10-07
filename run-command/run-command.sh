#!/bin/bash
args=()
for a in "$@"
do
    if [ $a != 'no-arg' ] ; then
        args+=( $a )
    fi
done

"${args[@]}"
exit $?
