#-----------------------------------------------------------------------------
"""
GPIO Commands

This code is the generic front end for GPIO operations.
The vendor specific flash drivers are within the vendor directories.
Those drivers expose a common API used by this code.
"""
#-----------------------------------------------------------------------------

import util

#-----------------------------------------------------------------------------

_help_gpio = (
    ('[name]', 'gpio name (see "gpio info")'),
)

_invalid_gpio_name = 'invalid gpio name (see "gpio info")'

#-----------------------------------------------------------------------------

class gpio(object):

  def __init__(self, driver):
    self.driver = driver
    self.menu = (
      ('clr', self.cmd_clr, _help_gpio),
      ('init', self.driver.cmd_init),
      ('set', self.cmd_set, _help_gpio),
      ('status', self.cmd_status),
    )

  def cmd_clr(self, ui, args):
    """clear gpio (0)"""
    if util.wrong_argc(ui, args, (1,)):
      return None
    x = self.driver.name_arg(args[0])
    if x is None:
      ui.put(_invalid_gpio_name)
      return
    self.driver.clr_bit(x[0], x[1])

  def cmd_set(self, ui, args):
    """set gpio (1)"""
    if util.wrong_argc(ui, args, (1,)):
      return None
    x = self.driver.name_arg(args[0])
    if x is None:
      ui.put(_invalid_gpio_name)
      return
    self.driver.set_bit(x[0], x[1])

  def cmd_status(self, ui, args):
    """display gpio status"""
    ui.put('%s\n' % self.driver)

#-----------------------------------------------------------------------------
