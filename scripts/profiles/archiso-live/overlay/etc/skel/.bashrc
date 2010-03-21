alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '
#cat ~/.logo
#echo
#cal
#set show-all-if-ambiguous on

# Use a dedicated file for bash aliases
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
