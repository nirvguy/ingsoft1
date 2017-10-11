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
from collections import deque

class CabinDoor:
    def __init__(self):
        self._state = OPENED_DOOR

    def toState(self, state):
        self._state = state

    def open(self):
        self._state.open(self)

    def close(self):
        self._state.close(self)

    def isOpened(self):
        return self._state is OPENED_DOOR

    def isClosed(self):
        return self._state is CLOSED_DOOR

    def isOpening(self):
        return self._state is OPENING_DOOR

    def isClosing(self):
        return self._state is CLOSING_DOOR

class OpenedDoor:
    def open(self, cabinDoor):
        pass

    def close(self, cabinDoor):
        cabinDoor.toState(CLOSING_DOOR)

class ClosedDoor:
    def open(self, cabinDoor):
        cabinDoor.toState(OPENING_DOOR)

    def close(self, cabinDoor):
        pass

class OpeningDoor:
    def open(self, cabinDoor):
        cabinDoor.toState(OPENED_DOOR)

    def close(self, cabinDoor):
        cabinDoor.toState(CLOSING_DOOR)

class ClosingDoor:
    def open(self, cabinDoor):
        cabinDoor.toState(OPENING_DOOR)

    def close(self, cabinDoor):
        cabinDoor.toState(CLOSED_DOOR)

OPENED_DOOR = OpenedDoor()
CLOSED_DOOR = ClosedDoor()
OPENING_DOOR = OpeningDoor()
CLOSING_DOOR = ClosingDoor()


class StoppedCabin:
    def __init__(self):
        pass

    def nextFloor(self, cabin):
        pass

    def move(self, cabin, targetFloor):
        if cabin.floorNumber() < targetFloor:
            cabin.toState(GOING_UP_CABIN)
        elif cabin.floorNumber() > targetFloor:
            cabin.toState(GOING_DOWN_CABIN)

    def stop(self, cabin):
        pass

class GoingUpCabin:
    def __init__(self):
        pass

    def nextFloor(self, cabin):
        cabin.setFloor(cabin.floorNumber() + 1)

    def move(self, cabin, targetFloor):
        if cabin.floorNumber() > targetFloor:
            cabin.toState(GOING_DOWN_CABIN)
        elif cabin.floorNumber() == targetFloor:
            cabin.toState(STOPPED_CABIN)

    def stop(self, cabin):
        cabin.toState(STOPPED_CABIN)

class GoingDownCabin:
    def __init__(self):
        pass

    def nextFloor(self, cabin):
        cabin.setFloor(cabin.floorNumber() - 1)

    def move(self, cabin, targetFloor):
        if cabin.floorNumber() < targetFloor:
            cabin.toState(GOING_UP_CABIN)
        elif cabin.floorNumber() == targetFloor:
            cabin.toState(STOPPED_CABIN)

    def stop(self, cabin):
        cabin.toState(STOPPED_CABIN)

STOPPED_CABIN = StoppedCabin()
GOING_UP_CABIN = GoingUpCabin()
GOING_DOWN_CABIN = GoingDownCabin()

class Cabin:
    OUT_OF_SYNC_CABIN_SENSOR = 'Sensor de cabina desincronizado'
    OUT_OF_SYNC_DOOR_SENSOR = 'Sensor de puerta desincronizado'

    def __init__(self):
        self._state = STOPPED_CABIN
        self._cabinDoor = CabinDoor()
        self._floor = 0

    def toState(self, state):
        self._state = state

    def setFloor(self, floor):
        self._floor = floor

    def floorNumber(self):
        return self._floor

    def nextFloor(self):
        self._state.nextFloor(self)

    def move(self, targetFloor):
        if self.isDoorClosed():
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_DOOR_SENSOR)

        self._cabinDoor.close()
        self._state.move(self, targetFloor)

    def stop(self):
        self._state.stop(self)

    def isMoving(self):
        return self._state is not STOPPED_CABIN

    def isStopped(self):
        return self._state is STOPPED_CABIN

    def isDoorOpened(self):
        return self._cabinDoor.isOpened()

    def isDoorClosed(self):
        return self._cabinDoor.isClosed()

    def isDoorOpening(self):
        return self._cabinDoor.isOpening()

    def isDoorClosing(self):
        return self._cabinDoor.isClosing()

    def closeDoor(self):
        self._cabinDoor.close()

    def openDoor(self):
        self._cabinDoor.open()


