#
# Developed by 10Pines SRL
# License:
# This work is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.
#

class ElevatorEmergency(Exception):
    pass

class CabinDoorState:

    def accept(self,aVisitor):
        self.shouldBeImplementedBySubclass()

    def isOpened(self):
        self.shouldBeImplementedBySubclass()

    def isOpening(self):
        self.shouldBeImplementedBySubclass()

    def isClosing(self):
        self.shouldBeImplementedBySubclass()

    def isClosed(self):
        self.shouldBeImplementedBySubclass()

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        self.shouldBeImplementedBySubclass()

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        self.shouldBeImplementedBySubclass()

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        self.shouldBeImplementedBySubclass()

    def shouldBeImplementedBySubclass(self):
        raise RuntimeError("Should be implemented by subclass")

class CabinDoorClosingState(CabinDoorState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinDoorClosingState(self)

    def isOpened(self):
        return False

    def isOpening(self):
        return False

    def isClosing(self):
        return True

    def isClosed(self):
        return False

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        self.elevatorController.cabinDoorClosedWhenWorkingAndCabinStoppedAndClosing()

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        self.elevatorController.openCabinDoorWhenWorkingAndCabinStoppedAndDoorClosing()

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

class CabinDoorOpenedState(CabinDoorState):

    def __init__(self, elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinDoorOpenedState(self)

    def isOpened(self):
        return True

    def isOpening(self):
        return False

    def isClosing(self):
        return False

    def isClosed(self):
        return False

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

class CabinDoorClosedState(CabinDoorState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinDoorClosedState(self)

    def isOpened(self):
        return False

    def isOpening(self):
        return False

    def isClosing(self):
        return False

    def isClosed(self):
        return True

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        raise NotImplementedError()

class CabinDoorOpeningState(CabinDoorState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinDoorOpeningState(self)

    def isOpened(self):
        return False

    def isOpening(self):
        return True

    def isClosing(self):
        return False

    def isClosed(self):
        return False

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        self.elevatorController.cabinDoorClosedWhenWorkingAndCabinStoppedAndCabinDoorOpening();

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        self.elevatorController.openCabinDoorWhenWorkingAndCabinStoppedAndCabinDoorOpening();

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        self.elevatorController.closeCabinDoorWhenWorkingAndCabinStoppedAndCabinDoorOpening();

class CabinState:

    def accept(self,aVisitor):
        self.shouldBeImplementedBySubclass()

    def cabinDoorClosedWhenWorking(self):
        self.shouldBeImplementedBySubclass()

    def isMoving(self):
        self.shouldBeImplementedBySubclass()

    def isStopped(self):
        self.shouldBeImplementedBySubclass()

    def cabinDoorOpenedWhenWorking(self):
        self.shouldBeImplementedBySubclass()

    def openCabinDoorWhenWorking(self):
        self.shouldBeImplementedBySubclass()

    def isWaitingForPeople(self):
        self.shouldBeImplementedBySubclass()

    def closeCabinDoorWhenWorking(self):
        self.shouldBeImplementedBySubclass()

    def waitForPeopleTimedOutWhenWorking(self):
        self.shouldBeImplementedBySubclass()

    def shouldBeImplementedBySubclass(self):
        raise RuntimeError("Should be implemented by subclass")

class CabinStoppedState(CabinState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinStoppedState(self)

    def cabinDoorClosedWhenWorking(self):
        self.elevatorController.cabinDoorClosedWhenWorkingAndCabinStopped();

    def isMoving(self):
        return False

    def isStopped(self):
        return True

    def cabinDoorOpenedWhenWorking(self):
        self.elevatorController.cabinDoorOpenedWhenWorkingAndCabinStopped()

    def openCabinDoorWhenWorking(self):
        self.elevatorController.openCabinDoorWhenWorkingAndCabinStopped()

    def isWaitingForPeople(self):
        return False

    def closeCabinDoorWhenWorking(self):
        self.elevatorController.closeCabinDoorWhenWorkingAndCabinStopped()

    def waitForPeopleTimedOutWhenWorking(self):
        raise NotImplementedError()


class CabinMovingState(CabinState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinMovingState(self)

    def cabinDoorClosedWhenWorking(self):
        self.elevatorController.cabinDoorClosedWhenWorkingAndCabinMoving()

    def isMoving(self):
        return True

    def isStopped(self):
        return False

    def cabinDoorOpenedWhenWorking(self):
        raise NotImplementedError()

    def openCabinDoorWhenWorking(self):
        self.elevatorController.openCabinDoorWhenWorkingAndCabinMoving()

    def isWaitingForPeople(self):
        return False

    def closeCabinDoorWhenWorking(self):
        self.elevatorController.closeCabinDoorWhenWorkingAndCabinMoving()

    def waitForPeopleTimedOutWhenWorking(self):
        raise NotImplementedError()

class CabinWaitingForPeopleState(CabinState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController

    def accept(self,aVisitor):
        return aVisitor.visitCabinWaitingForPeopleState(self)

    def cabinDoorClosedWhenWorking(self):
        raise NotImplementedError()

    def isMoving(self):
        raise NotImplementedError()

    def isStopped(self):
        return False

    def cabinDoorOpenedWhenWorking(self):
        raise NotImplementedError()

    def openCabinDoorWhenWorking(self):
        raise NotImplementedError()

    def isWaitingForPeople(self):
        return True

    def closeCabinDoorWhenWorking(self):
        self.elevatorController.closeCabinDoorWhenWorkingAndCabinWaitingForPeople();

    def waitForPeopleTimedOutWhenWorking(self):
        self.elevatorController.waitForPeopleTimedOutWhenWorkingAndCabinWaitingForPeople();

class ElevatorControllerState:

    def isIdle(self):
        raise "Should be implemented by subclass"

    def goUpPushedFromFloor(self, aFloorNumber):
        raise "Should be implemented by subclass"

    def isWorking(self):
        raise "Should be implemented by subclass"

    def cabindDoorClosed(self):
        raise "Should be implemented by subclass"

    def cabinOnFloor(self,aFloorNumber):
        raise "Should be implemented by subclass"

    def cabinDoorOpened(self):
        raise "Should be implemented by subclass"

    def openCabinDoor(self):
        raise "Should be implemented by subclass"

    def waitForPeopleTimedOut(self):
        raise "Should be implemented by subclass"

    def closeCabinDoor(self):
        raise "Should be implemented by subclass"

class ElevatorControllerIdleState(ElevatorControllerState):

    def __init__(self, elevatorController):
        self.elevatorController = elevatorController

    def isIdle(self):
        return True

    def goUpPushedFromFloor(self, aFloorNumber):
        self.elevatorController.goUpPushedFromFloorWhenIdle(aFloorNumber)

    def isWorking(self):
        return False

    def cabindDoorClosed(self):
        self.elevatorController.cabinDoorClosedWhenIdle()

    def cabinOnFloor(self, aFloorNumber):
        self.elevatorController.cabinOnFloorWhenIdle(aFloorNumber)

    def cabinDoorOpened(self):
        raise NotImplementedError()

    def openCabinDoor(self):
        self.elevatorController.openCabinDoorWhenIdle()

    def  closeCabinDoor(self):
        self.elevatorController.closeCabinDoorWhenIdle()

    def  waitForPeopleTimedOut(self):
        raise NotImplementedError()

class ElevatorControllerIsWorkingState(ElevatorControllerState):

    def __init__(self,elevatorController):
        self.elevatorController = elevatorController


    def goUpPushedFromFloor(self, aFloorNumber):
        self.elevatorController.goUpPushedFromFloorWhenWorking(aFloorNumber)

    def isIdle(self):
        return False

    def isWorking(self):
        return True

    def cabindDoorClosed(self):
        self.elevatorController.cabinDoorClosedWhenWorking()

    def cabinOnFloor(self, aFloorNumber):
        self.elevatorController.cabinOnFloorWhenWorking(aFloorNumber)

    def cabinDoorOpened(self):
        self.elevatorController.cabinDoorOpenendWhenWorking()

    def openCabinDoor(self):
        self.elevatorController.openCabinDoorWhenWorking()

    def waitForPeopleTimedOut(self):
        self.elevatorController.waitForPeopleTimedOutWhenWorking()

    def closeCabinDoor(self):
        self.elevatorController.closeCabinDoorWhenWorking()


class ElevatorController:

    def __init__(self):
        self.controllerIsIdle()
        self.cabinIsStopped()
        self.cabinDoorIsOpened()
        self._cabinFloorNumber = 0
        self._floorsToGo = []
        self._consoles = []

    def attach(self, console):
        self._consoles.append(console)

    def cabinDoorIsOpened(self):
        self._cabinDoorState = CabinDoorOpenedState(self)

    def cabinIsStopped(self):
        self._cabinState = CabinStoppedState(self)

    def controllerIsIdle(self):
        self._state = ElevatorControllerIdleState(self)

    #Elevator state
    def isIdle(self):
        return self._state.isIdle()

    def isWorking(self):
        return self._state.isWorking()

    #Door state
    def isCabinDoorOpened(self):
        return self._cabinDoorState.isOpened()

    def isCabinDoorOpening(self):
        return self._cabinDoorState.isOpening()

    def isCabinDoorClosed(self):
        return self._cabinDoorState.isClosed()

    def isCabinDoorClosing(self):
        return self._cabinDoorState.isClosing()

    #Cabin state
    def cabinFloorNumber(self):
        return self._cabinFloorNumber

    def isCabinStopped(self):
        return self._cabinState.isStopped()

    def isCabinMoving(self):
        return self._cabinState.isMoving()

    def isCabinWaitingForPeople(self):
        return self._cabinState.isWaitingForPeople()

    #Events
    def goUpPushedFromFloor(self, aFloorNumber):
        self._state.goUpPushedFromFloor(aFloorNumber)


    def cabinOnFloor(self, aFloorNumber):
        self._state.cabinOnFloor(aFloorNumber)


    def cabinDoorClosed(self):
        self._state.cabindDoorClosed()

    def openCabinDoor(self):
        self._state.openCabinDoor()

    def cabinDoorOpened(self):
        self._state.cabinDoorOpened()

    def waitForPeopleTimedOut(self):
        self._state.waitForPeopleTimedOut()

    def closeCabinDoor(self):
        self._state.closeCabinDoor()

    def goUpPushedFromFloorWhenIdle(self, aFloorNumber):
        self.appendToFloorsToGo(aFloorNumber)
        self.controllerIsWorking()
        self.cabinDoorIsClosing()

    def cabinDoorIsClosing(self):
        self._cabinDoorState = CabinDoorClosingState(self)
        for c in self._consoles:
            c.notifyClosingDoor()

    def controllerIsWorking(self):
        self._state = ElevatorControllerIsWorkingState(self)

    def cabinDoorClosedWhenWorking(self):
        self._cabinState.cabinDoorClosedWhenWorking()

    def cabinDoorClosedWhenWorkingAndCabinStopped(self):
        self._cabinDoorState.cabinDoorClosedWhenWorkingAndCabinStopped()

    def cabinDoorClosedWhenWorkingAndCabinStoppedAndClosing(self):
        self._cabinDoorState = CabinDoorClosedState(self)
        self._cabinState = CabinMovingState(self)

    def cabinOnFloorWhenWorking(self, aFloorNumber):
        if (aFloorNumber<self._cabinFloorNumber):
            raise ElevatorEmergency("Sensor de cabina desincronizado")
        if (self._cabinFloorNumber+1 != aFloorNumber):
            raise ElevatorEmergency("Sensor de cabina desincronizado")

        self._cabinFloorNumber = aFloorNumber
        if (self._floorsToGo[0] == aFloorNumber):
            self._floorsToGo.pop(0)
            self.cabinIsStopped()
            self.cabinDoorIsOpening()

    def cabinDoorIsOpening(self):
        self._cabinDoorState = CabinDoorOpeningState(self)

    def cabinOnFloorWhenIdle(self, aFloorNumber):
        raise ElevatorEmergency("Sensor de cabina desincronizado")

    def cabinDoorOpenendWhenWorking(self):
        self._cabinState.cabinDoorOpenedWhenWorking()

    def cabinDoorOpenedWhenWorkingAndCabinStopped(self):
        self.cabinDoorIsOpened()
        if(self.hasFloorToGo()):
            self.cabinIsWaitingForPeople()
        else:
            self.controllerStateIsIdle()

    def cabinIsWaitingForPeople(self):
        self._cabinState = CabinWaitingForPeopleState(self)

    def controllerStateIsIdle(self):
        self._state = ElevatorControllerIdleState(self)

    def hasFloorToGo(self):
        return len(self._floorsToGo)>0

    def openCabinDoorWhenIdle(self):
        #No hago nada porque me pidieron abrir la puerta cuando no estoy haciendo nada
        #y en ese caso ya esta abierta
        pass

    def openCabinDoorWhenWorking(self):
        self._cabinState.openCabinDoorWhenWorking()

    def openCabinDoorWhenWorkingAndCabinStopped(self):
        self._cabinDoorState.openCabinDoorWhenWorkingAndCabinStopped()

    def openCabinDoorWhenWorkingAndCabinStoppedAndDoorClosing(self):
        self.cabinDoorIsOpening()

    def openCabinDoorWhenWorkingAndCabinMoving(self):
        #No puedo abrir la puerta porque la cabina se esta moviendo!
        pass

    def openCabinDoorWhenWorkingAndCabinStoppedAndCabinDoorOpening(self):
        #Ya se esta abriendo!! no tengo que hacer nada
        pass

    def goUpPushedFromFloorWhenWorking(self, aFloorNumber):
        self.appendToFloorsToGo(aFloorNumber)

    def appendToFloorsToGo(self,aFloorNumber):
        self._floorsToGo.append(aFloorNumber)
        self._floorsToGo.sort()

    def waitForPeopleTimedOutWhenWorking(self):
        self._cabinState.waitForPeopleTimedOutWhenWorking()

    def waitForPeopleTimedOutWhenWorkingAndCabinWaitingForPeople(self):
        self.cabinIsStopped()
        self.cabinDoorIsClosing()

    def closeCabinDoorWhenWorking(self):
        self._cabinState.closeCabinDoorWhenWorking()

    def closeCabinDoorWhenWorkingAndCabinWaitingForPeople(self):
        self.waitForPeopleTimedOutWhenWorkingAndCabinWaitingForPeople()

    def closeCabinDoorWhenIdle(self):
        #No estoy haciendo nada y me piden cerrar la puerta, por lo tanto no la
        #cierro porque no tengo que mover la cabina puesto que estoy idle
        pass

    def closeCabinDoorWhenWorkingAndCabinMoving(self):
        #Si la cabina se esta moviendo, la puerta ya esta cerrada, por lo tanto
        #no tengo que volver a cerrarla
        pass

    def closeCabinDoorWhenWorkingAndCabinStopped(self):
        self._cabinDoorState.closeCabinDoorWhenWorkingAndCabinStopped()

    def closeCabinDoorWhenWorkingAndCabinStoppedAndCabinDoorOpening(self):
        #Estoy abriendo la puerta para que suba gente y me piden cerrarla.
        #No la cierro hasta no abrir completamente la puerta
        pass

    def cabinDoorClosedWhenIdle(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")

    def cabinDoorClosedWhenWorkingAndCabinMoving(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")

    def cabinDoorClosedWhenWorkingAndCabinStoppedAndCabinDoorOpening(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")



