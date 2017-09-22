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
from copy import copy

class AccountTransaction:
    def value(self):
        pass

    @classmethod
    def registerForOn(cls,value,account):
        return account.register(cls(value))

class Deposit(AccountTransaction):

    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value


class Withdraw(AccountTransaction):
    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value

class SummarizingAccount:

    def balance(self):
        return reduce(lambda balance, transaction: balance + transaction.value(),
                      self.transactions(),
                      0)

    def hasRegistered(self, transaction):
        pass

    def manages(self, account):
        pass

    def doesAnyAccount(self, condition):
        return any(map(condition, self.accounts()))

    def transactions(self):
        pass

class ReceptiveAccount(SummarizingAccount):
    def __init__(self):
        self._transactions=[]

    def register(self,aTransaction):
        self._transactions.append(aTransaction)
        return aTransaction

    def hasRegistered(self, transaction):
        return transaction in self._transactions

    def manages(self, account):
        return self==account

    def accounts(self):
        return [self]

    def transactions(self):
        return copy(self._transactions)


class Portfolio(SummarizingAccount):
    def __init__(self):
        self._accounts = []

    def accounts(self):
        return reduce(lambda total_accounts, account: total_accounts + account.accounts(), self._accounts, [])

    def transactions(self):
        return reduce(lambda transactions,account: transactions + account.transactions(), self._accounts, [])

    def hasRegistered(self, transaction):
        return self.doesAnyAccount(lambda account: account.hasRegistered(transaction))

    def managesAccount(self, anAccount):
        return self.doesAnyAccount(lambda account: account.manages(anAccount))

    def manages(self, anAccount):
        return anAccount.doesAnyAccount(self.managesAccount)

    def addAccount(self,account):
        if self.manages(account):
            raise Exception(Portfolio.ACCOUNT_ALREADY_MANAGED)
        self._accounts.append(account)

    def addAccounts(self, accounts):
        for account in accounts:
            self.addAccount(account)

    @classmethod
    def createWith(cls, *accounts):
        portfolio = Portfolio()
        portfolio.addAccounts(accounts)
        return portfolio

    ACCOUNT_ALREADY_MANAGED = "La cuenta ya esta manejada por otro portfolio"

class PortfolioTests(unittest.TestCase):

    def test01ReceptiveAccountHaveZeroAsBalanceWhenCreated(self):
        account = ReceptiveAccount()
        self.assertEquals(0,account.balance())

    def test02DepositIncreasesBalanceOnTransactionValue(self):
        account = ReceptiveAccount ()
        Deposit.registerForOn(100,account)

        self.assertEquals(100,account.balance())

    def test03WithdrawDecreasesBalanceOnTransactionValue(self):
        account = ReceptiveAccount ()
        Deposit.registerForOn(100,account)
        Withdraw.registerForOn(-50,account)

        self.assertEquals(50,account.balance())

    def test04PortfolioBalanceIsSumOfManagedAccountsBalance(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        complexPortfolio = Portfolio()
        complexPortfolio.addAccount(account1)
        complexPortfolio.addAccount(account2)

        Deposit.registerForOn(100,account1)
        Deposit.registerForOn(200,account2)

        self.assertEquals(300,complexPortfolio.balance())

    def test05PortfolioCanManagePortfolios(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        Deposit.registerForOn(100,account1)
        Deposit.registerForOn(200,account2)
        Deposit.registerForOn(300,account3)
        self.assertEquals(600,composedPortfolio.balance())


    def test06ReceptiveAccountsKnowsRegisteredTransactions(self):
        account = ReceptiveAccount ()
        deposit = Deposit.registerForOn(100,account)
        withdraw = Withdraw.registerForOn(-50,account)

        self.assertTrue(account.hasRegistered(deposit))
        self.assertTrue(account.hasRegistered(withdraw))

    def test07ReceptiveAccountsDoNotKnowNotRegisteredTransactions(self):
        account = ReceptiveAccount ()
        deposit = Deposit (100)
        withdraw = Withdraw (-50)

        self.assertFalse(account.hasRegistered(deposit))
        self.assertFalse(account.hasRegistered(withdraw))

    def test08PortofoliosKnowsTransactionsRegisteredByItsManagedAccounts(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        deposit1 = Deposit.registerForOn(100,account1)
        deposit2 = Deposit.registerForOn(200,account2)
        deposit3 = Deposit.registerForOn(300,account3)

        self.assertTrue(composedPortfolio.hasRegistered(deposit1))
        self.assertTrue(composedPortfolio.hasRegistered(deposit2))
        self.assertTrue(composedPortfolio.hasRegistered(deposit3))

    def test09PortofoliosDoNotKnowTransactionsNotRegisteredByItsManagedAccounts(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        deposit1 = Deposit(100)
        deposit2 = Deposit(200)
        deposit3 = Deposit(300)

        self.assertFalse(composedPortfolio.hasRegistered(deposit1))
        self.assertFalse(composedPortfolio.hasRegistered(deposit2))
        self.assertFalse(composedPortfolio.hasRegistered(deposit3))

    def test10ReceptiveAccountManageItSelf(self):
        account1 = ReceptiveAccount ()

        self.assertTrue(account1.manages(account1))

    def test11ReceptiveAccountDoNotManageOtherAccount(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()

        self.assertFalse(account1.manages(account2))

    def test12PortfolioManagesComposedAccounts(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)

        self.assertTrue(complexPortfolio.manages(account1))
        self.assertTrue(complexPortfolio.manages(account2))
        self.assertFalse(complexPortfolio.manages(account3))

    def test13PortfolioManagesComposedAccountsAndPortfolios(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        self.assertTrue(composedPortfolio.manages(account1))
        self.assertTrue(composedPortfolio.manages(account2))
        self.assertTrue(composedPortfolio.manages(account3))
        self.assertTrue(composedPortfolio.manages(complexPortfolio))

    def test14AccountsKnowsItsTransactions(self):
        account1 = ReceptiveAccount ()

        deposit1 = Deposit.registerForOn(100,account1)

        self.assertEquals(1,len(account1.transactions()))
        self.assertTrue(deposit1 in account1.transactions())

    def test15PortfolioKnowsItsAccountsTransactions(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        deposit1 = Deposit.registerForOn(100,account1)
        deposit2 = Deposit.registerForOn(200,account2)
        deposit3 = Deposit.registerForOn(300,account3)

        self.assertEquals(3,len(composedPortfolio.transactions()))
        self.assertTrue(deposit1 in composedPortfolio.transactions())
        self.assertTrue(deposit2 in composedPortfolio.transactions())
        self.assertTrue(deposit3 in composedPortfolio.transactions())

    def test16CanNotCreatePortfoliosWithRepeatedAccount(self):
        account1 = ReceptiveAccount ()
        try:
            Portfolio.createWith(account1,account1)
            self.fail()
        except Exception as invalidPortfolio:
            self.assertEquals(Portfolio.ACCOUNT_ALREADY_MANAGED, invalidPortfolio.message)

    def test17CanNotCreatePortfoliosWithAccountsManagedByOtherManagedPortfolio(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        try:
            Portfolio.createWith(complexPortfolio,account1)
            self.fail()
        except Exception as invalidPortfolio:
            self.assertEquals(Portfolio.ACCOUNT_ALREADY_MANAGED, invalidPortfolio.message)

if __name__ == '__main__':
    unittest.main()
