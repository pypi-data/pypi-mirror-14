#!/usr/bin/env python

# Python module for working with NooLite USB stick (PC118, PC1116, PC1132)

# Latest version at: https://github.com/Sicness/pyNooLite

import warnings

try:
    import usb.core
except:
    raise ImportError(
        "Can't import usb.core. Please install 'pyusb' package " +
        "from PyPI: pip install pyusb --upgrade")


__author__ = "Anton Balashov"
__license__ = "GPL v3"
__maintainer__ = "Anton Balashov"
__email__ = "Sicness@darklogic.ru"


class NooLiteErr(Exception):

    """General NooLite error."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class NooLiteDeviceLookupErr(NooLiteErr):

    """Specific NooLite error indicating that target
    controller device is not found or not connected.
    """


class NooLite:

    """NooLite controller device."""

    _initial_command = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def __init__(
            self, channels=8, idVendor=0x16c0, idProduct=0x05df,
            channals=None, tests=None, **device_kwargs):
        # Channels
        if not isinstance(channels, int):
            raise TypeError("'channels' argument must be of int type")
        self._channels = channels
        # Deprecated 'channals'
        if channals is not None:
            warnings.warn(
                "'channals' argument is deprecated: " +
                    "use 'channels' argument instead",
                DeprecationWarning)
            if not isinstance(channals, int):
                raise TypeError("'channals' argument must be of int type")
            self._channels = channals
        # Number of channels limit
        if self._channels < 1:
            raise ValueError("'channels' argument must be greater than 0")
        # idVendor, idProduct
        if not isinstance(idVendor, int) or not isinstance(idProduct, int):
            raise TypeError(
                "'idVendor' and 'idProduct' arguments must be of int type")
        self._idVendor = idVendor
        self._idProduct = idProduct
        # Device kwargs for usb.core.find()
        self._device_kwargs = device_kwargs
        # Deprecated 'tests' argument
        if tests is not None:
            warnings.warn("'tests' argument is deprecated", DeprecationWarning)

    # Public methods

    def on(self, ch):
        """Turn power ON for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x02)

    def off(self, ch):
        """Turn power OFF for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x00)

    def switch(self, ch):
        """Switch power state between off and on for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x04)

    def set(self, ch, level):
        """Set brightness level for specified channel.
        Level must be between 0 and 120.
        First channel is 0.
        """
        try:
            level = int(level)
        except (TypeError, ValueError):
            raise TypeError(
                "Level value of %s cannot be correctly converted to int"
                % (repr(level)))
        if not (0 <= level <= 120):
            raise NooLiteErr(
                "Level value of %d is not valid: must be 0-120" % (level))
        if level > 0:
            level += 35
        return self._send_command(ch, 0x06, level)

    def save(self, ch):
        """Save current state as a scenario for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x08)

    def load(self, ch):
        """Call saved scenario for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x07)

    def bind(self, ch):
        """Send binding signal for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x0f)

    def unbind(self, ch):
        """Send unbinding signal for specified channel.
        First channel is 0.
        """
        return self._send_command(ch, 0x09)

    # Private methods

    def _send_command(self, ch, action, value=None):
        """Prepare and send NooLite actuation command."""
        cmd = self._get_initial_command()
        self._set_channel(cmd, ch)
        self._set_action(cmd, action, value)
        self._send_data(cmd)
        return 0  # Return 0 to indicate success

    def _get_initial_command(self):
        """Get initial (empty) command."""
        return self._initial_command[:]

    def _set_channel(self, cmd, ch):
        """Set channel number."""
        try:
            ch = int(ch)
        except (TypeError, ValueError):
            raise TypeError(
                "Channel %s cannot be correctly converted to int" % (repr(ch)))
        if not (0 <= ch < self._channels):
            raise NooLiteErr(
                "Channel %d is not valid: only channels 0-%d are supported"
                % (ch, self._channels - 1))
        cmd[4] = ch  # Set channel number

    def _set_action(self, cmd, action, value):
        """Set specific command action and action value (if required)."""
        cmd[1] = action  # Set action type
        if value is not None:
            cmd[2] = 0x01  # Set flag to use single value
            cmd[5] = value  # Set single value

    def _send_data(self, cmd):
        """Send prepared command data to controller device."""
        # Find NooLite USB controller device
        device = usb.core.find(
            idVendor=self._idVendor, idProduct=self._idProduct,
            **self._device_kwargs)
        if device is None:
            raise NooLiteDeviceLookupErr(
                "Can't find controller device with %s"
                % (self._format_device_data()))
        # Detach kernel driver if required
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)
        # Set controller device configuration
        device.set_configuration()
        # Send actual actuation command
        device.ctrl_transfer(0x21, 0x09, 0, 0, cmd)

    def _format_channels_data(self):
        """Format number of channels for string output."""
        return \
            "1 channel" if self._channels == 1 \
            else "%d channels" % (self._channels)

    def _format_device_data(self):
        """Format idVendor, idProduct and device_kwargs for string output."""
        device_data = \
            "idVendor=%d, idProduct=%d" % (self._idVendor, self._idProduct)
        if self._device_kwargs:
            device_data += ", " + ", ".join(
                ["%s=%s" % (k, v) for k, v in self._device_kwargs.items()])
        return device_data

    def __str__(self):
        return "NooLite controller (%s)" % (self._format_channels_data())

    def __repr__(self):
        return \
            "<NooLite controller: %s, %s>" \
            % (self._format_channels_data(), self._format_device_data())
