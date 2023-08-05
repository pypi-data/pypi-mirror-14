import configargparse
import random
import unittest
from datetime import datetime

from pynYNAB import KeyGenerator
from pynYNAB.Entity import AccountTypes
from pynYNAB.budget import Account, Payee
from pynYNAB.Client import clientfromargs
from pynYNAB.budget import Transaction


class commonLive(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(commonLive, self).__init__(*args, **kwargs)
        self.account = None
        self.budget = None
        self.transaction = None
        self.client = None

    def reload(self):
        import pynYNAB.config
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        self.client = clientfromargs(args)

    def setUp(self):
        self.reload()

    def util_add_account(self):
        account = Account(
            account_type=random.choice(list(AccountTypes)),
            account_name=KeyGenerator.generateuuid()
        )

        self.client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
        self.reload()
        self.assertIn(account, self.client.budget.be_accounts)

    def util_add_transaction(self):
        transaction = Transaction(
            amount=1,
            cleared='Uncleared',
            date=datetime.now(),
            entities_account_id=self.account.id,
        )
        self.client.add_transaction(transaction)
        self.reload()
        self.assertIn(transaction, self.client.budget.be_transactions)

    def util_get_empty_account_by_name_if_doesnt_exist(self, name):
        accounts = {a.account_name: a for a in self.client.budget.be_accounts if
                    a.account_name == name}
        if name in accounts:
            account = accounts[name]
            self.client.delete_account(account)

            self.reload()

            self.assertTrue(account not in self.client.budget.be_accounts)

        account = Account(
            account_type=AccountTypes.Checking,
            account_name=name
        )

        self.client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
        self.reload()
        self.assertIn(account, self.client.budget.be_accounts)
        return account

    def util_add_payee_by_name_if_doesnt_exist(self, name):
        payees = {p.name: p for p in self.client.budget.be_payees if
                  p.name == name}
        if name in payees:
            return payees[name]
        payee = Payee(
            name=name
        )

        self.client.budget.be_payees.append(payee)
        self.client.sync()
        self.reload()
        self.assertIn(payee, self.client.budget.be_payees)
        return payee
