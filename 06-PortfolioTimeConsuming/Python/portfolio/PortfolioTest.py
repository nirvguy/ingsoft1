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
from copy import copy

class AccountTransaction:
    def value(self):
        pass

    def accept(self, aVisitor):
        pass

    @classmethod
    def registerForOn(cls,value,account):
        return account.register(cls(value))

class Deposit(AccountTransaction):

    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value

    def accept(self, aVisitor):
        return aVisitor.visitDeposit(self);

class Withdraw(AccountTransaction):
    def __init__(self,value):
        self._value = value

    def value(self):
        return self._value

    def accept(self, aVisitor):
        return aVisitor.visitWithdraw(self);

class Transfer:
    def __init__(self,value, fromAccount, toAccount):
        self._value = value
        self._fromAccount = fromAccount
        self._toAccount = toAccount

    @classmethod
    def registerFor(cls, value, fromAccount, toAccount):
        transfer = Transfer(value,fromAccount,toAccount)
        fromAccount.register(transfer.withdrawLeg())
        toAccount.register(transfer.depositLeg())

        return transfer

    def depositLeg(self):
        return TransferDeposit(self)

    def withdrawLeg(self):
        return TransferWithdraw(self)

    def value (self):
        return self._value

class TransferDeposit(AccountTransaction):
    def __init__ (self, transfer):
        self._transfer = transfer

    def value(self):
        return self._transfer.value();

    def accept(self, aVisitor):
        return aVisitor.visitTransferDeposit(self);

class TransferWithdraw(AccountTransaction):
    def __init__ (self, transfer):
        self._transfer = transfer

    def value(self):
        return self._transfer.value();

    def accept(self, aVisitor):
        return aVisitor.visitTransferWithdraw(self);

class SummarizingAccount:

    def balance(self):
        pass

    def hasRegistered(self, transaction):
        pass

    def manages(self, account):
        pass

    def transactions(self):
        pass

    def acceptTransactionsVisitor(self, aVisitor):
        pass

    def accept(self, aVisitor):
        pass

class ReceptiveAccount(SummarizingAccount):
    def __init__(self):
        self._transactions=[]

    def balance(self):
        return BalanceVisitor(self).value()

    def register(self,aTransaction):
        self._transactions.append(aTransaction)
        return aTransaction

    def hasRegistered(self, transaction):
        return transaction in self._transactions

    def manages(self, account):
        return self==account

    def transactions(self):
        return copy(self._transactions)

    def acceptTransactionsVisitor(self, aVisitor):
        for transation in self._transactions:
            transation.accept(aVisitor)

    def accept(self, aVisitor):
        aVisitor.visitReceptiveAccount(self)

class Portfolio(SummarizingAccount):
    def __init__(self):
        self._accounts=[]

    def balance(self):
        return reduce(lambda balance,account: balance+account.balance(), self._accounts, 0)

    def hasRegistered(self, transaction):
        return reduce(lambda result,account: account.hasRegistered(transaction) or result, self._accounts, False)

    def manages(self, anAccount):
        return self==anAccount or reduce(lambda result,account: account.manages(anAccount) or result,self._accounts, False)

    def transactions(self):
        return reduce(lambda transactions,account: transactions + account.transactions(),self._accounts, [])

    def addAccount(self,account):
        if self.manages(account):
            raise Exception(self.__class__.ACCOUNT_ALREADY_MANAGED)

        self._accounts.append(account)

    def acceptTransactionsVisitor(self, aVisitor):
        for summarizingAccount in self._summarizingAccounts:
            summarizingAccount.acceptTransactionsVisitor(aVisitor)

    def accept(self, aVisitor):
        aVisitor.visitPortfolio(self)

    def visitAccountsWith(self, aVisitor):
        for summarizinAccount in self._accounts:
            summarizinAccount.accept(aVisitor)

    @classmethod
    def createWith(cls,anAccount,anotherAccount):
        portfolio = cls()
        portfolio.addAccount(anAccount)
        portfolio.addAccount(anotherAccount)
        return portfolio

    ACCOUNT_ALREADY_MANAGED = "La cuenta ya esta manejada por otro portfolio"

