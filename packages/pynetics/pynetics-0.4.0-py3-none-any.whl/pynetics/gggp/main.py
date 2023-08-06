from pprint import pprint

from pynetics.gggp import grammar

awesome_grammar = grammar.Grammar(
    start_symbol='frase',
    productions=[
        grammar.Production(
            'frase',
            grammar.And(
                grammar.Multiplier('sujeto', upper=1),
                'predicado',
                grammar.Multiplier(
                    grammar.And(
                        'conjuncion',
                        grammar.Multiplier('sujeto', upper=1),
                        'predicado'
                    ),
                )
            ),
        ),
        grammar.Production('conjuncion', grammar.Or(('y', 4), ('o', 6))),
        grammar.Production('sujeto', grammar.Or('sujeto_masc', 'sujeto_fem')),
        grammar.Production(
            'sujeto_masc',
            grammar.Or(
                grammar.And('el', 'nombre_comun_masc'),
                grammar.And(
                    grammar.Multiplier('el', upper=1),
                    'nombre_propio_masc'
                ),
            )
        ),
        grammar.Production(
            'sujeto_fem',
            grammar.Or(
                grammar.And('la', 'nombre_comun_fem'),
                grammar.And(
                    grammar.Multiplier('la', upper=1),
                    'nombre_propio_fem'
                ),
            )
        ),
        grammar.Production(
            'nombre_comun_masc',
            grammar.Or('chico', 'chatarrero', 'profesor', 'mutante', 'zombie'),
        ),
        grammar.Production(
            'nombre_propio_masc',
            grammar.Or('Pepe', 'Paco Pil', 'Richal'),
        ),
        grammar.Production(
            'nombre_comun_fem',
            grammar.Or('camionera', 'guitarrista', 'prestituta', 'tabernera'),
        ),
        grammar.Production(
            'nombre_propio_fem',
            grammar.Or('Juani', 'Pepi', 'Lili'),
        ),
        grammar.Production(
            'predicado',
            grammar.And('verbo', grammar.Multiplier('complemento', upper=1))
        ),
        grammar.Production(
            'verbo',
            grammar.Or(
                'corre',
                'habla',
                'ríe',
                'tiene',
                'va',
                'come',
                'dice',
                'canta',
                'caga',
                'mea',
                'micciona',
                'excreta',
                'evacúa',
            )
        ),
        grammar.Production(
            'complemento',
            grammar.Or(
                'la comida',
                'como puede',
                'que se las pela',
                'soy una rumbera',
                'abriendo puertas',
                'a las barricadas',
                'algo',
                'siempre',
                'a dos manos',
            )
        ),
    ]
)

pprint(' '.join(awesome_grammar.random_tree().word()))
