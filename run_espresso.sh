#!/bin/bash
set -e

main() {
    input_path=$1
    espresso_option=$2
    output_dnf=${input_path}_${espresso_option}.dnf

    START_TIME=`date +%Y/%m/%d/%H:%M:%S`
    ST=`date +%s.%N`
    echo "solve start time is: ${START_TIME}"

    ./espresso -e ${espresso_option} -o eqntott ${input_path} > ${output_dnf}

    ED=`date +%s.%N`
    END_TIME=`date +%Y/%m/%d/%H:%M:%S`
    echo "solve end time is: ${END_TIME}"

    set +e
    EXECUTING_TIME=$(printf "%.6f" `echo "${ED} - ${ST}" | bc`)
    set -e
    echo "Option is: ${espresso_option}, solve exec time is: ${EXECUTING_TIME}s"
    echo "input file is: ${input_path}"
}

main $@