class Tarjeta:
    MES_INVALIDO = 'Mes de expiracion invalido!'
    NRO_INVALIDO = 'Numero de tarjeta invalido!'
    DUENIO_VACIO = 'Nombre de duenio en blanco!'

    def __init__(self, numero, mes_expiracion, anio_expiracion, duenio):
        if len(str(numero)) != 16:
            raise Exception(Tarjeta.NRO_INVALIDO)

        if len(duenio) == 0:
            raise Exception(Tarjeta.DUENIO_VACIO)

        if mes_expiracion == 0 or mes_expiracion > 12:
            raise Exception(Tarjeta.MES_INVALIDO)

        self._numero = numero
        self._mes_expiracion = mes_expiracion
        self._anio_expiracion = anio_expiracion
        self._duenio = duenio

    def duenio(self):
        return self._duenio

    def mes_expiracion(self):
        return self._mes_expiracion

    def anio_expiracion(self):
        return self._anio_expiracion

    def numero(self):
        return self._numero

    def expiro(self, fecha):
        if fecha.year != self._anio_expiracion:
            return fecha.year > self._anio_expiracion
        else:
            return fecha.month > self._mes_expiracion
