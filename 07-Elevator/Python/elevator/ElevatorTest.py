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

class OpenedDoor:
    def __init__(self):
        pass

    def stateForOpen(self):
        return self

    def stateForClose(self):
        return CLOSING_DOOR

class ClosedDoor:
    def __init__(self):
        pass

    def stateForOpen(self):
        return OPENING_DOOR

    def stateForClose(self):
        return self

class OpeningDoor:
    def __init__(self):
        pass

    def stateForOpen(self):
        return OPENED_DOOR

    def stateForClose(self):
        return CLOSING_DOOR

class ClosingDoor:
    def __init__(self):
        pass

    def stateForOpen(self):
        return OPENING_DOOR

    def stateForClose(self):
        return CLOSED_DOOR

OPENED_DOOR = OpenedDoor()
CLOSED_DOOR = ClosedDoor()
OPENING_DOOR = OpeningDoor()
CLOSING_DOOR = ClosingDoor()

class CabinDoor:
    OUT_OF_SYNC_DOOR_SENSOR = 'Sensor de puerta desincronizado'

    def __init__(self):
        self._state = OPENED_DOOR

    def open(self):
        self._state = self._state.stateForOpen()

    def close(self):
        self._state = self._state.stateForClose()

    def state(self):
        return self._state


class IdleMotor:
    def __init__(self):
        pass

    def stateForIdle(self):
        return self

    def stateForWork(self):
        return WORKING_MOTOR

class WorkingMotor:
    def __init__(self):
        pass

    def stateForIdle(self):
        return IDLE_MOTOR

    def stateForWork(self):
        return self

IDLE_MOTOR = IdleMotor()
WORKING_MOTOR = WorkingMotor()

class Motor:
    def __init__(self):
        self._state = IDLE_MOTOR

    def idle(self):
        self._state = self._state.stateForIdle()

    def work(self):
        self._state = self._state.stateForWork()

    def state(self):
        return self._state


class StoppedCabin:
    def __init__(self):
        pass

    def stateForMove(self):
        return MOVING_CABIN

    def stateForStop(self):
        return self

class MovingCabin:
    def __init__(self):
        pass

    def stateForMove(self):
        return self

    def stateForStop(self):
        return STOPPED_CABIN

STOPPED_CABIN = StoppedCabin()
MOVING_CABIN = MovingCabin()

class Cabin:
    OUT_OF_SYNC_CABIN_SENSOR = 'Sensor de cabina desincronizado'

    def __init__(self):
        self._state = STOPPED_CABIN
        self._cabinDoor = CabinDoor()
        self._floor = 0

    def floorNumber(self):
        return self._floor

    def nextFloor(self):
        self._floor += 1

    def move(self):
        if self.isDoorClosed():
            raise ElevatorEmergency(CabinDoor.OUT_OF_SYNC_DOOR_SENSOR)

        self._cabinDoor.close()
        self._state = self._state.stateForMove()

    def stop(self):
        self._state = self._state.stateForStop()

    def state(self):
        return self._state

    def isDoorOpened(self):
        return self._cabinDoor.state() is OPENED_DOOR

    def isDoorClosed(self):
        return self._cabinDoor.state() is CLOSED_DOOR

    def isDoorOpening(self):
        return self._cabinDoor.state() is OPENING_DOOR

    def isDoorClosing(self):
        return self._cabinDoor.state() is CLOSING_DOOR

    def closeDoor(self):
        self._cabinDoor.close()

    def openDoor(self):
        self._cabinDoor.open()


class ElevatorController:
    def __init__(self):
        self._cabin = Cabin()
        self._floorQueue = deque()
        self._motor = Motor()

    def isIdle(self):
        return self._motor.state() is IDLE_MOTOR

    def isWorking(self):
        return self._motor.state() is WORKING_MOTOR

    def isCabinStopped(self):
        return self._cabin.state() is STOPPED_CABIN

    def isCabinMoving(self):
        return self._cabin.state() is MOVING_CABIN

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
        if self._motor.state() is IDLE_MOTOR:
            self._cabin.closeDoor()
        self._motor.work()
        self._floorQueue.append(floor)

    def cabinDoorClosed(self):
        if len(self._floorQueue) == 0:
            raise ElevatorEmergency(CabinDoor.OUT_OF_SYNC_DOOR_SENSOR)

        self._cabin.move()

    def cabinOnFloor(self, floor):
        self._cabin.stop()
        self._cabin.openDoor()
        self._motor.work()
        self._cabin.nextFloor()
        if self._cabin.floorNumber() != floor:
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_CABIN_SENSOR)

        if len(self._floorQueue) == 0:
            raise ElevatorEmergency(Cabin.OUT_OF_SYNC_CABIN_SENSOR)

        if self._cabin.floorNumber() == self._floorQueue[0]:
            self._floorQueue.pop()

    def cabinDoorOpened(self):
        self._cabin.openDoor()
        if len(self._floorQueue) == 0:
            self._motor.idle()

    def openCabinDoor(self):
        if self._cabin.state() is not MOVING_CABIN and not self._cabin.isDoorOpening():
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
