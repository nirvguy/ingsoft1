#
# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest

class Numero:
    DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO = 'No se puede dividir por 0'

    def esCero(self):
        self.shouldBeImplementedBySubclass()

    def esUno(self):
        self.shouldBeImplementedBySubclass()

    def __add__(self,sumando):
        self.shouldBeImplementedBySubclass()

    def __mul__(self,factor):
        self.shouldBeImplementedBySubclass()
    
    def __div__(self,divisor):
        self.shouldBeImplementedBySubclass()

    def shouldBeImplementedBySubclass(self):
        raise NotImplementedError('Should be implemented by the subclass')

class Entero(Numero):
    
    def __init__(self, numero):
        self._valor = numero

    def valor(self):
        return self._valor
    
    def esCero(self):
        return self._valor == 0

    def esUno(self):
        return self._valor == 1

    def __eq__(self,anObject):
        if isinstance(anObject, self.__class__):
            return self._valor==anObject._valor
        else: 
            return False
        
    def __add__(self,sumando):
        return Entero(self._valor+sumando.valor())
 
    def __mul__(self,factor):
        return Entero(self._valor*factor.valor())
         
    def __div__(self,divisor):
        return divisor.dividirEntero(self)
        
    def dividirEntero(self,dividendo):
        if self.esCero():
            raise Exception(Numero.DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO)
        if self.esUno():
            return dividendo
        
        maximoComunDivisor = self.maximoComunDivisorCon(dividendo)
        #No puedo usar / porque puedo caer en una recursion, por eso divido directamente
        #los valores porque se que son enteros
        numerador = dividendo.divisionEntera(maximoComunDivisor)
        denominador = self.divisionEntera(maximoComunDivisor)
        
        if denominador.esUno():
            return numerador
        
        return Fraccion(numerador,denominador)

    def divisionEntera(self,divisorEntero):
        return Entero (self._valor / divisorEntero.valor())
            
    def maximoComunDivisorCon(self,otroEntero):
        if otroEntero.esCero(): 
            return self
        else:
            return otroEntero.maximoComunDivisorCon(self.restoCon(otroEntero))
    
    def restoCon(self, divisor):
        return Entero (self._valor % divisor.valor());
        
    
class Fraccion(Numero):
    
    def __init__(self, numerador, denominador):
        self._numerador = numerador
        self._denominador = denominador

    def numerador(self):
        return self._numerador
    
    def denominador(self):
        return self._denominador
    
    def esCero(self):
        return False

    def esUno(self):
        return False

    def __eq__(self,anObject):
        if isinstance(anObject, self.__class__):
            return self._numerador*anObject.denominador()==self._denominador*anObject.numerador()
        else: 
            return False
        
    def __add__(self,sumando):
        nuevoDenominador = self._denominador * sumando.denominador()
        primerSumando = self._numerador * sumando.denominador()
        segundoSumando = self._denominador * sumando.numerador()
        nuevoNumerador = primerSumando + segundoSumando
        
        return nuevoNumerador / nuevoDenominador
  
    def __mul__(self,factor):
        return (self._numerador * factor.numerador()) / (self._denominador * factor.denominador())
            
    def __div__(self,divisor):
        return divisor.dividirFraccion(self)
    
    def dividirFraccion(self,dividendo):
        return (dividendo.numerador() * self._denominador) / (dividendo.denominador () * self._numerador)

