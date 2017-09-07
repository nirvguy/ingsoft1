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
import time

class CustomerBook:
    
    CUSTOMER_NAME_CAN_NOT_BE_EMPTY = 'Customer name can not be empty'
    CUSTOMER_ALREADY_EXIST = 'Customer already exists'
    INVALID_CUSTOMER_NAME = 'Invalid customer name'
    
    def __init__(self):
        self.customerNames = set()
    
    def addCustomerNamed(self,name):
        #El motivo por el cual se hacen estas verificaciones y se levanta esta excepcion es por motivos del
        #ejercicio - Hernan.
        if not name:
            raise ValueError(self.__class__.CUSTOMER_NAME_CAN_NOT_BE_EMPTY)
        if self.includesCustomerNamed(name):
            raise ValueError(self.__class__.CUSTOMER_ALREADY_EXIST)
        
        self.customerNames.add(name)
        
    def isEmpty(self):
        return self.numberOfCustomers()==0
    
    def numberOfCustomers(self):
        return len(self.customerNames)
    
    def includesCustomerNamed(self,name): 
        return name in self.customerNames
    
    def removeCustomerNamed(self,name):
        #Esta validacion mucho sentido no tiene, pero esta puesta por motivos del ejericion - Hernan
        if not self.includesCustomerNamed(name):
            raise KeyError(self.__class__.INVALID_CUSTOMER_NAME)
        
        self.customerNames.remove(name)

def measureTimeOfOperationInMilliseconds(operation):
    timeBeforeRunning = time.time()
    operation()
    timeAfterRunning = time.time()
    return (timeAfterRunning - timeBeforeRunning) * 1000

def setupCustomerBook(setup=None):
    customerBook = CustomerBook()
    if setup:
        setup(customerBook)
    return customerBook

class IdionTest(unittest.TestCase):
    def assertOperationTookLessThanNMilliseconds(self, timeOfOperation, maxTime):
        self.assertTrue(timeOfOperation < maxTime)

    def assertCustomerOperationDidNotTimedOut(self, maxTime, customerOperation, setupOperation=None):
        customerBook = setupCustomerBook(setupOperation)
        timeOfOperation = measureTimeOfOperationInMilliseconds(lambda : customerOperation(customerBook))
        self.assertOperationTookLessThanNMilliseconds(timeOfOperation, maxTime)

    def testAddingCustomerShouldNotTakeMoreThan50Milliseconds(self):
        self.assertCustomerOperationDidNotTimedOut(maxTime=50,
            customerOperation=lambda customerBook: customerBook.addCustomerNamed('John Lennon'))

    def testRemovingCustomerShouldNotTakeMoreThan100Milliseconds(self):
        paulMcCartney = 'Paul McCartney'
        self.assertCustomerOperationDidNotTimedOut(maxTime=100,
            customerOperation=lambda customerBook: customerBook.removeCustomerNamed(paulMcCartney),
            setupOperation=lambda customerBook: customerBook.addCustomerNamed(paulMcCartney))

    def assertOperationFails(self, operation, exceptionType, operationOnExcept):
        try:
            operation()
            self.fail()
        except exceptionType as exception:
            operationOnExcept(exception)

    def assertCustomerOperationFailsWithMessage(self, customerOperation, exceptionType, exceptionMessage, customerOperationOnExcept, setupOperation=None):
        customerBook = setupCustomerBook(setupOperation)

        def onExcept(exception):
            self.assertEquals(exception.message, exceptionMessage)
            customerOperationOnExcept(customerBook)

        self.assertOperationFails(operation=lambda: customerOperation(customerBook),
            exceptionType=exceptionType,
            operationOnExcept=onExcept)

    def testCanNotAddACustomerWithEmptyName(self):
        self.assertCustomerOperationFailsWithMessage(
            customerOperation=lambda customerBook: customerBook.addCustomerNamed(''),
            exceptionType=ValueError,
            exceptionMessage=CustomerBook.CUSTOMER_NAME_CAN_NOT_BE_EMPTY,
            customerOperationOnExcept=lambda customerBook: self.assertTrue(customerBook.isEmpty()))

    def testCanNotRemoveNotAddedCustomer(self):

        def assertThatCustomerBookDidNotChanged(customerBook):
            self.assertTrue(customerBook.numberOfCustomers()==1)
            self.assertTrue(customerBook.includesCustomerNamed('Paul McCartney'))

        self.assertCustomerOperationFailsWithMessage(
            customerOperation=lambda customerBook: customerBook.removeCustomerNamed('John Lennon'),
            exceptionType=KeyError,
            exceptionMessage=CustomerBook.INVALID_CUSTOMER_NAME,
            customerOperationOnExcept=assertThatCustomerBookDidNotChanged,
            setupOperation=lambda customerBook: customerBook.addCustomerNamed('Paul McCartney'))

      
if __name__ == "__main__":
    unittest.main()


