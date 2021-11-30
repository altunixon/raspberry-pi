#!/usr/bin/env bash

set -u
set -o pipefail

fbcp_env=$(command -v fbcp)
fbcp_bin=${1:-$fbcp_env}
[ -z "$fbcp_bin" ] && fbcp_bin='/usr/bin/fbcp'
fbcp_timestamp=$(date '+%Y%m%d-%H%M%S')

if [ -L "$fbcp_bin" ] || [ ! -f "$fbcp_bin" ]; then
    install_method='ln'
else
    install_method='cp'
fi

case $install_method in
    ln)
        [ -L "$fbcp_bin" ] && \
            fbcp_now=$(readlink -f ${fbcp_bin}) || \
            fbcp_now=''
        echo -e "[${install_method^^}] Change fbcp Driver: ${fbcp_bin} -> [${fbcp_now}]"
    ;;
    cp)
        [ -f "$fbcp_bin" ] && \
            fbcp_now=$(md5sum "${fbcp_bin}" | awk '{print $1}') || \
            fbcp_now=''
        echo -e "[${install_method^^}] Change fbcp Driver: ${fbcp_bin}"
    ;;
esac

fbcp_avail=($(find /usr/bin -maxdepth 1 -type f -iname 'fbcp*'))
[ ${#fbcp_avail[@]} -eq 0 ] && exit 1

PS3="[${install_method^^}] Select fbcp driver to install: "
select fbcp_sel in  ${fbcp_avail[@]}
do
    if [ -z "$fbcp_sel" ]; then
        echo -e "[${install_method^^}] Invalid Selection"
        exit 1
    fi
    case $install_method in
    ln)
        if [ -L "$fbcp_bin" ]; then
            if [ "$fbcp_now" == "$fbcp_sel" ]; then
                echo -e "[LN] Selected Version already installed:\n   Current: ${fbcp_now} <- ${fbcp_bin}\n  Selected: ${fbcp_sel}"
                exit 0
            fi
            echo -e "[LN] Unlink Previous:\n   Current: ${fbcp_now} <- ${fbcp_bin}"
            sudo unlink "$fbcp_bin"
        fi
        sudo ln -s "${fbcp_sel}" "${fbcp_bin}"
        fbcp_rc=$?
        echo -e "[LN] Installed Version:\n  Selected: $(readlink -f ${fbcp_bin})"
        exit $fbcp_rc
    ;;
    cp)
        if [ -f "$fbcp_bin" ]; then
            fbcp_new=$(md5sum "${fbcp_sel}" | awk '{print $1}')
            if [ "$fbcp_now" == "$fbcp_new" ]; then
                echo -e "[CP] Selected Version already installed:\n   Current: ${fbcp_now}  ${fbcp_bin}\n  Selected: ${fbcp_new}  ${fbcp_sel})"
                exit 0
            fi

            fbcp_backup="${fbcp_bin}_${fbcp_timestamp}"
            echo -e "[CP] Backup Current:\n   Current: ${fbcp_bin}  ${fbcp_now}\n    Backup: ${fbcp_backup}"
            [ ! -f "$fbcp_backup" ] && \
                sudo mv -vf "${fbcp_bin}" "${fbcp_backup}" || \
                exit 1
            sudo cp -vf "${fbcp_sel}" "${fbcp_bin}"
            fbcp_rc=$?
            echo -e "[CP] Installed Version:\n  $(md5sum ${fbcp_bin})\n  Selected: ${fbcp_new}  ${fbcp_sel}"
            exit $fbcp_rc
        fi
    ;;
    esac
done