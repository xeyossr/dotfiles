#!/usr/bin/env sh
# Rofi menu for Quick Edit / View of Settings (SUPER E)

# define your preferred text editor and terminal to use
editor=${EDITOR:-nano}
tty=kitty

configs="$HOME/.config/hypr/configs"
HyprConfig="$HOME/.config/hypr"
WaybarConfig="$HOME/.config/waybar"
# Set rofi scaling
[[ "${rofiScale}" =~ ^[0-9]+$ ]] || rofiScale=10
r_scale="configuration {font: \"JetBrainsMono Nerd Font ${rofiScale}\";}"

# Evaluate spawn position
readarray -t curPos < <(hyprctl cursorpos -j | jq -r '.x,.y')
readarray -t monRes < <(hyprctl -j monitors | jq '.[] | select(.focused==true) | .width,.height,.scale,.x,.y')
readarray -t offRes < <(hyprctl -j monitors | jq -r '.[] | select(.focused==true).reserved | map(tostring) | join("\n")')
monRes[2]="$(echo "${monRes[2]}" | sed "s/\.//")"
monRes[0]="$(( ${monRes[0]} * 100 / ${monRes[2]} ))"
monRes[1]="$(( ${monRes[1]} * 100 / ${monRes[2]} ))"
curPos[0]="$(( ${curPos[0]} - ${monRes[3]} ))"
curPos[1]="$(( ${curPos[1]} - ${monRes[4]} ))"

if [ "${curPos[0]}" -ge "$((${monRes[0]} / 2))" ] ; then
    x_pos="east"
    x_off="-$(( ${monRes[0]} - ${curPos[0]} - ${offRes[2]} ))"
else
    x_pos="west"
    x_off="$(( ${curPos[0]} - ${offRes[0]} ))"
fi

if [ "${curPos[1]}" -ge "$((${monRes[1]} / 2))" ] ; then
    y_pos="south"
    y_off="-$(( ${monRes[1]} - ${curPos[1]} - ${offRes[3]} ))"
else
    y_pos="north"
    y_off="$(( ${curPos[1]} - ${offRes[1]} ))"
fi

r_override="window{location:${x_pos} ${y_pos};anchor:${x_pos} ${y_pos};x-offset:${x_off}px;y-offset:${y_off}px;border:2px;border-radius:20px;} wallbox{border-radius:20px;} element{border-radius:20px;}"

menu(){
  printf "1. [Hypr] Edit hyprland.conf\n"
  printf "2. [Hypr] Edit windowrules.conf\n"
  printf "3. [Hypr] Edit keybindings.conf\n"
  printf "4. [Hypr] Edit animations.conf\n"
  printf "5. [Hypr] Edit themes/colors.conf\n"
  printf "6. [Hypr] Edit themes/common.conf\n"
  printf "7. [Hypr] Edit themes/theme.conf\n"
  printf "8. [Hypr] Edit pyprland.toml\n"
  printf "9. [Waybar] Edit config.ctl\n"
  printf "10. [Waybar] Edit style.css\n"
}

main() {
    choice=$(menu | rofi -dmenu -theme-str "${r_scale}" -theme-str "${r_override}" -config ~/.config/rofi/clipboard.rasi | cut -d. -f1)
    case $choice in
        1)
            $tty $editor "$HyprConfig/hyprland.conf"
            ;;
        2)
            $tty $editor "$HyprConfig/windowrules.conf"
            ;;
        3)
            $tty $editor "$HyprConfig/keybindings.conf"
            ;;
        4)
            $tty $editor "$HyprConfig/animations.conf"
            ;;
        5)
            $tty $editor "$HyprConfig/themes/colors.conf"
            ;;
        6)
            $tty $editor "$HyprConfig/themes/common.conf"
            ;;
        7)
            $tty $editor "$HyprConfig/themes/theme.conf"
            ;;
        8)
            $tty $editor "$HyprConfig/pyprland.toml"
            ;;
        9)
            $tty $editor "$WaybarConfig/config.ctl"
            ;;
        10)
            $tty $editor "$WaybarConfig/style.css"
            ;;
        *)
            ;;
    esac
}

main