class AccountTransactionVisitor:
    pass

class AccountSummary(AccountTransactionVisitor):
    def __init__(self, account):
        self._account = account

    def lines(self):
        time.sleep(1)
        self._lines = []
        self._account.acceptTransactionsVisitor(self)

        return self._lines

    def visitDeposit(self, deposit):
        self._lines.append("Deposito por " + str(deposit.value()))

    def visitWithdraw(self, withdraw):
        self._lines.append("Extraccion por " + str(withdraw.value()))

    def visitCertificateOfDeposit(self, certificateOfDeposit):
        self._lines.append(
                "Plazo fijo por " + str(certificateOfDeposit.value())+
                " durante " + str(certificateOfDeposit.numberOfDays())+
                " dias a una tna de " + str(certificateOfDeposit.tna()))

    def visitTransferDeposit(self, transferDeposit):
        self._lines.append("Transferencia por " + str(transferDeposit.value ()))

    def visitTransferWithdraw(self, transferWithdraw):
        self._lines.append("Transferencia por " + str(-transferWithdraw.value ()))

class BalanceVisitor(AccountTransactionVisitor):
    def __init__(self, account):
        self._account = account

    def value(self):
        self._value = 0
        self._account.acceptTransactionsVisitor(self)
        return self._value

    def visitDeposit(self, deposit):
        self._value += deposit.value()

    def visitWithdraw(self, withdraw):
        self._value -= withdraw.value()

    def visitCertificateOfDeposit(self, certificateOfDeposit):
        self._value -= certificateOfDeposit.value()

    def visitTransferDeposit(self, transferDeposit):
        self._value += transferDeposit.value()

    def visitTransferWithdraw(self, transferWithdraw):
        self._value -= transferWithdraw.value()

class TransferNet(AccountTransactionVisitor):
    def __init__(self, account):
        self._account = account

    def value(self):
        self._value = 0
        self._account.acceptTransactionsVisitor(self)
        return self._value

    def visitDeposit(self, deposit):
        pass

    def visitWithdraw(self, withdraw):
        pass

    def visitCertificateOfDeposit(self, certificateOfDeposit):
        pass

    def visitTransferDeposit(self, transferDeposit):
        self._value += transferDeposit.value()

    def visitTransferWithdraw(self, transferWithdraw):
        self._value -= transferWithdraw.value()

class CertificateOfDeposit(AccountTransaction):
    def __init__(self, value, numberOfDays, tna):
        self._value = value
        self._numberOfDays = numberOfDays
        self._tna = tna

    def accept(self, aVisitor):
        aVisitor.visitCertificateOfDeposit(self)

    def value(self):
        return self._value

    def earnings(self):
        return self._value*(self._tna/360)*self._numberOfDays

    def numberOfDays(self):
        return self._numberOfDays

    def tna(self):
        return self._tna

    @classmethod
    def registerFor(cls, value, numberOfDays, tna, account):
        certificateOfDeposit = cls(value,numberOfDays,tna)
        account.register(certificateOfDeposit)

        return certificateOfDeposit


class InvestmentNet:
    def __init__(self, account):
        self._account = account

    def value(self):
        time.sleep(1)
        self._value = 0
        self._account.acceptTransactionsVisitor(self)

        return self._value

    def visitCertificateOfDeposit(self, certificateOfDeposit):
        self._value = certificateOfDeposit.value()

    def visitDeposit(self, deposit):
        pass

    def visitWithdraw(self, withdraw):
        pass

    def visitTransferDeposit(self, transferDeposit):
        pass

    def  visitTransferWithdraw(self, transferWithdraw):
        pass

class InvestmentEarnings:
    def __init__(self, account):
        self._account = account

    def value(self):
        time.sleep(1)
        self._value = 0
        self._account.acceptTransactionsVisitor(self)

        return self._value

    def visitCertificateOfDeposit(self, certificateOfDeposit):
        self._value += certificateOfDeposit.earnings()

    def visitDeposit(self, deposit):
        pass

    def visitWithdraw(self, withdraw):
        pass

    def visitTransferDeposit(self, transferDeposit):
        pass

    def  visitTransferWithdraw(self, transferWithdraw):
        pass

