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

    def updateBalance(self, balance, account):
        pass

    @classmethod
    def registerForOn(cls,value,account):
        return account.register(cls(value))

class Deposit(AccountTransaction):

    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value

    def accountTransferNet(self):
        return 0

    def accountTransactionValue(self):
        return self.value()

    def visit(self, reducer):
        return reducer.deposit(self)

class Withdraw(AccountTransaction):
    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value

    def accountTransferNet(self):
        return 0

    def accountTransactionValue(self):
        return -self.value()

    def visit(self, reducer):
        return reducer.withdraw(self)

class Transfer:
    def __init__(self, transaction):
        self._transaction = transaction

    def accountTransferNet(self):
        return self._transaction.accountTransactionValue()

    def accountTransactionValue(self):
        return self._transaction.accountTransactionValue()

    def visit(self, reducer):
        return reducer.transfer(self)

    @classmethod
    def registerFor(cls, value, fromAccount, toAccount):
        fromAccount.register(cls(Withdraw(value)))
        toAccount.register(cls(Deposit(value)))

class SummarizingAccount:

    def balance(self):
        pass

    def hasRegistered(self, transaction):
        pass

    def manages(self, account):
        pass

    def transactions(self):
        pass

    def reversePortofolioTreeOf(self, accountNames):
        return list(reversed(self.portfolioTreeOf(accountNames)))

class ReceptiveAccount(SummarizingAccount):
    def __init__(self):
        self._transactions=[]

    def balance(self):
        return BalanceReducer(self).reduce()

    def register(self,aTransaction):
        self._transactions.append(aTransaction)
        return aTransaction

    def hasRegistered(self, transaction):
        return transaction in self._transactions

    def manages(self, account):
        return self==account

    def transactions(self):
        return copy(self._transactions)

    def visit(self, treeCalculator):
        return treeCalculator.receptive()

class Portfolio(SummarizingAccount):
    def __init__(self):
        self._accounts=[]

    def balance(self):
        #return reduce(
        #              lambda balance,account: balance+account.balance(),
        #              self._accounts, 0)
        #return sum(map(lambda account: account.balance(), self._accounts))
        return sum(account.balance() for account in self._accounts)

    def hasRegistered(self, transaction):
        #return reduce(
        #              lambda result,account: result or account.hasRegistered(transaction),
        #              self._accounts, False)
        #return any(map(lambda account: account.hasRegistered(transaction),self._accounts))
        return any(account.hasRegistered(transaction) for account in self._accounts)

    def manages(self, anAccount):
        #return reduce(
        #            lambda result,account: result or account.manages(anAccount),
        #            self._accounts, self==anAccount)
        #return self==anAccount or any(map(lambda account: account.manages(anAccount),self._accounts))
        return self==anAccount or any(account.manages(anAccount) for account in self._accounts)

    def transactions(self):
        #return reduce(lambda transactions,account: transactions + account.transactions(),self._accounts, [])
        return [xfer for acc in self._accounts for xfer in acc.transactions()]

    def addAccount(self,account):
        if self.manages(account):
            raise Exception(self.__class__.ACCOUNT_ALREADY_MANAGED)

        self._accounts.append(account)

    def accounts(self):
        return self._accounts

    def visit(self, treeCalculator):
        return treeCalculator.portfolio()

    @classmethod
    def createWith(cls,anAccount,anotherAccount):
        portfolio = cls()
        portfolio.addAccount(anAccount)
        portfolio.addAccount(anotherAccount)
        return portfolio

    ACCOUNT_ALREADY_MANAGED = "La cuenta ya esta manejada por otro portfolio"

class CertificateOfDeposit(AccountTransaction):
    def __init__(self, value, numberOfDays, tna):
        self._value = value
        self._numberOfDays = numberOfDays
        self._tna = tna

    def value(self):
        return self._value

    def earnings(self):
        return self._value*(self._tna/360)*self._numberOfDays

    def numberOfDays(self):
        return self._numberOfDays

    def tna(self):
        return self._tna

    def accountTransferNet(self):
        return 0

    def accountTransactionValue(self):
        return -self.value()

    def visit(self, reducer):
        return reducer.certificateOfDeposit(self)

    @classmethod
    def registerFor(cls, value, numberOfDays, tna, account):
        certificateOfDeposit = cls(value,numberOfDays,tna)
        account.register(certificateOfDeposit)

        return certificateOfDeposit

class TransactionReducer:
    def __init__(self, account):
        self._account = account

    def deposit(self, transaction):
        pass

    def withdraw(self, transaction):
        pass

    def transfer(self, transaction):
        pass

    def certificateOfDeposit(self, transaction):
        pass

    def _mapTransactions(self):
        return map(lambda transaction: transaction.visit(self),
                   self._account.transactions())

    def reduce(self):
        return self.__class__.reducer(self._mapTransactions())

class BalanceReducer(TransactionReducer):
    reducer = sum

    def deposit(self, transaction):
        return transaction.value()

    def withdraw(self, transaction):
        return -transaction.value()

    def transfer(self, transaction):
        return transaction.accountTransactionValue()

    def certificateOfDeposit(self, transaction):
        return -transaction.value()

