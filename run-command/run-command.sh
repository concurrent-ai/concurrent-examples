#!/bin/bash
echo "run-command.sh. Entered. Arguments: $1 $2 $3 $4 $5"
args=()
for a in "$@"
do
    if [ $a != 'no-arg' ] ; then
        args+=( $a )
    fi
done

"${args[@]}"
exit $?