class PortfolioTreePrinter:
    def __init__(self, portfolio, accountNames):
        self._portfolio = portfolio
        self._accountNames = accountNames

    def lines(self):
        self._lines = []
        self._spaces = 0

        self._portfolio.accept(self)

        return self._lines

    def visitPortfolio(self, portfolio):
        self.lineFor(portfolio)
        self._spaces += 1
        portfolio.visitAccountsWith(self)
        self._spaces -= 1

    def lineFor(self, summarizingAccount):
        line = ""
        for i in range(self._spaces):
            line = line + " "

        line = line + self._accountNames[summarizingAccount]
        self._lines.append(line)

    def visitReceptiveAccount(self, receptiveAccount):
        self.lineFor(receptiveAccount)

class ReversePortfolioTreePrinter:
    def __init__(self, portfolio, accountNames):
        self._portfolio = portfolio
        self._accountNames = accountNames

    def lines(self):
        printer = PortfolioTreePrinter(self._portfolio,self._accountNames)
        lines = printer.lines()
        lines.reverse()
        return lines

class AccountSummaryWithInvestmentEarnings:

    def __init__(self, account):
        self._account = account

    def lines(self):
        summary = AccountSummary(self._account)
        investmentEarnings = InvestmentEarnings(self._account)

        lines = summary.lines()
        lines.append("Ganancias por " + str(investmentEarnings.value()))

        return lines

