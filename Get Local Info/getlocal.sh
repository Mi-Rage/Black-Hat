#!/bin/bash -
#
# getlocal.sh
#
# Description:
# Collect basic information about the system and dump it into a file.
#
# Usage:
# bash getlocal.sh < cmds.txt
# cmds.txt — is a file with a list of commands to execute
#
# SepCmds - separating commands from the input line.

function SepCmds()
{
 LCMD=${ALINE%%|*}   # Take everything from the cmd string to the symbol '|'. It`s a Linux commamd.
 REST=${ALINE#*|}    # Get the rest of the string from the '|' character and further
 WCMD=${REST%%|*}    # Take everything from the cmd string to the symbol '|'. It`s a Win commamd.
 REST=${REST#*|}     # Get the rest of the string from the '|' character and further
 TAG=${REST%%|*}     # Take everything from the cmd string to the symbol '|'. It`s a Tag.
 if [[ $OSTYPE == "MSWin" ]]
 then
 CMD="$WCMD"
 else
 CMD="$LCMD"
 fi
}

function DumpInfo ()
{ 
 printf '<systeminfo host="%s" type="%s"' "$HOSTNAME" "$OSTYPE"
 printf ' date="%s" time="%s">\n' "$(date '+%F')" "$(date '+%T')"
 readarray CMDS      # Read all input lines (up to the end of the file being read or by pressing Ctrl+D) into the CMDS array
 for ALINE in "${CMDS[@]}"
 do
 # Ignoring comments lines
 if [[ ${ALINE:0:1} == '#' ]] ; then continue ; fi
 SepCmds
 if [[ ${CMD:0:3} == N/A ]]
 then
 continue
 else
 printf "<%s>\n" $TAG
 echo "Executing $CMD" 
 $CMD
 printf "</%s>\n" $TAG
 fi
 done
 printf "</systeminfo>\n"
}

function OsDetect ()
{
    if type -t wevtutil &> /dev/null
    then
     OSTYPE=MSWin
    elif type -t scutil &> /dev/null
    then
     OSTYPE=macOS
    else
     OSTYPE=Linux
    fi
}

OsDetect
HOSTNM=$(hostname)
TMPFILE="${HOSTNM}.info"
# Collect both information and errors in the tmp file
DumpInfo > $TMPFILE 2>&1