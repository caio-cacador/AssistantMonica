
COMPLIMENT = ('linda', 'gostosa', 'delicia', 'inteligente', 'esperta', 'foda')
COMPLIMENT_RESPONSE = ('Obrigada', 'São seus olhos!', 'Eu sei')

NORMAL_GREETING = ('oi', 'ola')

INFORMAL_GREETING = ('eai', 'e ai', 'e ae', 'fala ai', 'suave')

GREETING_WITH_QUESTION = ('tudo bem', 'como vc vai', 'como vc esta')

CONVERSATION_INTERPRETER = (NORMAL_GREETING + INFORMAL_GREETING + GREETING_WITH_QUESTION)


WHAT_IS_INTERPRETER = ('o que é', 'o q e', 'oq e', 'o que eh', 'o q eh', 'oque e')

WHO_IS_INTERPRETER = ('quem é', 'quem eh')

MONICA_FILTER = ['monica']

LINK_FILTER = ('www.buscape', 'www.fastshop', 'www.zoom', 'www.magazineluiza', 'www.xvideos', 'www.porhub')

TAG_FILTER = "<p style.*?>|<img.*?>|<p class=.*?>|<a href.*?>|</strong>|<strong>|<a class=.*?>|" + \
             "<sup class.*?>|<span>\[.*?\]</span>|<sup.?>|" + \
             "</i>|</sub>|<sub>|<span.*?</span>|<small>|</small>|\\xa0|<\/span>\)<\/span>|" + \
             "<\/span>\(<\/span>|<em>.*?</em>"

TAG_FILTER_FASE_2 = "<p>|<b>|</b>|<br>|</br>|<br/>|<a>|</a>|</sup>|</p>|<i>|</span>|<span>"

OPEN_DOOR = ['abra a porta', 'destranque a porta']
LOCK_DOOR = ['feche a porta', 'tranque a porta']
GET_BEDROOM_IMAGE = ['mostre meu quarto', 'mostre o meu quarto', 'mande a foto do quarto', 'mande a foto do meu quarto']

PERMISSION_DENIED_TO_EXECUTE_COMMAND = 'Você não tem permissão para dar esse comando! você é um merda.'

RESTART = ['reinicie', 'morra']