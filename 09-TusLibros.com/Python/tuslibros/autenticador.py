class Autenticador(object):
    COMBINACION_USUARIO_Y_CLAVE_INVALIDA = 'El usuario o la clave son invalidos!'

    def __init__(self, usuarios):
        self._usuarios = usuarios

    def login(self, usuario, contrasenia):
        if usuario not in self._usuarios or self._usuarios[usuario] != contrasenia:
            raise Exception(self.COMBINACION_USUARIO_Y_CLAVE_INVALIDA)
