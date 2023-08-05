

append(){
    grep -q -F '$1' $2 || echo '$1' >> $2
}

log(){
    printf "$(tput setaf 0)log: $@ [$0] $(tput sgr0)\n"
}

call(){
    printf "$(tput setaf 2)Call: $@ [$0] $(tput sgr0)\n"
    $@
}

getcwd(){
    echo "$( cd "$( dirname "${0}" )" && pwd )"
}
