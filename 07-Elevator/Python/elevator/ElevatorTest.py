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

class CabinDoorState:
    OPENED = 0
    CLOSED = 1
    OPENING = 2
    CLOSING = 3


class ElevatorController:
    def __init__(self):
        self._isIdle = True
        self._cabinDoorState = CabinDoorState.OPENED
        self._isCabinMoving = False
        self._floor = 0

    def isIdle(self):
        return self._isIdle

    def isWorking(self):
        return not self._isIdle

    def isCabinStopped(self):
        return not self._isCabinMoving

    def isCabinMoving(self):
        return self._isCabinMoving

    def isCabinDoorOpened(self):
        return self._cabinDoorState is CabinDoorState.OPENED

    def isCabinDoorClosed(self):
        return self._cabinDoorState is CabinDoorState.CLOSED

    def isCabinDoorOpening(self):
        return self._cabinDoorState is CabinDoorState.OPENING

    def isCabinDoorClosing(self):
        return self._cabinDoorState is CabinDoorState.CLOSING

    def cabinFloorNumber(self):
        return self._floor

    def goUpPushedFromFloor(self, floor):
        self._isIdle = False
        self._cabinDoorState = CabinDoorState.CLOSING

    def cabinDoorClosed(self):
        self._cabinDoorState = CabinDoorState.CLOSED
        self._isCabinMoving = True

    def cabinOnFloor(self, floor):
        self._isIdle = False
        self._isCabinMoving = False
        self._cabinDoorState = CabinDoorState.OPENING
        self._floor = floor

    def cabinDoorOpened(self):
        self._cabinDoorState = CabinDoorState.OPENED
        self._isIdle = True

    def openCabinDoor(self):
        if not self._isCabinMoving:
            if self._cabinDoorState in [CabinDoorState.CLOSED, CabinDoorState.CLOSING]:
                self._cabinDoorState = CabinDoorState.OPENING
            else:
                self._cabinDoorState = CabinDoorState.OPENED

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
