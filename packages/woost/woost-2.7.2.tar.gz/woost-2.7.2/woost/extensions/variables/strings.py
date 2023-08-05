#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

# Variable
#------------------------------------------------------------------------------
translations.define("Variable",
    ca = u"Variable",
    es = u"Variable",
    en = u"Variable"
)

translations.define("Variable-plural",
    ca = u"Variables",
    es = u"Variables",
    en = u"Variables"
)

translations.define("Variable.identifier",
    ca = u"Identificador",
    es = u"Identificador",
    en = u"Identifier"
)

translations.define("Variable.text",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define("Variable.translated_text",
    ca = u"Text traduït",
    es = u"Texto traducido",
    en = u"Translated text"
)

translations.define("Variable.dynamic_value",
    ca = u"Expressió",
    es = u"Expresión",
    en = u"Expression"
)

translations.define("Variable.expression-explanation",
    ca = u"""
        <p>
            Bloc de codi Python que permet produïr el valor de la variable
            programàticament.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                Si es deixa en blanc, el valor obtingut a partir dels camps
                <em>text</em> o <em>text traduït</em> es retorna sense
                modificar. Si s'emplena el camp, el codi tindrà accés a les
                variables següents:
            </p>
            <dl>
                <dt><code>self</code></dt>
                <dd>
                    Una referència a l'objecte <code>Variable</code>.
                </dd>
                <dt><code>text</code></dt>
                <dd>
                    El text que s'utilitzarà com a valor per la variable.
                    Inicialitzat al text que es retornaria normalment.
                </dd>
            </dl>
        </detalls>
        """,
    es = u"""
        <p>
            Bloque de código Python que permite producir el valor de la
            variable programáticamente.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                Si se deja en blanco, el valor obtenido a partir de los
                campos <em>texto</em> o <em>texto traducido</em> se devolverá
                sin modificar. Si se rellena este campo, el código tendrá
                acceso a las variables siguientes:
            </p>
            <dl>
                <dt><code>self</code></dt>
                <dd>
                    Una referencia a este objeto <code>Variable</code>.
                </dd>
                <dt><code>text</code></dt>
                <dd>
                    El texto que se utilitzará como valor para la variable.
                    Inicializado con el texto que se devolvería normalmente.
                </dd>
            </dl>
        </detalls>
        """,
    en = u"""
        <p>
            Python code block that makes it possible to change the value for
            this variable programmatically.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                If left blank, the variable's value is produced by evaluating
                the <em>text</em> and <em>translated text</em> fields. If given
                a value, the code block will have access to the following
                variables:
            </p>
            <dl>
                <dt><code>self</code></dt>
                <dd>
                    A reference to this <code>Variable</code> object.
                </dd>
                <dt><code>text</code></dt>
                <dd>
                    The text that will be produced by this variable.
                    Initialized to the text that would be produced if the
                    expression field was empty.
                </dd>
            </dl>
        </detalls>
        """
)

