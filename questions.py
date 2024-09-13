from enum import Enum


questions_equivs = {
    'Tecnología': 'TECNOLOGIA', 
    'Cooperativismo': 'COOPS', 
    'Argentina': 'ARGENTINA', 
    'Python': 'PYTHON', 
    'Hurlingham': 'HURLINGHAM', 
    'Programación': 'PROGRAMACION'}

LABELS = list(questions_equivs.keys())

class Questions(Enum):
    COOPS = [
        ("¿El cooperativismo argentino tiene sus raíces en el siglo XIX?", True),
        ("¿Las cooperativas en Argentina pueden operar en cualquier sector económico?", True),
        ("¿Es obligatorio que una cooperativa argentina distribuya todos sus excedentes entre sus miembros?", False),
        ("¿Pueden las cooperativas argentinas recibir beneficios fiscales?", True),
        ("¿La membresía en una cooperativa argentina es limitada a un número fijo de personas?", False),
        ("¿Es necesario que todas las cooperativas en Argentina tengan un Consejo de Administración?", True),
        ("¿El INAES es el organismo que regula las cooperativas en Argentina?", True),
        ("¿Una cooperativa argentina puede ser transformada en una sociedad anónima?", False),
        ("¿Las cooperativas argentinas tienen que cumplir con la Ley de Cooperativas N° 20.337?", True),
        ("¿Es obligatorio que los miembros de una cooperativa tengan igualdad de votos?", True),
        ("Existe una cooperativa en Australia que fabrica colchones para canguros", False),
        ("En Japón, hay cooperativas que ofrecen alquiler de amigos para actividades sociales y eventos ", True),
        ("Existe una cooperativa en Francia que produce perfume de lavanda para sus miembros.", False),
        ("En Italia, hay una cooperativa que restaura y alquila castillos", True),
        ("En Argentina existe una cooperativa de artistas callejeros", True),
        ("En Argentina existe una cooperativa que exporta miel a más de 20 países.", True),
        ("Las cooperativas se pueden organizar en federaciones y confederaciones.", True)
    ]
    TECNOLOGIA = [
        ("¿HTML es un lenguaje de programación?", False),
        ("¿El sistema operativo Linux es de código abierto?", True),
        ("¿Un terabyte es mayor que un gigabyte?", True),
        ("¿El protocolo HTTPS es más seguro que HTTP?", True),
        ("¿JavaScript y Java son el mismo lenguaje de programación?", False),
        ("¿Almacenar en la nube se refiere a guardar datos en servidores accesibles por Internet?", True),
        ("¿La inteligencia artificial y el aprendizaje automático son lo mismo?", False),
        ("¿El navegador web Google Chrome fue lanzado antes que Mozilla Firefox?", False),
        ("¿El cifrado de datos se usa para proteger la información de accesos no autorizados?", True),
        ("¿La tecnología blockchain se utiliza principalmente en las criptomonedas?", True),
        ("El nombre de la mascota de Linux es Tux", True),
        ("La mascota de Linux es un perro", False)
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
    ("¿Las listas en Python son mutables?", True),
    ("¿Los diccionarios en Python permiten claves duplicadas?", False),
    ("¿Python soporta múltiples herencias?", True),
    ("¿El operador '+' puede ser usado para concatenar cadenas en Python?", True),
    ("¿Las tuplas en Python son mutables?", False),
    ("¿Python tiene recolección automática de basura (garbage collection)?", True),
    ("¿El módulo 'os' permite interactuar con el sistema operativo?", True),
    ("¿Python puede ser usado para desarrollo web?", True),
    ("¿'None' es equivalente a 'False' en Python?", False),
    ("¿El método 'append()' agrega elementos al final de una lista?", True),
    ("¿Python tiene tipos de datos estáticos?", False),
    ("¿El ciclo 'while' en Python necesita una condición booleana?", True),
    ("¿Las funciones lambda pueden tener múltiples expresiones?", False),
    ("¿El operador '==' compara la identidad de los objetos en Python?", False),
    ("¿Se puede definir una función dentro de otra función en Python?", True),
    ("¿El método 'clear()' borra el contenido de una lista?", True),
    ("¿El operador '**' se usa para la exponenciación en Python?", True),
    ("¿El módulo 'math' en Python incluye funciones trigonométricas?", True),
    ("¿Una variable en Python necesita ser declarada con un tipo específico?", False),
    ("¿El statement 'global' permite modificar variables globales dentro de funciones?", True),
    ("¿El tipo 'int' en Python tiene un límite máximo?", False),
    ("¿Python es adecuado para scripting y automatización?", True),
    ("¿Las clases en Python pueden tener métodos estáticos?", True),
    ("¿El operador '//' realiza una división entera en Python?", True),
    ("¿Python tiene una palabra clave llamada 'switch'?", False),
    ("¿Se puede manejar excepciones en Python usando 'try-except'?", True),
    ("¿El método 'pop()' elimina el primer elemento de una lista?", False),
    ("¿El módulo 'json' en Python permite trabajar con JSON?", True),
    ("¿Python es un lenguaje case-sensitive?", True),
    ("¿El statement 'pass' se usa para definir un bloque vacío en Python?", True),
    ("¿El operador 'is' compara la identidad de los objetos?", True),
    ("¿Las listas en Python pueden contener diferentes tipos de datos?", True),
    ("¿La palabra clave 'del' elimina una variable en Python?", True),
    ("¿Python tiene soporte para el concepto de 'closures'?", True),
    ("¿El método 'sort()' modifica la lista original?", True),
    ("¿El ciclo 'for' en Python necesita un contador manual?", False),
    ("¿Se puede definir propiedades en las clases usando 'property()'?", True),
    ("¿Python permite el uso de 'decorators' para modificar el comportamiento de funciones?", True),
    ("¿El método 'remove()' elimina un elemento de una lista por su índice?", False),
    ("¿El statement 'yield' en Python convierte una función en un generador?", True)
    ]

    ARGENTINA = [
        ("¿El Aconcagua es la montaña más alta de América del Sur?", True),
        ("¿Argentina ganó su primera Copa del Mundo de fútbol en 1986?", False),
        ("¿La moneda oficial de Argentina es el peso argentino?", True),
        ("¿El escritor Jorge Luis Borges nació en Argentina?", True),
        ("¿La Patagonia se encuentra en el norte de Argentina?", False),
        ("¿El mate es una bebida tradicional en Argentina?", True),
        ("¿Argentina es el segundo país más grande de América del Sur?", True),
        ("¿Mar del Plata es una ciudad costera en Argentina?", True),
        ("¿Messi y Gardel cumplen el mismo día?", True),
        ("Argentina tiene un museo dedicado enteramente al dulce de leche ", True),
        ("En Argentina existe una isla habitada en su mayoría por conejos ", True),
        ("La Avenida 9 de Julio en Buenos Aires es la avenida más larga del mundo", False),
        ("Argentina es el segundo mayor productor de vino de sudamérica ", False)

    ]
    ROSARIO = [
        ("¿Rosario es la ciudad natal de Lionel Messi?", True),
        ("¿El río Paraná pasa por Rosario?", True),
        ("¿Rosario es la capital de la provincia de Santa Fe?", False),
        ("¿Rosario es conocida por su importante puerto comercial?", True),
        ("¿Rosario tiene uno de los parques más grandes de Argentina, el Parque Independencia?", True),
        ("¿La Universidad Nacional de Rosario es una de las principales universidades de la ciudad?", True),
        ("¿Rosario está ubicada en la región noroeste de Argentina?", False),
        ("¿El Che Guevara nació en Rosario?", True),
        ("Messi tiene 8 balones de oro", True),
        ("Rosario es famosa por sus murales callejeros, que cuentan con más de 500 obras de arte urbano", True),
        ("En Rosario se celebra anualmente el Festival Internacional de las Esculturas de Arena", False),
        ("Rosario es conocida por tener la mayor cantidad de heladerías por habitante en Argentina", False),
        ("Rosario es considerada la capital del fútbol femenino", True),
        ("Rosario siempre estuvo cerca", True)
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
        ("¿La mayoría de los países en Latinoamérica se independizaron en el siglo XIX?", True),
        ("El Machu Picchu, en Perú, es una de las Siete Maravillas del Mundo Moderno", True),
        ("Las Islas Galápagos, en Ecuador, inspiraron la teoría de la evolución de Charles Darwin", True),
        ("En Bolivia, el Salar Uyuni es tan plano y extenso que se utiliza para calibrar satélites como espejo natural", True)
    ]
