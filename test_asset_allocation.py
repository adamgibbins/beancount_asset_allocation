#!/usr/bin/env python3

from beancount.utils import test_utils
import asset_allocation

class TestScriptCheck(test_utils.TestCase):

    @test_utils.docfile
    def test_basic_unspecified(self, filename):
        """
        2010-01-01 open Assets:Investments:Brokerage
        2010-01-01 open Assets:Bank

        2011-03-02 * "Buy stock"
         Assets:Investments:Brokerage 1 BNCT {200 USD}
         Assets:Bank

        2011-03-02 price BNCT 200 USD
        """
        with test_utils.capture('stdout', 'stderr') as (stdout, _):
            result = test_utils.run_with_args(asset_allocation.main, [filename])
        self.assertEqual(0, result)
        self.assertRegex(stdout.getvalue(), "unknown *100.0% *200 *")
        # self.assertLines("", stdout.getvalue())


    @test_utils.docfile
    def test_basic_specified(self, filename):
        """
        2010-01-01 open Assets:Investments:Brokerage
        2010-01-01 open Assets:Bank
        2010-01-01 commodity BNCT
         asset_allocation_equity: 60
         asset_allocation_bond: 40

        2011-03-02 * "Buy stock"
         Assets:Investments:Brokerage 1 BNCT {200 USD}
         Assets:Bank

        2011-03-02 price BNCT 200 USD
        """
        with test_utils.capture('stdout', 'stderr') as (stdout, _):
            result = test_utils.run_with_args(asset_allocation.main, [filename])
        self.assertEqual(0, result)
        self.assertRegex(stdout.getvalue(), "equity *60.0% *120 *")
        self.assertRegex(stdout.getvalue(), "bond *40.0% *80")


    @test_utils.docfile
    def test_basic_account_filter(self, filename):
        """
        2010-01-01 open Assets:Investments:Brokerage
        2010-01-01 open Assets:Investments:XTrade
        2010-01-01 open Assets:Bank
        2010-01-01 commodity BNCT
         asset_allocation_equity: 60
         asset_allocation_bond: 40

        2011-03-02 * "Buy stock"
         Assets:Investments:Brokerage 1 BNCT {200 USD}
         Assets:Bank

        2011-01-02 * "Buy stock"
         Assets:Investments:XTrade 2 BNCT {200 USD}
         Assets:Bank

        2011-03-02 price BNCT 200 USD
        """
        with test_utils.capture('stdout', 'stderr') as (stdout, _):
            result = test_utils.run_with_args(asset_allocation.main, [filename,
                '--accounts', 'Assets:Investments:Brokerage'])
        self.assertEqual(0, result)
        self.assertRegex(stdout.getvalue(), "equity *60.0% *120 *")
        self.assertRegex(stdout.getvalue(), "bond *40.0% *80")


    @test_utils.docfile
    def test_basic_filter_exclude_parent(self, filename):
        """
        2010-01-01 open Assets:Investments:Brokerage
        2010-01-01 open Assets:Investments:XTrade
        2010-01-01 open Assets:Bank
        2010-01-01 commodity BNCT
         asset_allocation_equity: 60
         asset_allocation_bond: 40

        2011-03-02 * "Buy stock"
         Assets:Investments:Brokerage 1 BNCT {200 USD}
         Assets:Bank

        2011-01-02 * "Buy stock"
         Assets:Investments:XTrade 2 BNCT {200 USD}
         Assets:Bank

        2011-01-02 * "Buy stock"
         Assets:Investments 7 BNCT {200 USD}
         Assets:Bank

        2011-03-02 price BNCT 200 USD
        """
        with test_utils.capture('stdout', 'stderr') as (stdout, _):
            result = test_utils.run_with_args(asset_allocation.main, [filename,
                '--accounts', 'Assets:Investments:Brokerage'])
        self.assertEqual(0, result)
        self.assertRegex(stdout.getvalue(), "equity *60.0% *120 *")
        self.assertRegex(stdout.getvalue(), "bond *40.0% *80")
