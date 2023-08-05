import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import noolite

init_cmd = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


class Tests(unittest.TestCase):
    def test_init_ch_type(self):
        self.assertRaises(
            ValueError, noolite.NooLite, channals="bla", tests=True)

    def test_init_idVendor_type(self):
        self.assertRaises(
            ValueError, noolite.NooLite, idVendor="bla", tests=True)

    def test_init_idProduct_type(self):
        self.assertRaises(
            ValueError, noolite.NooLite, idProduct="bla", tests=True)

    def test_ch_str(self):
        switcher = noolite.NooLite(tests=True)
        cmd = init_cmd
        cmd[4] = 7
        cmd[1] = 0x02
        self.assertEqual(switcher.on("7"), cmd)

    def test_ch_int(self):
        switcher = noolite.NooLite(tests=True)
        cmd = init_cmd
        cmd[4] = 7
        cmd[1] = 0x00
        self.assertEqual(switcher.off(7), cmd)

    def test_ch_negative(self):
        switcher = noolite.NooLite(tests=True)
        self.assertRaises(noolite.NooLiteErr, switcher.on, -1)

    def test_ch_too_big(self):
        switcher = noolite.NooLite(channals=32, tests=True)
        self.assertRaises(noolite.NooLiteErr, switcher.on, 42)

    def test_set(self):
        switcher = noolite.NooLite(tests=True)
        value = 50
        cmd = init_cmd
        cmd[4] = 7
        cmd[2] = 0x01
        cmd[1] = 0x06
        cmd[5] = 35 + value
        self.assertEqual(switcher.set(7, value), cmd)

    def test_set_str(self):
        switcher = noolite.NooLite(tests=True)
        value = "70"
        cmd = init_cmd
        cmd[4] = 7
        cmd[2] = 0x01
        cmd[1] = 0x06
        cmd[5] = 35 + int(value)
        self.assertEqual(switcher.set(7, value), cmd)

    def test_set_zero(self):
        switcher = noolite.NooLite(tests=True)
        value = 0
        cmd = init_cmd
        cmd[4] = 7
        cmd[2] = 0x01
        cmd[1] = 0x06
        cmd[5] = 0
        self.assertEqual(switcher.set(7, value), cmd)

    def test_device_kwargs_used_for_device_finding(self):
        switcher = noolite.NooLite(bus=1, address=12)
        with mock.patch('usb.core.find', return_value=mock.Mock()) \
                as mock_usb_core_find:
            switcher.on(5)
        mock_usb_core_find.assert_called_once_with(
            idVendor=mock.ANY, idProduct=mock.ANY,
            bus=1, address=12)

    def test_NooLiteDeviceLookupErr(self):
        switcher = noolite.NooLite(idVendor=12345, idProduct=54321)
        with mock.patch('usb.core.find', return_value=None):
            with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
                switcher.off(5)
        self.assertIsInstance(err.exception, noolite.NooLiteErr)
        self.assertIn('idVendor=12345', err.exception.value)
        self.assertIn('idProduct=54321', err.exception.value)

    def test_NooLiteDeviceLookupErr_with_device_kwargs(self):
        switcher = noolite.NooLite(
            idVendor=12345, idProduct=54321, bDeviceClass=7, bDeviceProtocol=1)
        with mock.patch('usb.core.find', return_value=None):
            with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
                switcher.off(5)
        self.assertIn('idVendor=12345', err.exception.value)
        self.assertIn('idProduct=54321', err.exception.value)
        self.assertIn('bDeviceClass=7', err.exception.value)
        self.assertIn('bDeviceProtocol=1', err.exception.value)

    def test_NooLiteDeviceLookupErr_with_custom_match_device_kwarg(self):
        switcher = noolite.NooLite(custom_match=lambda dev: dev.bus == 2)
        with mock.patch('usb.core.find', return_value=None):
            with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
                switcher.off(5)
        self.assertIn('custom_match=<function', err.exception.value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
