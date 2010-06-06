#!/bin/bash
#
# Write memory- and disk-status with some nice color-graphs :) 
# To get stats, the file "/proc/meminfo" and the commands "df" 
# and "uptime" are used
# 17 Sep, 1997, Tompi ( Thomas Haukland, s770@ii.uib.no )
# Edited by Markku 31-October-2004 (rasat@pacific.net.sg)

#################################################################
# First set which colors to use, and how long the graphs will be:
#################################################################

l=30;    # Graphs will be $l chars long
r_c="\033[m";         # Reset color-code
u_c="\033[32;41m";    # Used space will be red
f_c="\033[32;42m";    # Unused space will be green
s_c="\033[34;44m";    # Shared, buffers, cached will be blue
w_c="\033[36;40m";   # Writing will be done with blue
h_c="\033[33;40;1m";  # Highlight with yellow
l1_c="\033[35;40;1m";           # First line(version etc) is bright purple
l2_c="\033[35;40m";             # Second line(cpu etc) is purple

#######################################################################################
# Output /proc/version and exec 'uptime'
#######################################################################################

echo -e "\033[0;36mSYSTEM INFO"
echo -en "$r_c "; cut -f 1 -d \# /proc/version;
echo ""
# echo -en "$r_c$l2_c"; uptime; echo -en "$r_c"
echo -en "$r_c"

set `cat /proc/meminfo`
#########################################################################
# Now $8 will be total memory, $9 used memory, $11 shared, $15 swap-total 
# $16 swap-used, $12 buffers and $13 cached. Now do some arithmetic:
#########################################################################

cd /tmp
grep MemTotal /proc/meminfo >sch1.tmp
awk '{ print $2 }' sch1.tmp >sch2.tmp
MemTot="$(cat sch2.tmp)"
rm *.tmp

grep MemFree /proc/meminfo >sch1.tmp
awk '{ print $2 }' sch1.tmp >sch2.tmp
MemFree="$(cat sch2.tmp)" 
rm *.tmp

Memunused=$[($MemTot - $MemFree) * 100 / $MemTot]

grep SwapTotal /proc/meminfo >sch1.tmp
awk '{ print $2 }' sch1.tmp >sch2.tmp
SwapTot="$(cat sch2.tmp)"
rm *.tmp

grep SwapFree /proc/meminfo >sch1.tmp
awk '{ print $2 }' sch1.tmp >sch2.tmp
SwapFree="$(cat sch2.tmp)" 
rm *.tmp

Swapunused=$[($SwapTot - $SwapFree) * 100 / $SwapTot]

########################################################################
# Declaring a function which will print the mem, swap, buffer, shared
# and cached graphs using these parameters:
# $1: First text-string, $2: Free, $3: Free-color, 
# $4: Used-color, $5: Used-Kb, $6: Total-Kb
########################################################################

function write_graph () {
 echo -en "$w_c $1$4";
 printf "%${2}s" ""; echo -en "$3";
 printf "%$((${l} - ${2}))s" "";
 echo -e "$h_c $5$r_c$w_c$6 Kb used."; 
 }

######################################################
# Write memory, swap, shared, buffer and cache-graphs:

# write_graph  "Memory        : "
# write_graph  "Swap          : "
# write_graph  "Shared        : "
# write_graph  "Buffers       : "
# write_graph  "Cached        : "

echo -e "\033[0;36mMemory info      Size(MB) Free(MB) Full %"
echo -en " Memory        : $r_c"
echo -n $[$MemTot / 1024] "     "
echo -n $[$MemFree / 1024] "        "
echo "$Memunused%"

echo -en "\033[0;36m Swap          : $r_c"
echo -n $[$SwapTot / 1024] "     "
echo -n $[$SwapFree / 1024] "      "
echo "  $Swapunused%"

#############################################################
# Piping "df" through a little awk-program that writes graphs
#############################################################

echo ""
echo -e "\033[0;36mMount Point      Usage                          Size(MB)  \033[1;32mFree(MB)  \033[1;31mFull %\033[0m" 


df | awk -v r="$r_c" -v w="$w_c" -v h="$h_c" -v f="$f_c" \
          -v u="$u_c" -v s="$s_c" -v lngth="$l" \
 \
 'BEGIN {getline;r_c=r;w_c=w;h_c=h;
         f_c=f;u_c=u;s_c=s;l=lngth;}
 {
 tot=$3*l/$2+1; 
 printf("%s%s%-14s%s", w_c, " ", $6, ": ");
 
 for (i=1; i<l+1; i++) {
  if ( i < tot ) { printf("%s%s", u_c, " ") }
  else { printf("%s%s", f_c, " ") }
  }
 print(w_c r_c" " $2 / 1024"   "r_c r_c$4 / 1024 r_c"   "($2 - $4) * 100 / $2"%");
 }
 END{printf(r_c)}'

echo ""





