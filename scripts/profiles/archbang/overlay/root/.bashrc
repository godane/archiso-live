alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

# Use a dedicated file for bash aliases
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
