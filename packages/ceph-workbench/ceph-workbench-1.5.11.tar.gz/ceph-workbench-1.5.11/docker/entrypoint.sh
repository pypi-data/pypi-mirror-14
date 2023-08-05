#!/bin/bash

CONF_DIR='/opt/.ceph-workbench'

function get_openrc() {
    while [ $# -ge 1 ] ; do
        if test "$1" = '--openrc' ; then
            shift
            echo "$1"
            return
        elif echo $1 | grep --quiet '^--openrc=' ; then
            echo $1 | sed -e 's/^--openrc=//'
            return
        fi
        shift
    done
    echo "openrc.sh"
}

function source_openrc() {
    local openrc=$(get_openrc "$@")
    if test -f $CONF_DIR/$openrc ; then
        source $CONF_DIR/$openrc
    else
        echo "~/.ceph-workbench/$openrc" does not exist >&2
        return 1
    fi
}


function run() {
    source_openrc "$@"
    adduser --disabled-password --gecos Teuthology --quiet --uid $USER_ID $USER_NAME
    if ! test -d /home/$USER_NAME/.ceph-workbench ; then
        ln -s /opt/.ceph-workbench /home/$USER_NAME/.ceph-workbench
    fi
    sudo --set-home --preserve-env --user $USER_NAME "$@"
}

function run_tests() {
    shopt -s -o xtrace
    PS4='${BASH_SOURCE[0]}:$LINENO: ${FUNCNAME[0]}:  '

    test 'foo.sh' = $(get_openrc --openrc foo.sh) || return 1
    test 'bar.sh' = $(get_openrc --openrc=bar.sh) || return 1
    test 'openrc.sh' = $(get_openrc) || return 1

    CONF_DIR=$HOME/.ceph-workbench
    rm -f $CONF_DIR/UNLIKELY.sh
    ! source_openrc --openrc UNLIKELY.sh || return 1
    mkdir -p $CONF_DIR
    echo VAR=VALUE | tee $CONF_DIR/UNLIKELY.sh
    source_openrc --openrc UNLIKELY.sh || return 1
    test $VAR = VALUE || return 1
    rm $CONF_DIR/UNLIKELY.sh
}

if test "$1" = TESTS ; then
    run_tests
else
    run "$@"
fi
