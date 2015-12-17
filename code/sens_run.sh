#!/bin/bash

declare -a casenams=("T213BL03S10P60" \
                     "T215BL03S10P60" "T220BL03S10P60" \
                     "T225BL03S10P60" "T230BL03S10P60" \
                     "T235BL03S10P60" "T240BL03S10P60" \
                     "T245BL03S10P60" "T253BL03S10P60")

for casenam in "${casenams[@]}"; do
#for casenam in "T245BL03S10P60"; do
  tbb=${casenam:1:3}
  spares=${casenam:9:2}
  arecod=${casenam:4:1}

  if [ "${arecod}" = "B" ] ; then
    area='2400.0'
  else
    area='5000.0'
  fi
  
  # mccSearchUI.py
  # line 32
  outdir="\"mainDirStr\"\t:\t\"\/Users\/nsagitap\/output\/GTG\/sensitivity_200703\/"${casenam}"\","
  # line 35
  if [ "${spares}" = "04" ] ; then
    indir="\"CEoriDirName\"\t:\t\"\/Users\/nsagitap\/data\/MTSAT\/Indonesia\/200703\/\""
  else
    indir="\"CEoriDirName\"\t:\t\"\/Users\/nsagitap\/data\/MTSAT\/Indonesia\/200703\/S"${spares}"\""
  fi

  # mccSearch.py
  # line 33 34
  xres="XRES="${spares}".0"
  yres="YRES="${spares}".0"
  # line 45
  tbbmax="T_BB_MAX="${tbb}
  # line 50
  areamin="AREA_MIN="${area}
  
  # mccSearchUI
  sed -i "32s/.*/"${outdir}"/" mccSearchUI.py
  sed -i "35s/.*/"${indir}"/" mccSearchUI.py
  # mccSearch
  sed -i "33s/.*/"${xres}"/" mccSearch.py
  sed -i "34s/.*/"${yres}"/" mccSearch.py
  sed -i "45s/.*/"${tbbmax}"/" mccSearch.py
  sed -i "50s/.*/"${areamin}"/" mccSearch.py
  # iomethods
  sed -i "29s/.*/"${xres}"/" iomethods.py
  sed -i "30s/.*/"${yres}"/" iomethods.py
  sed -i "41s/.*/"${tbbmax}"/" iomethods.py
  sed -i "46s/.*/"${areamin}"/" iomethods.py
  
  python mccSearchUI.py
done