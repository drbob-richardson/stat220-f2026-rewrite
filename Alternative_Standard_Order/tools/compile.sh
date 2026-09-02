#!/bin/bash
# Compile a deck twice and report page count + overfull boxes + em dashes.
# usage: tools/compile.sh Module_05_Randomness_and_Probability
cd "$(dirname "$0")/../Slides" || exit 1
NAME="$1"
pdflatex -interaction=nonstopmode -halt-on-error "$NAME.tex" > /dev/null 2>&1
pdflatex -interaction=nonstopmode -halt-on-error "$NAME.tex" > "$NAME.buildlog" 2>&1
STATUS=$?
if [ $STATUS -ne 0 ]; then
  echo "FAILED TO COMPILE: $NAME"
  grep -n -A4 "^!" "$NAME.buildlog" | head -40
  exit 1
fi
PAGES=$(tr -d '\n' < "$NAME.buildlog" | grep -o "Output written on $NAME.pdf ([0-9]*" | grep -o "[0-9]*$")
VBOX=$(grep -c "Overfull \\\\vbox" "$NAME.buildlog")
HBOX=$(grep -c "Overfull \\\\hbox" "$NAME.buildlog")
EMD=$(grep -c "—" "$NAME.tex")
echo "$NAME: pages=$PAGES  overfull_vbox=$VBOX  overfull_hbox=$HBOX  emdashes=$EMD"
if [ "$VBOX" -gt 0 ]; then
  echo "--- vbox locations ---"
  grep -n -A2 "Overfull \\\\vbox" "$NAME.buildlog" | grep -oE "has occurred while \\\\output is active|\[[0-9]+\]" | head -20
  grep -n "Overfull \\\\vbox" "$NAME.buildlog" | head -20
fi
