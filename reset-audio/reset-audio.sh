#!/bin/bash

CARD=$(pactl list cards short | grep bluez | awk '{print $2}')
CURRENT_PROFILE=$(pactl list cards | grep -A 30 "$CARD" | grep "Active Profile:" | awk '{print $3}')

if [[ "$CURRENT_PROFILE" == "a2dp-sink"* ]]; then
   pactl set-card-profile "$CARD" headset-head-unit
   sleep 0.3
   pactl set-card-profile "$CARD" a2dp-sink
   notify-send "Audio Reset" "headset to handsfree but back to headset hehehe"
elif [[ "$CURRENT_PROFILE" == "headset-head-unit"* ]]; then
   pactl set-card-profile "$CARD" a2dp-sink
   sleep 0.3
   pactl set-card-profile "$CARD" headset-head-unit
   notify-send "Audio Reset" "handsfree to headset but back to handsfree aseek"
else
   notify-send "Audio Reset" "unknown profile: $CURRENT_PROFILE"
fi
