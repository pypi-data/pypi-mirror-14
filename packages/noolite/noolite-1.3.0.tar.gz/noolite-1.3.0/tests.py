import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import warnings

import noolite


class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctrl_cmd = (0x21, 0x09, 0, 0)
        if not hasattr(cls, 'assertRaisesRegex'):  # Python 2 compatibility
            cls.assertRaisesRegex = cls.assertRaisesRegexp

    def setUp(self):
        self.exp_cmd = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.mock_device = mock.Mock()
        patcher = mock.patch('usb.core.find')
        self.addCleanup(patcher.stop)
        self.mock_usb_core_find = patcher.start()
        self.mock_usb_core_find.return_value = self.mock_device

    # Test initialization

    def test_init_default(self):
        controller = noolite.NooLite()
        self.assertEqual(controller._channels, 8)
        self.assertEqual(controller._idVendor, 0x16c0)
        self.assertEqual(controller._idProduct, 0x05df)
        self.assertEqual(controller._device_kwargs, {})

    def test_init_channel_type(self):
        self.assertRaises(TypeError, noolite.NooLite, channels='blah')

    def test_init_channel_value(self):
        for channels in (-5, -1, 0):
            self.assertRaisesRegex(
                ValueError, "greater than 0",
                noolite.NooLite, channels=channels)

    def test_init_idVendor_type(self):
        self.assertRaises(TypeError, noolite.NooLite, idVendor='blah')

    def test_init_idProduct_type(self):
        self.assertRaises(TypeError, noolite.NooLite, idProduct='blah')

    def test_init_with_device_kwargs(self):
        controller = noolite.NooLite(bus=1, address=21)
        self.assertEqual(controller._device_kwargs, dict(bus=1, address=21))

    def test_init_channals_deprecated(self):
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter('always')
            noolite.NooLite(channals=8)
            self.assertEqual(len(warns), 1)
            self.assertTrue(issubclass(warns[-1].category, DeprecationWarning))
            self.assertIn("deprecated", str(warns[-1].message))

    def test_init_channals_deprecated_but_still_active(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            controller = noolite.NooLite(channals=16)
            self.assertEqual(controller._channels, 16)

    def test_init_channals_deprecated_but_takes_precedence_over_channels(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            controller = noolite.NooLite(channels=16, channals=32)
            self.assertEqual(controller._channels, 32)

    def test_init_tests_deprecated(self):
        for value in (True, False):
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                noolite.NooLite(tests=value)
                self.assertEqual(len(warns), 1)
                self.assertTrue(
                    issubclass(warns[-1].category, DeprecationWarning))
                self.assertIn("deprecated", str(warns[-1].message))

    # Test 'ch' argument for all commands

    def test_ch_int(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 5
        self.exp_cmd[1] = 0x00
        controller.off(5)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_ch_str(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 6
        self.exp_cmd[1] = 0x02
        controller.on("6")
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_ch_negative(self):
        controller = noolite.NooLite()
        self.assertRaisesRegex(
            noolite.NooLiteErr, "-1 is not valid", controller.switch, -1)

    def test_ch_too_big(self):
        controller = noolite.NooLite(channels=32)
        with self.assertRaises(noolite.NooLiteErr) as error:
            controller.save(42)
        self.assertIn("42 is not valid", str(error.exception))
        self.assertIn("0-31", str(error.exception))

    # Test simple commands

    def test_on(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x02
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.on(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_off(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x00
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.off(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_switch(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x04
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.switch(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_set_int_level(self):
        controller = noolite.NooLite()
        value = 50
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x06
        self.exp_cmd[2] = 0x01
        self.exp_cmd[5] = 35 + value
        controller.set(7, value)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_set_str_level(self):
        controller = noolite.NooLite()
        value = "70"
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x06
        self.exp_cmd[2] = 0x01
        self.exp_cmd[5] = 35 + int(value)
        controller.set(7, value)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_set_zero_level(self):
        controller = noolite.NooLite()
        value = 0
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x06
        self.exp_cmd[2] = 0x01
        self.exp_cmd[5] = 0
        controller.set(7, value)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_set_negative_level(self):
        controller = noolite.NooLite()
        self.assertRaisesRegex(
            noolite.NooLiteErr, "-1 is not valid: .* 0-120",
            controller.set, 7, -1)

    def test_set_excessive_level(self):
        controller = noolite.NooLite()
        self.assertRaisesRegex(
            noolite.NooLiteErr, "121 is not valid: .* 0-120",
            controller.set, 7, 121)

    def test_save(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x08
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.save(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_load(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x07
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.load(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_bind(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x0f
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.bind(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    def test_unbind(self):
        controller = noolite.NooLite()
        self.exp_cmd[4] = 7
        self.exp_cmd[1] = 0x09
        self.exp_cmd[2] = 0x00
        self.exp_cmd[5] = 0x00
        controller.unbind(7)
        self.mock_device.ctrl_transfer.assert_called_once_with(
            mock.ANY, mock.ANY, mock.ANY, mock.ANY, self.exp_cmd)

    # Test multiple calls

    def test_simple_cmds_reset_format_and_data_bytes_after_set_cmd_call(self):
        controller = noolite.NooLite()
        level = 67
        for method in (
                'on', 'off', 'switch', 'save', 'load', 'bind', 'unbind'):
            # Call set method
            controller.set(7, level)
            act_cmd = self.mock_device.ctrl_transfer.call_args[0][-1]
            self.assertEqual(act_cmd[1], 0x06)  # Command
            self.assertEqual(act_cmd[2], 0x01)  # Format
            self.assertEqual(act_cmd[5], 35 + level)  # Level
            act_cmd = self.mock_device.ctrl_transfer.reset_mock()
            # Call non-set method
            getattr(controller, method)(7)
            act_cmd = self.mock_device.ctrl_transfer.call_args[0][-1]
            self.assertNotEqual(act_cmd[1], 0x06)  # Command
            self.assertEqual(act_cmd[2], 0x00)  # Format
            self.assertEqual(act_cmd[5], 0x00)  # Level
            act_cmd = self.mock_device.ctrl_transfer.reset_mock()

    # Test all commands returning 0 to indicate success

    def test_commands_return_zero_to_indicate_success(self):
        controller = noolite.NooLite()
        for method in (
                'on', 'off', 'switch', 'set',
                'save', 'load', 'bind', 'unbind'):
            if method == 'set':
                return_value = getattr(controller, method)(7, 42)
            else:
                return_value = getattr(controller, method)(7)
            self.assertEqual(return_value, 0)

    # Test controller device search

    def test_idVendor_and_idProduct_used_for_device_search(self):
        controller = noolite.NooLite(idVendor=12345, idProduct=54321)
        controller.on(4)
        self.mock_usb_core_find.assert_called_once_with(
            idVendor=12345, idProduct=54321)

    def test_device_kwargs_used_for_device_search(self):
        controller = noolite.NooLite(bus=1, address=12)
        controller.on(5)
        self.mock_usb_core_find.assert_called_once_with(
            idVendor=mock.ANY, idProduct=mock.ANY,
            bus=1, address=12)

    def test_NooLiteDeviceLookupErr(self):
        controller = noolite.NooLite(idVendor=12345, idProduct=54321)
        self.mock_usb_core_find.return_value = None
        with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
            controller.off(5)
        self.assertIsInstance(err.exception, noolite.NooLiteErr)
        self.assertIn('idVendor=12345', err.exception.value)
        self.assertIn('idProduct=54321', err.exception.value)

    def test_NooLiteDeviceLookupErr_with_device_kwargs(self):
        controller = noolite.NooLite(
            idVendor=12345, idProduct=54321,
            bDeviceClass=7, bDeviceProtocol=1)
        self.mock_usb_core_find.return_value = None
        with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
            controller.off(5)
        self.assertIn('idVendor=12345', err.exception.value)
        self.assertIn('idProduct=54321', err.exception.value)
        self.assertIn('bDeviceClass=7', err.exception.value)
        self.assertIn('bDeviceProtocol=1', err.exception.value)

    def test_NooLiteDeviceLookupErr_with_custom_match_device_kwarg(self):
        controller = noolite.NooLite(custom_match=lambda dev: dev.bus == 2)
        self.mock_usb_core_find.return_value = None
        with self.assertRaises(noolite.NooLiteDeviceLookupErr) as err:
            controller.off(5)
        self.assertIn('custom_match=<function', err.exception.value)

    # Test kernel driver detaching

    def test_kernel_driver_is_detached_if_active(self):
        controller = noolite.NooLite()
        self.mock_device.is_kernel_driver_active.return_value = True
        controller.switch(4)
        self.mock_device.detach_kernel_driver.assert_called_once_with(0)

    def test_kernel_driver_is_not_explicitly_detached_if_not_active(self):
        controller = noolite.NooLite()
        self.mock_device.is_kernel_driver_active.return_value = False
        controller.switch(4)
        self.assertFalse(self.mock_device.detach_kernel_driver.called)

    # Test set configuration for controller device

    def test_set_configuration_is_called(self):
        controller = noolite.NooLite()
        controller.bind(3)
        self.mock_device.set_configuration.assert_called_once_with()

    # Test NooLite instance str and repr

    def test_string_representation(self):
        controller = noolite.NooLite(
            channels=1, idVendor=12345, idProduct=54321,
            bDeviceClass=7, bDeviceProtocol=1)
        string_representation = str(controller)
        self.assertIn("NooLite", string_representation)
        self.assertIn("1 channel", string_representation)
        self.assertNotIn("idVendor", string_representation)
        self.assertNotIn("idProduct", string_representation)
        self.assertNotIn("bDeviceClass", string_representation)
        self.assertNotIn("bDeviceProtocol", string_representation)

    def test_internal_representation(self):
        controller = noolite.NooLite(
            channels=16, idVendor=12345, idProduct=54321,
            bDeviceClass=7, bDeviceProtocol=1)
        string_representation = repr(controller)
        self.assertIn("NooLite", string_representation)
        self.assertIn("16 channels", string_representation)
        self.assertIn("idVendor=12345", string_representation)
        self.assertIn("idProduct=54321", string_representation)
        self.assertIn("bDeviceClass=7", string_representation)
        self.assertIn("bDeviceProtocol=1", string_representation)


if __name__ == '__main__':
    unittest.main(verbosity=2)