class SummaryReducer(TransactionReducer):
    reducer = list

    def deposit(self, transaction):
        return "Deposito por {}".format(transaction.value())

    def withdraw(self, transaction):
        return "Extraccion por {}".format(transaction.value())

    def transfer(self, transaction):
        return "Transferencia por {}".format(transaction.accountTransactionValue())

    def certificateOfDeposit(self, transaction):
        return "Plazo fijo por {} durante {} dias a una tna de {}".format(transaction.value(), transaction.numberOfDays(), transaction.tna())

class AccountTransferNetReducer(TransactionReducer):
    reducer = sum

    def deposit(self, transaction):
        return 0

    def withdraw(self, transaction):
        return 0

    def transfer(self, transaction):
        return transaction.accountTransferNet()

    def certificateOfDeposit(self, transaction):
        return 0

class InvestmentNetReducer(TransactionReducer):
    reducer = sum

    def deposit(self, transaction):
        return 0

    def withdraw(self, transaction):
        return 0

    def transfer(self, transaction):
        return 0

    def certificateOfDeposit(self, transaction):
        return transaction.value()

class InvestmentEarningsReducer(TransactionReducer):
    reducer = sum
    def deposit(self, transaction):
        return 0

    def withdraw(self, transaction):
        return 0

    def transfer(self, transaction):
        return 0

    def certificateOfDeposit(self, transaction):
        return transaction.earnings()

class TreeCalculator(object):
    def __init__(self, account, accountNames):
        self._account = account
        self._accountNames = accountNames

    def receptive(self):
        return [self._accountNames[self._account]]

    def portfolio(self):
        account_tree = [self._accountNames[self._account]]
        for account in self._account.accounts():
            treeCalculator = TreeCalculator(account, self._accountNames)
            account_tree.extend(map(lambda text: ' ' + text,
                                    treeCalculator.tree()))
        return account_tree

    def tree(self):
        return self._account.visit(self)

class ReverseTreeCalculator(TreeCalculator):
    def tree(self):
        return list(reversed(super(self.__class__, self).tree()))

