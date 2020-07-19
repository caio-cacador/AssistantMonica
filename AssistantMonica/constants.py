
COMPLIMENT = ('linda', 'gostosa', 'delicia', 'inteligente', 'esperta', 'foda')
COMPLIMENT_RESPONSE = ('Obrigada', 'São seus olhos!', 'Eu sei')

NORMAL_GREETING = ('oi', 'ola')

INFORMAL_GREETING = ('eai', 'e ai', 'e ae', 'fala ai', 'suave')

GREETING_WITH_QUESTION = ('tudo bem', 'td bem', 'como vc vai', 'como vc esta')

CONVERSATION_INTERPRETER = (NORMAL_GREETING + INFORMAL_GREETING + GREETING_WITH_QUESTION)


WHAT_IS_INTERPRETER = ('o que e', 'o q e', 'oq e', 'o que eh', 'o q eh', 'oque e')

WHO_IS_INTERPRETER = ('quem e', 'quem e', 'quem eh')

MONICA_FILTER = ('monica')

LINK_FILTER = ('www.buscape', 'www.fastshop', 'www.zoom', 'www.magazineluiza', 'www.xvideos', 'www.porhub')

TAG_FILTER = "<p style.*?>|<img.*?>|<p class=.*?>|<a href.*?>|</strong>|<strong>|<a class=.*?>|" + \
             "<sup class.*?>|<span>\[.*?\]</span>|<sup.?>|<p>|<b>|</b>|<br>|</br>|<br/>|<a>|</a>|</sup>|</p>|<i>|" + \
             "</i>|</sub>|<sub>|<span.?span></span>|<span.?</span>|<small>|</small>|\\xa0|<\/span>\)<\/span>|" + \
             "<\/span>\(<\/span>|"