class ElevatorController:
    def __init__(self):
        self._cabin = Cabin()
        self._floorQueue = deque()

    def isIdle(self):
        return not self.isWorking()

    def isWorking(self):
        return self._cabin.isMoving() or self._cabin.isDoorOpening() or self._cabin.isDoorClosing() or len(self._floorQueue) > 0

    def isCabinStopped(self):
        return self._cabin.isStopped()

    def isCabinMoving(self):
        return self._cabin.isMoving()

    def isCabinDoorOpened(self):
        return self._cabin.isDoorOpened()

    def isCabinDoorClosed(self):
        return self._cabin.isDoorClosed()

    def isCabinDoorOpening(self):
        return self._cabin.isDoorOpening()

    def isCabinDoorClosing(self):
        return self._cabin.isDoorClosing()

    def isCabinWaitingForPeople(self):
        return self._cabin.isDoorOpened()

    def cabinFloorNumber(self):
        return self._cabin.floorNumber()

    def waitForPeopleTimedOut(self):
        self._cabin.closeDoor()

    def goUpPushedFromFloor(self, floor):
        if self.isIdle():
            self._cabin.closeDoor()
        self._floorQueue.append(floor)

    def cabinDoorClosed(self):
        if len(self._floorQueue) == 0:
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_DOOR_SENSOR)

        self._cabin.move(self._floorQueue[0])

    def cabinOnFloor(self, floor):
        if len(self._floorQueue) == 0:
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_CABIN_SENSOR)

        self._cabin.nextFloor()
        self._cabin.stop()
        self._cabin.openDoor()
        if self._cabin.floorNumber() != floor:
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_CABIN_SENSOR)

        if self._cabin.floorNumber() == self._floorQueue[0]:
            self._floorQueue.popleft()

    def cabinDoorOpened(self):
        self._cabin.openDoor()

    def openCabinDoor(self):
        if self._cabin.isStopped() and not self._cabin.isDoorOpening():
            self._cabin.openDoor()

    def closeCabinDoor(self):
        if len(self._floorQueue) > 0:
            self._cabin.closeDoor()


class ElevatorEmergency(Exception):
    pass

class ElevatorTest(unittest.TestCase):

    def test01ElevatorStartsIdleWithDoorOpenOnFloorZero(self):
        elevatorController = ElevatorController()

        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertEqual(0,elevatorController.cabinFloorNumber())

    def test02CabinDoorStartsClosingWhenElevatorGetsCalled(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)

        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())

        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())

        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertTrue(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())

    def test03CabinStartsMovingWhenDoorGetsClosed(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()

        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())

        self.assertFalse(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinMoving())

        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertTrue(elevatorController.isCabinDoorClosed())

    def test04CabinStopsAndStartsOpeningDoorWhenGetsToDestination(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())

        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())

        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertTrue(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())

        self.assertEquals(1,elevatorController.cabinFloorNumber())

    def test05ElevatorGetsIdleWhenDoorGetOpened(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()

        self.assertTrue(elevatorController.isIdle())
        self.assertFalse(elevatorController.isWorking())

        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())

        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())

        self.assertEquals(1,elevatorController.cabinFloorNumber())

    # STOP HERE!

    def test06DoorKeepsOpenedWhenOpeningIsRequested(self):
        elevatorController = ElevatorController()

        self.assertTrue(elevatorController.isCabinDoorOpened())

        elevatorController.openCabinDoor()

        self.assertTrue(elevatorController.isCabinDoorOpened())

    def test07DoorMustBeOpenedWhenCabinIsStoppedAndClosingDoors(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    def test08CanNotOpenDoorWhenCabinIsMoving(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())


    def test09DoorKeepsOpeneingWhenItIsOpeneing(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    # STOP HERE!!

    def test10RequestToGoUpAreEnqueueWhenRequestedWhenCabinIsMoving(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())


    def test11CabinDoorStartClosingAfterWaitingForPeople(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())


    def test12StopsWaitingForPeopleIfCloseDoorIsPressed(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())



    def test13CloseDoorDoesNothingIfIdle(self):
        elevatorController = ElevatorController()

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())



    def test14CloseDoorDoesNothingWhenCabinIsMoving(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())


    def test15CloseDoorDoesNothingWhenOpeningTheDoorToWaitForPeople(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    # STOP HERE!!

    def test16ElevatorHasToEnterEmergencyIfStoppedAndOtherFloorSensorTurnsOn(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")

    def test17ElevatorHasToEnterEmergencyIfFalling(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")



    def test18ElevatorHasToEnterEmergencyIfJumpsFloors(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(3)
        elevatorController.cabinDoorClosed()
        try:
            elevatorController.cabinOnFloor(3)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")



    def test19ElevatorHasToEnterEmergencyIfDoorClosesAutomatically(self):
        elevatorController = ElevatorController()

        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")



    def test20ElevatorHasToEnterEmergencyIfDoorClosedSensorTurnsOnWhenClosed(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")



    def test21ElevatorHasToEnterEmergencyIfDoorClosesWhenOpening(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")



    # STOP HERE!!
    # More tests here to verify bad sensor function

    def test22CabinHasToStopOnTheFloorsOnItsWay(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    def test23ElevatorCompletesAllTheRequests(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(2)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    def test24CabinHasToStopOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())


    def test25CabinHasToStopAndWaitForPeopleOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()

        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())

if __name__ == '__main__':
    unittest.main()
