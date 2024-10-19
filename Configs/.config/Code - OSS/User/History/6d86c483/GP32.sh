#!/bin/bash
# Rofi menu for Quick Edit / View of Settings (SUPER E)

# define your preferred text editor and terminal to use
editor=${EDITOR:-nano}
tty=kitty

configs="$HOME/.config/hypr/configs"
UserConfigs="$HOME/.config/hypr/UserConfigs"

# Set rofi scaling
[[ "${rofiScale}" =~ ^[0-9]+$ ]] || rofiScale=10
r_scale="configuration {font: \"JetBrainsMono Nerd Font ${rofiScale}\";}"
wind_border=$((hypr_border * 3 / 2))
elem_border=$([ $hypr_border -eq 0 ] && echo "5" || echo $hypr_border)

r_override="window{location:${x_pos} ${y_pos};anchor:${x_pos} ${y_pos};x-offset:${x_off}px;y-offset:${y_off}px;border:${hypr_width}px;border-radius:${wind_border}px;} wallbox{border-radius:${elem_border}px;} element{border-radius:${elem_border}px;}"

menu(){
  printf "1. edit Env variables\n"
  printf "2. edit Window Rules\n"
  printf "3. edit Startup Apps\n"
  printf "4. edit Keybinds\n"
  printf "5. edit Settings\n"
}

main() {
    choice=$(menu | rofi -dmenu -theme-str "${r_scale}" -config ~/.config/rofi/clipboard.rasi | cut -d. -f1)
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