class PortfolioTests(unittest.TestCase):

    def test01ReceptiveAccountHaveZeroAsBalanceWhenCreated(self):
        account = ReceptiveAccount()
        self.assertEqual(0,account.balance())

    def test02DepositIncreasesBalanceOnTransactionValue(self):
        account = ReceptiveAccount ()
        Deposit.registerForOn(100,account)

        self.assertEqual(100,account.balance())

    def test03WithdrawDecreasesBalanceOnTransactionValue(self):
        account = ReceptiveAccount ()
        Deposit.registerForOn(100,account)
        Withdraw.registerForOn(50,account)

        self.assertEqual(50,account.balance())

    def test04PortfolioBalanceIsSumOfManagedAccountsBalance(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        complexPortfolio = Portfolio()
        complexPortfolio.addAccount(account1)
        complexPortfolio.addAccount(account2)

        Deposit.registerForOn(100,account1)
        Deposit.registerForOn(200,account2)

        self.assertEqual(300,complexPortfolio.balance())

    def test05PortfolioCanManagePortfolios(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        Deposit.registerForOn(100,account1)
        Deposit.registerForOn(200,account2)
        Deposit.registerForOn(300,account3)
        self.assertEqual(600,composedPortfolio.balance())


    def test06ReceptiveAccountsKnowsRegisteredTransactions(self):
        account = ReceptiveAccount ()
        deposit = Deposit.registerForOn(100,account)
        withdraw = Withdraw.registerForOn(50,account)

        self.assertTrue(account.hasRegistered(deposit))
        self.assertTrue(account.hasRegistered(withdraw))

    def test07ReceptiveAccountsDoNotKnowNotRegisteredTransactions(self):
        account = ReceptiveAccount ()
        deposit = Deposit (100)
        withdraw = Withdraw (50)

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

        self.assertEqual(1,len(account1.transactions()))
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

        self.assertEqual(3,len(composedPortfolio.transactions()))
        self.assertTrue(deposit1 in composedPortfolio.transactions())
        self.assertTrue(deposit2 in composedPortfolio.transactions())
        self.assertTrue(deposit3 in composedPortfolio.transactions())

    def test16CanNotCreatePortfoliosWithRepeatedAccount(self):
        account1 = ReceptiveAccount ()
        try:
            Portfolio.createWith(account1,account1)
            self.fail()
        except Exception as invalidPortfolio:
            self.assertEqual(Portfolio.ACCOUNT_ALREADY_MANAGED, str(invalidPortfolio))

    def test17CanNotCreatePortfoliosWithAccountsManagedByOtherManagedPortfolio(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        try:
            Portfolio.createWith(complexPortfolio,account1)
            self.fail()
        except Exception as invalidPortfolio:
            self.assertEqual(Portfolio.ACCOUNT_ALREADY_MANAGED, str(invalidPortfolio))

    def test18TransferShouldWithdrawFromFromAccountAndDepositIntoToAccount(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Transfer.registerFor(100,fromAccount, toAccount)

        self.assertEqual(-100, fromAccount.balance())
        self.assertEqual(100, toAccount.balance())


    def test19AccountSummaryShouldProvideHumanReadableTransactionsDetail(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)

        lines = self.accountSummaryLines(fromAccount)

        self.assertEqual(3,len(lines))
        self.assertEqual("Deposito por 100", lines[0])
        self.assertEqual("Extraccion por 50", lines[1])
        self.assertEqual("Transferencia por -100", lines[2])


    def accountSummaryLines(self,fromAccount):
        return SummaryReducer(fromAccount).reduce()

    def test20ShouldBeAbleToBeQueryTransferNet(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        Transfer.registerFor(250,toAccount, fromAccount)

        self.assertEqual(150.0,self.accountTransferNet(fromAccount))
        self.assertEqual(-150.0,self.accountTransferNet(toAccount))

    def accountTransferNet(self, account):
        return AccountTransferNetReducer(account).reduce()

    def test21CertificateOfDepositShouldWithdrawInvestmentValue(self):
        account = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(1000,account)
        Withdraw.registerForOn(50,account)
        Transfer.registerFor(100,account, toAccount)
        CertificateOfDeposit.registerFor(100,30,0.1,account)

        self.assertEqual(100.0,self.investmentNet(account))
        self.assertEqual(750.0,account.balance())


    def investmentNet(self,account):
        return InvestmentNetReducer(account).reduce()

    def test22ShouldBeAbleToQueryInvestmentEarnings(self):
        account = ReceptiveAccount ()

        CertificateOfDeposit.registerFor(100,30,0.1,account)
        CertificateOfDeposit.registerFor(100,60,0.15,account)

        investmentEarnings = 100*(0.1/360)*30 + 100*(0.15/360)*60

        self.assertEqual(investmentEarnings,self.investmentEarnings(account))

    def investmentEarnings(self, account):
        return InvestmentEarningsReducer(account).reduce()

    def test23AccountSummaryShouldWorkWithCertificateOfDeposit(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        CertificateOfDeposit.registerFor(1000, 30, 0.1, fromAccount)

        lines = self.accountSummaryLines(fromAccount)

        self.assertEqual(4,len(lines))
        self.assertEqual("Deposito por 100", lines[0])
        self.assertEqual("Extraccion por 50", lines[1])
        self.assertEqual("Transferencia por -100", lines[2])
        self.assertEqual("Plazo fijo por 1000 durante 30 dias a una tna de 0.1", lines[3])

    def test24ShouldBeAbleToBeQueryTransferNetWithCertificateOfDeposit(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        Transfer.registerFor(250,toAccount, fromAccount)
        CertificateOfDeposit.registerFor(1000, 30, 0.1, fromAccount)

        self.assertEqual(150.0,self.accountTransferNet(fromAccount))
        self.assertEqual(-150.0,self.accountTransferNet(toAccount))

    def test25PortfolioTreePrinter(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        accountNames = dict()
        accountNames[composedPortfolio]= "composedPortfolio"
        accountNames[complexPortfolio]= "complexPortfolio"
        accountNames[account1]= "account1"
        accountNames[account2]="account2"
        accountNames[account3]="account3"

        lines = self.portofolioTreeOf(composedPortfolio, accountNames)

        self.assertEqual(5, len(lines))
        self.assertEqual("composedPortfolio", lines[0])
        self.assertEqual(" complexPortfolio", lines[1])
        self.assertEqual("  account1", lines[2])
        self.assertEqual("  account2", lines[3])
        self.assertEqual(" account3", lines[4])

    def portofolioTreeOf(self, composedPortfolio, accountNames):
        return TreeCalculator(composedPortfolio, accountNames).tree()

    def test26ReversePortfolioTreePrinter(self):
        account1 = ReceptiveAccount ()
        account2 = ReceptiveAccount ()
        account3 = ReceptiveAccount ()
        complexPortfolio = Portfolio.createWith(account1,account2)
        composedPortfolio = Portfolio.createWith(complexPortfolio,account3)

        accountNames = dict()
        accountNames[composedPortfolio]= "composedPortfolio"
        accountNames[complexPortfolio]= "complexPortfolio"
        accountNames[account1]= "account1"
        accountNames[account2]="account2"
        accountNames[account3]="account3"

        lines = self.reversePortofolioTreeOf(composedPortfolio, accountNames)

        self.assertEqual(5, len(lines))
        self.assertEqual(" account3", lines[0])
        self.assertEqual("  account2", lines[1])
        self.assertEqual("  account1", lines[2])
        self.assertEqual(" complexPortfolio", lines[3])
        self.assertEqual("composedPortfolio", lines[4])

    def reversePortofolioTreeOf(self, composedPortfolio, accountNames):
        return ReverseTreeCalculator(composedPortfolio, accountNames).tree()
