#!/bin/bash
# -*- coding: utf-8 -*-
# :Project:   SoL -- Docker entry point script
# :Created:   mer 30 mar 2016 21:34:31 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

set -e

case $1 in
    start)
        echo "Starting SoL server..."
        exec pserve config.ini
        ;;

    shell)
        /bin/bash
        ;;

    *)
        exec soladmin $@
        ;;
esac
