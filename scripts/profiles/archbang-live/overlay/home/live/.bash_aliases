# You can use this file to set your bash aliases.
# Many of the aliases here are taken from:
# http://ubuntuforums.org/showthread.php?t=204382

# enable color support of ls
if [ "$TERM" != "dumb" ]; then
    eval "`dircolors -b`"
    alias ls='ls --color=auto'
    alias dir='ls --color=auto --format=vertical'
    alias vdir='ls --color=auto --format=long'
fi

# work around for a common typo
alias cd..="cd .."

# make nano use the -w option by 'default'
alias nano="nano -w"

# Make these commands ask before clobbering a file. Use -F to override
#alias rm="rm -i"
#alias cp="cp -i"
#alias mv="mv -i"

# Use human-readable filesizes for 'du' and 'df'
alias du="du -h"
alias df="df -h"

# Display current date
alias today='date +"%A, %B %-d, %Y"'

# Make cal use Monday as first day of the week.
alias cal="cal -m"

alias bb="bauerbill"

alias update="sudo bauerbill -Syu"
