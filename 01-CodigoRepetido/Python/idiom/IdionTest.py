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
        self.assertCustomerOperationDidNotTimedOut(50,
            lambda customerBook: customerBook.addCustomerNamed('John Lennon'))

    def testRemovingCustomerShouldNotTakeMoreThan100Milliseconds(self):
        paulMcCartney = 'Paul McCartney'
        self.assertCustomerOperationDidNotTimedOut(100,
            lambda customerBook: customerBook.removeCustomerNamed(paulMcCartney),
            lambda customerBook: customerBook.addCustomerNamed(paulMcCartney))

    def testCanNotAddACustomerWithEmptyName(self):
        customerBook = CustomerBook()
        
        try:
            customerBook.addCustomerNamed('')
            self.fail()
        except ValueError as exception:
            self.assertEquals(exception.message,CustomerBook.CUSTOMER_NAME_CAN_NOT_BE_EMPTY)
            self.assertTrue(customerBook.isEmpty())
                 
    def testCanNotRemoveNotAddedCustomer(self):
        customerBook = CustomerBook()
        customerBook.addCustomerNamed('Paul McCartney')
        
        try:
            customerBook.removeCustomerNamed('John Lennon')
            self.fail()
        except KeyError as exception:
            self.assertEquals(exception.message,CustomerBook.INVALID_CUSTOMER_NAME)
            self.assertTrue(customerBook.numberOfCustomers()==1)
            self.assertTrue(customerBook.includesCustomerNamed('Paul McCartney'))

      
if __name__ == "__main__":
    unittest.main()