class NumeroTest(unittest.TestCase):

    def createCero(self):
        return Entero(0)
    
    def createUno(self):
        return Entero(1)
    
    def createDos(self):
        return Entero(2)
    
    def createTres(self):
        return Entero(3)
    
    def createCuatro(self):
        return Entero(4)
    
    def createCinco(self):
        return Entero(5)
    
    def createUnQuinto(self):
        return self.uno / self.cinco
    
    def createDosQuintos(self):
        return self.dos / self.cinco
    
    def createTresQuintos(self):
        return self.tres / self.cinco
    
    def createDosVeinticincoavos(self):
        return self.dos / Entero(25)
    
    def createUnMedio(self):
        return self.uno / self.dos
    
    def createCincoMedios(self):
        return self.cinco / self.dos
    
    def createSeisQuintos(self):
        return Entero(6) / self.cinco
    
    def createCuatroMedios(self):
        return self.cuatro / self.dos
    
    def createDosCuartos(self):
        return self.dos / self.cuatro

    def setUp(self):
        self.cero = self.createCero()
        self.uno = self.createUno()
        self.dos = self.createDos()
        self.tres = self.createTres()
        self.cuatro = self.createCuatro()
        self.cinco = self.createCinco()
        self.unQuinto = self.createUnQuinto()
        self.dosQuintos = self.createDosQuintos()
        self.tresQuintos = self.createTresQuintos()
        self.dosVeinticincoavos = self.createDosVeinticincoavos()
        self.unMedio = self.createUnMedio()
        self.cincoMedios = self.createCincoMedios()
        self.seisQuintos = self.createSeisQuintos()
        self.cuatroMedios = self.createCuatroMedios()
        self.dosCuartos = self.createDosCuartos()
             
    def test01EsCeroDevuelveTrueSoloParaElCero(self):
        self.assertTrue (self.cero.esCero())
        self.assertFalse (self.uno.esCero())

    def test02EsUnoDevuelveTrueSoloParaElUno(self):
        self.assertTrue (self.uno.esUno())
        self.assertFalse (self.cero.esUno())

    def test03SumaDeEnteros(self):
        self.assertEqual (self.dos,self.uno+self.uno)
    
    def test04MultiplicacionDeEnteros(self):
        self.assertEqual(self.cuatro, self.dos*self.dos)

    def test05DivisionDeEnteros(self):
        self.assertEqual(self.uno, self.dos/self.dos)
    
    def test06SumaDeFracciones(self):
        sieteDecimos = Entero(7) / Entero (10) # <- REEMPLAZAR POR LO QUE CORRESPONDA;
        self.assertEqual (sieteDecimos,self.unQuinto+self.unMedio)
        # 
        # La suma de fracciones es:
        # 
        # a/b + c/d = (a.d + c.b) / (b.d)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # NO SE ESTA TESTEANDO ESE CASO
        #

    def test07MultiplicacionDeFracciones(self):
        self.assertEqual (self.dosVeinticincoavos,self.unQuinto*self.dosQuintos)
        # 
        # La multiplicacion de fracciones es:
        # 
        # (a/b) * (c/d) = (a.c) / (b.d)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # TODAVIA NO SE ESTA TESTEANDO ESE CASO
        #
    
    def test08DivisionDeFracciones(self):
        self.assertEqual (self.cincoMedios,self.unMedio/self.unQuinto)
        # 
        # La division de fracciones es:
        # 
        # (a/b) / (c/d) = (a.d) / (b.c)
        # 
        # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
        # TODAVIA NO SE ESTA TESTEANDO ESE CASO
        #

    # 
    # Ahora empieza lo lindo! - Primero hacemos que se puedan sumar enteros con fracciones
    # y fracciones con enteros 
    #
    def test09SumaDeEnteroYFraccion(self):
        self.assertEqual (self.seisQuintos,self.uno+self.unQuinto)
    
    def test10SumaDeFraccionYEntero(self):
        self.assertEqual (self.seisQuintos,self.unQuinto+self.uno)

    # 
    # Hacemos lo mismo para la multipliacion
    #
    def test11MultiplicacionDeEnteroPorFraccion(self):
        self.assertEqual(self.dosQuintos,self.dos*self.unQuinto)
    
    def test12MultiplicacionDeFraccionPorEntero(self):
        self.assertEqual(self.dosQuintos,self.unQuinto*self.dos)
    
    # 
    # Hacemos lo mismo para la division
    #
    def test13DivisionDeEnteroPorFraccion(self):
        self.assertEqual(self.cincoMedios,self.uno/self.dosQuintos)
    
    def test14DivisionDeFraccionPorEntero(self):
        self.assertEqual(self.dosVeinticincoavos,self.dosQuintos/self.cinco)
    
    # 
    # Ahora si empezamos con problemas de reduccion de fracciones
    #
    def test15UnaFraccionPuedeSerIgualAUnEntero(self):
        self.assertEquals(self.dos,self.cuatroMedios)

    def test16LasFraccionesAparentesSonIguales(self):
        self.assertEquals(self.unMedio,self.dosCuartos)
        #
        # Las fracciones se reducen utilizando el maximo comun divisor (mcd)
        # Por lo tanto, para a/b, sea c = mcd (a,b) => a/b reducida es:
        # (a/c) / (b/c).
        # 
        # Por ejemplo: a/b = 2/4 entonces c = 2. Por lo tanto 2/4 reducida es:
        # (2/2) / (4/2) = 1/2
        # 
        # Para obtener el mcd pueden usar el algoritmo de Euclides que es:
        # 
        # mcd (a,b) = 
        #         si b = 0 --> a
        #         si b != 0 -->mcd(b, restoDeDividir(a,b))
        #     
        # Ejemplo:
        # mcd(2,4) ->
        # mcd(4,restoDeDividir(2,4)) ->
        # mcd(4,2) ->
        # mcd(2,restoDeDividir(4,2)) ->
        # mcd(2,0) ->
        # 2
        #
    
    def test17LaSumaDeFraccionesPuedeDarEntero(self):
        self.assertEquals (self.uno,self.unMedio+self.unMedio)

    def test18LaMultiplicacionDeFraccionesPuedeDarEntero(self):
        self.assertEquals(self.dos,self.cuatro*self.unMedio)

    def test19LaDivisionDeEnterosPuedeDarFraccion(self):
        self.assertEquals(self.unMedio, self.dos/self.cuatro)

    def test20LaDivisionDeFraccionesPuedeDarEntero(self):
        self.assertEquals(self.uno, self.unMedio/self.unMedio)
    
    def test21NoSePuedeDividirEnteroPorCero(self):
        try:
            self.uno/self.cero
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    def test22NoSePuedeDividirFraccionPorCero(self):
        try:
            self.unQuinto/self.cero
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    # Este test puede ser redundante dependiendo de la implementacion realizada 
    def test23NoSePuedeCrearFraccionConDenominadorCero(self):
        try:
            self.crearFraccionCon(self.uno,self.cero)
            self.fail()
        except Exception as e:
            self.assertEquals(self.descripcionDeErrorDeNoSePuedeDividirPorCero(),e.message)

    def crearFraccionCon(self, numerador, denominador): 
        return numerador/denominador
    
    def descripcionDeErrorDeNoSePuedeDividirPorCero(self):
        #Tratar de que la implementacion de este metodo utilice el mensaje definido en alguna de las clase de numero
        return Numero.DESCRIPCION_DE_ERROR_DE_DIVISION_POR_CERO
    
if __name__ == "__main__":
    unittest.main()
    