class AccountSummaryWithAllInvestmentInformation:

    def __init__(self, account):
        self._account = account

    def lines(self):
        summary = AccountSummaryWithInvestmentEarnings(self._account)
        investmentNet = InvestmentNet(self._account)

        lines = summary.lines()
        lines.append("Inversiones por " + str(investmentNet.value()))

        return lines

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
        Withdraw.registerForOn(50,account)

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

    def test18TransferShouldWithdrawFromFromAccountAndDepositIntoToAccount(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Transfer.registerFor(100,fromAccount, toAccount)

        self.assertEquals(-100, fromAccount.balance())
        self.assertEquals(100, toAccount.balance())


    def test19AccountSummaryShouldProvideHumanReadableTransactionsDetail(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)

        lines = self.accountSummaryLines(fromAccount)

        self.assertEquals(3,len(lines))
        self.assertEquals("Deposito por 100", lines[0])
        self.assertEquals("Extraccion por 50", lines[1])
        self.assertEquals("Transferencia por -100", lines[2])


    def accountSummaryLines(self,fromAccount):
        summary = AccountSummary(fromAccount)
        lines = summary.lines()
        return lines

    def test20ShouldBeAbleToBeQueryTransferNet(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        Transfer.registerFor(250,toAccount, fromAccount)

        self.assertEquals(150.0,self.accountTransferNet(fromAccount))
        self.assertEquals(-150.0,self.accountTransferNet(toAccount))


    def accountTransferNet(self, account):
        accountTransferNet = TransferNet(account)
        return accountTransferNet.value()


    def test21CertificateOfDepositShouldWithdrawInvestmentValue(self):
        account = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(1000,account)
        Withdraw.registerForOn(50,account)
        Transfer.registerFor(100,account, toAccount)
        CertificateOfDeposit.registerFor(100,30,0.1,account)

        self.assertEquals(100.0,self.investmentNet(account))
        self.assertEquals(750.0,account.balance())


    def investmentNet(self,account):
        accountInvestmentNet = InvestmentNet(account)
        return accountInvestmentNet.value()


    def test22ShouldBeAbleToQueryInvestmentEarnings(self):
        account = ReceptiveAccount ()

        CertificateOfDeposit.registerFor(100,30,0.1,account)
        CertificateOfDeposit.registerFor(100,60,0.15,account)

        investmentEarnings = 100*(0.1/360)*30 + 100*(0.15/360)*60

        self.assertEquals(investmentEarnings,self.investmentEarnings(account))

    def investmentEarnings(self, account):
        accountInvestmentEarnings = InvestmentEarnings(account)
        return accountInvestmentEarnings.value()

    def test23AccountSummaryShouldWorkWithCertificateOfDeposit(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        CertificateOfDeposit.registerFor(1000, 30, 0.1, fromAccount)

        lines = self.accountSummaryLines(fromAccount)

        self.assertEquals(4,len(lines))
        self.assertEquals("Deposito por 100", lines[0])
        self.assertEquals("Extraccion por 50", lines[1])
        self.assertEquals("Transferencia por -100", lines[2])
        self.assertEquals("Plazo fijo por 1000 durante 30 dias a una tna de 0.1", lines[3])

    def test24ShouldBeAbleToBeQueryTransferNetWithCertificateOfDeposit(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        Transfer.registerFor(250,toAccount, fromAccount)
        CertificateOfDeposit.registerFor(1000, 30, 0.1, fromAccount)

        self.assertEquals(150.0,self.accountTransferNet(fromAccount))
        self.assertEquals(-150.0,self.accountTransferNet(toAccount))


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

        self.assertEquals(5, len(lines))
        self.assertEquals("composedPortfolio", lines[0])
        self.assertEquals(" complexPortfolio", lines[1])
        self.assertEquals("  account1", lines[2])
        self.assertEquals("  account2", lines[3])
        self.assertEquals(" account3", lines[4])

    def portofolioTreeOf(self, composedPortfolio, accountNames):
        printer = PortfolioTreePrinter (composedPortfolio,accountNames)

        return printer.lines()



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

        self.assertEquals(5, len(lines))
        self.assertEquals(" account3", lines[0])
        self.assertEquals("  account2", lines[1])
        self.assertEquals("  account1", lines[2])
        self.assertEquals(" complexPortfolio", lines[3])
        self.assertEquals("composedPortfolio", lines[4])

    def reversePortofolioTreeOf(self, composedPortfolio, accountNames):
        printer = ReversePortfolioTreePrinter (composedPortfolio,accountNames)

        return printer.lines()

    def test27AccountSummaryWithInvestmentEarningsShouldNotTakeTooLong(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        CertificateOfDeposit.registerFor(1000, 360, 0.1, fromAccount)

        lines = self.shouldNotTakeMoreThan(
            lambda:AccountSummaryWithInvestmentEarnings(fromAccount).lines(),1.1)

        self.assertEquals(5,len(lines))
        self.assertEquals("Deposito por 100", lines[0])
        self.assertEquals("Extraccion por 50", lines[1])
        self.assertEquals("Transferencia por -100", lines[2])
        self.assertEquals("Plazo fijo por 1000 durante 360 dias a una tna de 0.1", lines[3])
        self.assertEquals("Ganancias por 100.0", lines[4])

    def test28AccountSummaryWithInvestmentFullInfoShouldNotTakeTooLong(self):
        fromAccount = ReceptiveAccount ()
        toAccount = ReceptiveAccount ()

        Deposit.registerForOn(100,fromAccount)
        Withdraw.registerForOn(50,fromAccount)
        Transfer.registerFor(100,fromAccount, toAccount)
        CertificateOfDeposit.registerFor(1000, 360, 0.1, fromAccount)

        lines = self.shouldNotTakeMoreThan(
            lambda:AccountSummaryWithAllInvestmentInformation(fromAccount).lines(),1.1)

        self.assertEquals(6,len(lines))
        self.assertEquals("Deposito por 100", lines[0])
        self.assertEquals("Extraccion por 50", lines[1])
        self.assertEquals("Transferencia por -100", lines[2])
        self.assertEquals("Plazo fijo por 1000 durante 360 dias a una tna de 0.1", lines[3])
        self.assertEquals("Ganancias por 100.0", lines[4])
        self.assertEquals("Inversiones por 1000", lines[5])


    def shouldNotTakeMoreThan(self,aLambda,aTimeLimit):
        timeBeforeRunning = time.time()
        result = aLambda()
        timeAfterRunning = time.time()

        self.assertTrue(timeAfterRunning - timeBeforeRunning <= aTimeLimit)
        return result

if __name__ == '__main__':
    unittest.main()
