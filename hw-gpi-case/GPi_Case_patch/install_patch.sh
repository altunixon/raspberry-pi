#!/usr/bin/env bash

set -o pipefail

patch_dir="${1:-}"
boot_conf="config.txt"
boot_cmdl="cmdline.txt"
boot_overlay_video="dpi24-gpi.dtbo"
boot_overlay_audio="pwm-audio-pi-zero-gpi.dtbo"

backup_date=$(date +%Y%m%d-%H%M)
backup_path="./original_files/${backup_date}"

patch_help="Usage:\n\t$0 <patch_folder>\n\nPatch Folder content structure:\n\t<patch_folder>/$boot_conf\n\t<patch_folder>/$boot_cmdl\n\t<patch_folder>/overlays/$boot_overlay_video\n\t<patch_folder>/overlays/$boot_overlay_audio\n\nBackups available at:\n\t'$backup_path'\n\nRollback is simply running this script on the backup folder, ie:\n\t$0 '$backup_path'\n"
if [ -z $1 ] || [ ! -d "$1" ]; then
    echo -e "$patch_help"
    exit 1
fi

mkdir -p "${backup_path}/overlays"

function swap_bootcnf() {
    if [ $(diff "/boot/$1" "${patch_dir%%/}/$1" | wc -l) -gt 0 ]; then
        echo "Swapping Config"
        sudo mv -v --no-clobber "/boot/$1" "${backup_path}/"
        sudo cp -v --no-clobber "${patch_dir%%/}/$1" /boot/
    else
        echo "$1 havent changed, SKIP"
    fi
}

function swap_overlay() {
    if [ ! -f "/boot/overlays/$1" ] || [ $(md5sum "/boot/overlays/$1" | awk '{print $1}') != $(md5sum "${patch_dir%%/}/overlays/$1" | awk '{print $1}') ]; then
        echo "Swapping $1"
        sudo mv -v --no-clobber "/boot/overlays/$1" "${backup_path%%/}/overlays/"
        sudo cp -v --no-clobber "${patch_dir%%/}/overlays/$1" /boot/overlays/
    else
        echo "$1 havent changed, SKIP"
    fi
}

swap_bootcnf "$boot_conf"
swap_bootcnf "$boot_cmdl"
swap_overlay "$boot_overlay_video"
swap_overlay "$boot_overlay_audio"
