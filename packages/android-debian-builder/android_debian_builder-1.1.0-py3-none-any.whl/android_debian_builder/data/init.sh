#!/bin/sh
# -*- mode: sh; tab-width: 4; indent-tabs-mode: nil -*-
set -e
PATH=/bin:/usr/bin:/sbin:/usr/sbin

do_start() {
    # Add your own setup commands here. For example:
    # /etc/init.d/ssh start
    echo "Starting Debian."
    {% for cmd in config.extra_setup_commands %}
    {{ cmd }}
    {% endfor %}
}

do_login() {
    # Take necessary steps to launch the desired shell environment.
    bash --login
}

do_stop() {
    # Add your own teardown commands here. For example:
    # /etc/init.d/ssh stop
    echo "Stopping Debian."
    {% for cmd in config.extra_teardown_commands %}
    {{ cmd }}
    {% endfor %}
}

case "$1" in
    start) do_start;;
    login) do_login;;
    stop) do_stop;;
    *) echo "Usage: init.rc start | stop";;
esac
