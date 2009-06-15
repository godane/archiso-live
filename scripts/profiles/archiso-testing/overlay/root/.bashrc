#export PS1="\u@\H > "

# Custom prompt
export PS1="\[\e[31;1m\]\u\[\e[30;1m\]@\[\e[37;1m\]\H \[\e[37;1m\]\W $ \[\e[0m\]"

# Use a dedicated file for bash aliases
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
