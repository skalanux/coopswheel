from enum import Enum


questions_equivs = {
    'Tecnología': 'TECNOLOGIA', 
    'Cooperativismo': 'COOPS', 
    'Argentina': 'ARGENTINA', 
    'Python': 'PYTHON', 
    'Rosario': 'ROSARIO', 
    'Latinoamérica': 'LATINOAMERICA'}

LABELS = list(questions_equivs.keys())

class Questions(Enum):
    COOPS = [
        ("¿El cooperativismo argentino tiene sus raíces en el siglo XIX?", True),
        ("¿Las cooperativas en Argentina pueden operar en cualquier sector económico?", True),
        ("¿Es obligatorio que una cooperativa argentina distribuya todos sus excedentes entre sus miembros?", False),
        ("¿Pueden las cooperativas argentinas recibir beneficios fiscales?", True),
        ("¿La membresía en una cooperativa argentina es limitada a un número fijo de personas?", False),
        ("¿Es necesario que todas las cooperativas en Argentina tengan un Consejo de Administración?", True),
        ("¿El INAES (Instituto Nacional de Asociativismo y Economía Social) es el organismo que regula las cooperativas en Argentina?", True),
        ("¿Una cooperativa argentina puede ser transformada en una sociedad anónima?", False),
        ("¿Las cooperativas argentinas tienen que cumplir con la Ley de Cooperativas N° 20.337?", True),
        ("¿Es obligatorio que los miembros de una cooperativa argentina tengan igualdad de votos, independientemente del capital aportado?", True)
    ]
    TECNOLOGIA = [
        ("¿HTML es un lenguaje de programación?", False),
        ("¿El sistema operativo Linux es de código abierto?", True),
        ("¿Un terabyte es mayor que un gigabyte?", True),
        ("¿El protocolo HTTPS es más seguro que HTTP?", True),
        ("¿JavaScript y Java son el mismo lenguaje de programación?", False),
        ("¿El almacenamiento en la nube se refiere a guardar datos en servidores remotos accesibles por Internet?", True),
        ("¿La inteligencia artificial y el aprendizaje automático son lo mismo?", False),
        ("¿El navegador web Google Chrome fue lanzado antes que Mozilla Firefox?", False),
        ("¿El cifrado de datos se usa para proteger la información de accesos no autorizados?", True),
        ("¿La tecnología blockchain se utiliza principalmente en las criptomonedas?", True)
    ]
    PYTHON = [
        ("¿Python es un lenguaje de programación de alto nivel?", True),
        ("¿Python fue creado por Guido van Rossum?", True),
        ("¿Python es un lenguaje de programación compilado?", False),
        ("¿La sintaxis de Python permite el uso de corchetes para delimitar bloques de código?", False),
        ("¿Python soporta programación orientada a objetos?", True),
        ("¿Python es conocido por su simplicidad y legibilidad?", True),
        ("¿Python tiene un gestor de paquetes llamado pip?", True),
        ("¿La extensión de archivo estándar para scripts de Python es .py?", True),
        ("¿Python 2 y Python 3 son completamente compatibles entre sí?", False),
        ("¿Las listas en Python son mutables?", True)
    ]
    ARGENTINA = [
        ("¿Buenos Aires es la capital de Argentina?", True),
        ("¿El tango es un género musical originario de Argentina?", True),
        ("¿El Aconcagua es la montaña más alta de América del Sur?", True),
        ("¿Argentina ganó su primera Copa del Mundo de fútbol en 1986?", False),
        ("¿La moneda oficial de Argentina es el peso argentino?", True),
        ("¿El escritor Jorge Luis Borges nació en Argentina?", True),
        ("¿La Patagonia se encuentra en el norte de Argentina?", False),
        ("¿El mate es una bebida tradicional en Argentina?", True),
        ("¿Argentina es el segundo país más grande de América del Sur?", True),
        ("¿Mar del Plata es una ciudad costera en Argentina?", True)
    ]
    ROSARIO = [
        ("¿Rosario es una ciudad en la provincia de Santa Fe, Argentina?", True),
        ("¿El Monumento a la Bandera se encuentra en Rosario?", True),
        ("¿Rosario es la ciudad natal de Lionel Messi?", True),
        ("¿El río Paraná pasa por Rosario?", True),
        ("¿Rosario es la capital de la provincia de Santa Fe?", False),
        ("¿Rosario es conocida por su importante puerto comercial?", True),
        ("¿Rosario tiene uno de los parques más grandes de Argentina, el Parque Independencia?", True),
        ("¿La Universidad Nacional de Rosario es una de las principales universidades de la ciudad?", True),
        ("¿Rosario está ubicada en la región noroeste de Argentina?", False),
        ("¿El Che Guevara nació en Rosario?", True)
    ]
    LATINOAMERICA = [
        ("¿Brasil es el país más grande de Latinoamérica?", True),
        ("¿El idioma oficial de la mayoría de los países en Latinoamérica es el español?", True),
        ("¿El Amazonas es el río más largo de Latinoamérica?", True),
        ("¿El Machu Picchu se encuentra en México?", False),
        ("¿El Carnaval de Río de Janeiro es una de las fiestas más grandes de Latinoamérica?", True),
        ("¿Latinoamérica incluye países de América Central y del Sur?", True),
        ("¿El desierto de Atacama se encuentra en Perú?", False),
        ("¿México es parte de Latinoamérica?", True),
        ("¿La Patagonia se extiende por Chile y Argentina?", True),
        ("¿La mayoría de los países en Latinoamérica se independizaron en el siglo XIX?", True)
    ]
