#!/bin/bash
# Rofi menu for Quick Edit / View of Settings (SUPER E)

# define your preferred text editor and terminal to use
editor=${EDITOR:-nano}
tty=kitty

configs="$HOME/.config/hypr/configs"
UserConfigs="$HOME/.config/hypr/UserConfigs"

menu(){
  printf "1. edit Env variables\n"
  printf "2. edit Window Rules\n"
  printf "3. edit Startup Apps\n"
  printf "4. edit Keybinds\n"
  printf "5. edit Settings\n"
}

main() {
    choice=$(menu | rofi -i -dmenu -config ~/.config/rofi/config-compact.rasi | cut -d. -f1)
    case $choice in
        1)
            $tty $editor "$UserConfigs/env.conf"
            ;;
        2)
            $tty $editor "$UserConfigs/windowrules.conf"
            ;;
        3)
            $tty $editor "$UserConfigs/autostart.conf"
            ;;
        4)
            $tty $editor "$UserConfigs/binds.conf"
            ;;
        5)
            $tty $editor "$UserConfigs/settings.conf"
            ;;
        *)
            ;;
    esac
}

main
