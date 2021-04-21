import unittest
import time
from unittest import mock
from phone import Phone, bluetooth, State



class test_phone(unittest.TestCase):

    def setUp(self):
        self.bluetooth_address = "AA:BB:CC:DD:EE:FF"
        self.sut = Phone("tester", bluetooth_address="AA:BB:CC:DD:EE:FF")

    def phonePresent(self):
        return  [{'service-classes': ['1801'],
                                        'profiles': [],
                                        'name': None,
                                        'description': None,
                                        'provider': None,
                                        'service-id': None,
                                        'protocol': 'L2CAP',
                                        'port': 31,
                                        'host': 'AA:BB:CC:DD:EE:FF'},
                                        {'service-classes': ['1800'],
                                        'profiles': [],
                                        'name': None,
                                        'description': None,
                                        'provider': None,
                                        'service-id': None,
                                        'protocol': 'L2CAP',
                                        'port': 31,
                                        'host': 'AA:BB:CC:DD:EE:FF'}]

    def test_isHome(self):
        bluetooth.find_service = mock.MagicMock(return_value=self.phonePresent())
        self.assertTrue(self.sut.__isHome__())
        bluetooth.find_service.assert_called_with(address=self.bluetooth_address)

        bluetooth.find_service = mock.MagicMock(return_value=[])
        self.assertFalse(self.sut.__isHome__())
        bluetooth.find_service.assert_called_with(address=self.bluetooth_address)

    def stateChanged(self):
        print("Came home!")
        if self.sut.state == State.HOME:
            self.home = True
        else:
            self.home = False

    #@patch('time.sleep', return_value=None)
    def test_phoneComesHome(self):
        self.home = False

        bluetooth.find_service = mock.MagicMock(return_value=[])
        time.sleep = mock.Mock(return_value=None)

        self.sut.addCBStateChanged(self.stateChanged)

        self.sut.startTracing()
        while time.sleep.call_count < 5:
            print("Waiting...")

        self.assertFalse(self.home)
        bluetooth.find_service = mock.MagicMock(return_value=self.phonePresent())
        call_count_now = time.sleep.call_count
        while time.sleep.call_count < 5 + call_count_now:
            print("Waiting...")
        self.sut.stopTracing()
        self.assertTrue(self.home)





if __name__ == '__main__':
    unittest.main()