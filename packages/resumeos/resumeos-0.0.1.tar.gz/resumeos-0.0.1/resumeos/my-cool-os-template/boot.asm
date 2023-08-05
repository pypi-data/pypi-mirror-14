global start

section .text
bits 32
start:
    {% for ins in instructions_list %}
    {{ins}}
    {% endfor%}
    hlt
