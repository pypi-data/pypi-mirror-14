import nombramientos


class Lexer(nombramientos.Lexer):
    pass


class Parser(nombramientos.Parser):
    pass

if __name__ == "__main__":
    c = u"Consejero: RIBERA SALUD SA. Presidente: RIBERA SALUD SA. Consejero: RIBERA SALUD PROYECTOS SL;RIBERA SALUD INFRAESTRUCTURAS SL;RIBERA SALUD TECNOLOGIAS SL;TORREVIEJA SALUD SL;INSTITUTO DE GESTION SANITARIA SA;ENTORNO 2000 SA;TENEDORA DE PARTICIPACIONES TECNOLOGICAS SA;ARACIL GALLARDO JOSE;FERNANDEZ VIDAL FERNANDO MANUEL. SecreNoConsj: FERNANDEZ MARTINEZ MARIA."
    cese = c
    # m = Lexer()
    # m.build()
    # m.test(nombramiento)
    print Parser(cese).to_str()
