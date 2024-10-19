#!/bin/bash
# Rofi menu for Quick Edit / View of Settings (SUPER E)

# define your preferred text editor and terminal to use
editor=${EDITOR:-nano}
tty=kitty

configs="$HOME/.config/hypr/configs"
UserConfigs="$HOME/.config/hypr/UserConfigs"

[[ "${rofiScale}" =~ ^[0-9]+$ ]] || rofiScale=10
r_scale="configuration {font: \"JetBrainsMono Nerd Font ${rofiScale}\";}"
elem_border=$(( hypr_border * 3 ))


menu(){
  printf "1. edit Env variables\n"
  printf "2. edit Window Rules\n"
  printf "3. edit Startup Apps\n"
  printf "4. edit Keybinds\n"
  printf "5. edit Settings\n"
}

main() {
    choice=$(menu | rofi -dmenu -theme-str "${r_scale}" -config ~/.config/rofi/selector.rasi | cut -d. -f1)
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