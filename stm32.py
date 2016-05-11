#-----------------------------------------------------------------------------
"""

SoC file for stm32 devices

"""
#-----------------------------------------------------------------------------

import cortexm
import util
from util import fld, fld_set
from regs import reg32, reg16, reg8, regset, memio

#-----------------------------------------------------------------------------
# Flash

r = []
r.append(reg32('ACR', 0x00))
r.append(reg32('KEYR', 0x04))
r.append(reg32('OPTKEYR', 0x08))
r.append(reg32('SR', 0x0C))
r.append(reg32('CR', 0x10))
r.append(reg32('AR',0x14))
r.append(reg32('OBR', 0x1C))
r.append(reg32('WRPR', 0x20))
flash_regs = regset('Flash', r)

#-----------------------------------------------------------------------------
# GPIO

r = []
r.append(reg32('MODER', 0x00))
r.append(reg32('OTYPER', 0x04))
r.append(reg32('OSPEEDR', 0x08))
r.append(reg32('PUPDR', 0x0C))
r.append(reg32('IDR', 0x10))
r.append(reg32('ODR', 0x14))
r.append(reg32('BSRR', 0x18))
r.append(reg32('LCKR', 0x1C))
r.append(reg32('AFRL', 0x20))
r.append(reg32('AFRH', 0x24))
r.append(reg32('BRR', 0x28))
gpio_regs = regset('GPIO', r)

# TODO some sort of per platform selection for gpio info
def gpio_n(n):
  """return (name, base) for gpio[n]"""
  if n >= 6:
    return None
  name = ('A','B','C','D','E','F')[n]
  base = 0x48000000  + (0x400 * n)
  return (name, base)

#-----------------------------------------------------------------------------
# STM32F3 devices

# Vector Tables
# irq_number : name

# STM32F303xB/C/D/E, STM32F358xC and STM32F398xE
vtable0 = {
  0: 'WWDG',
  1: 'PVD',
  2: 'TAMPER_STAMP',
  3: 'RTC_WKUP',
  4: 'FLASH',
  5: 'RCC',
  6: 'EXTI0',
  7: 'EXTI1',
  8: 'EXTI2_TS',
  9: 'EXTI3',
  10: 'EXTI4',
  11: 'DMA1_Channel1',
  12: 'DMA1_Channel2',
  13: 'DMA1_Channel3',
  14: 'DMA1_Channel4',
  15: 'DMA1_Channel5',
  16: 'DMA1_Channel6',
  17: 'DMA1_Channel7',
  18: 'ADC1_2',
  19: 'USB_HP/CAN_TX',
  20: 'USB_LP/CAN_RX0',
  21: 'CAN_RX1',
  22: 'CAN_SCE',
  23: 'EXTI9_5',
  24: 'TIM1_BRK/TIM15',
  25: 'TIM1_UP/TIM16',
  26: 'TIM1_TRG_COM/TIM17',
  27: 'TIM1_CC',
  28: 'TIM2',
  29: 'TIM3',
  30: 'TIM4',
  31: 'I2C1_EV',
  32: 'I2C1_ER',
  33: 'I2C2_EV',
  34: 'I2C2_ER',
  35: 'SPI1',
  36: 'SPI2',
  37: 'USART1',
  38: 'USART2',
  39: 'USART3',
  40: 'EXTI15_10',
  41: 'RTC_Alarm',
  42: 'USBWakeUp',
  43: 'TIM8_BRK',
  44: 'TIM8_UP',
  45: 'TIM8_TRG_COM',
  46: 'TIM8_CC',
  47: 'ADC3',
  48: 'FMC',
  51: 'SPI3',
  52: 'UART4',
  53: 'UART5',
  54: 'TIM6_DAC',
  55: 'TIM7',
  56: 'DMA2_Channel1',
  57: 'DMA2_Channel2',
  58: 'DMA2_Channel3',
  59: 'DMA2_Channel4',
  60: 'DMA2_Channel5',
  61: 'ADC4',
  64: 'COMP1_2_3',
  65: 'COMP4_5_6',
  66: 'COMP7',
  72: 'I2C3_EV',
  73: 'I2C3_ER',
  74: 'USB_HP',
  75: 'USB_LP',
  76: 'USB_WakeUp_RMP',
  77: 'TIM20_BRK',
  78: 'TIM20_UP',
  79: 'TIM20_TRG_COM',
  80: 'TIM20_CC',
  81: 'FPU',
  84: 'SPI4',
}

# STM32F303x6/8and STM32F328x8
vtable1 = {
  0: 'WWDG',
  1: 'PVD',
  2: 'TAMPER_STAMP',
  3: 'RTC_WKUP',
  4: 'FLASH',
  5: 'RCC',
  6: 'EXTI0',
  7: 'EXTI1',
  8: 'EXTI2_TS',
  9: 'EXTI3',
  10: 'EXTI4',
  11: 'DMA1_Channel1',
  12: 'DMA1_Channel2',
  13: 'DMA1_Channel3',
  14: 'DMA1_Channel4',
  15: 'DMA1_Channel5',
  16: 'DMA1_Channel6',
  17: 'DMA1_Channel7',
  18: 'ADC1_2',
  19: 'CAN_TX',
  20: 'CAN_RX0',
  21: 'CAN_RX1',
  22: 'CAN_SCE',
  23: 'EXTI9_5',
  24: 'TIM1_BRK/TIM15',
  25: 'TIM1_UP/TIM16',
  26: 'TIM1_TRG_COM/TIM17',
  27: 'TIM1_CC',
  28: 'TIM2',
  29: 'TIM3',
  31: 'I2C1_EV',
  32: 'I2C1_ER',
  35: 'SPI1',
  37: 'USART1',
  38: 'USART2',
  39: 'USART3',
  40: 'EXTI15_10',
  41: 'RTC_Alarm',
  54: 'TIM6_DAC1',
  55: 'TIM7_DAC2',
  64: 'COMP2',
  65: 'COMP4_6',
  81: 'FPU',
}

# Memory Maps
# name: (base address, size in bytes)

# STM32F303xB/C and STM32F358xC
memmap0 = {
  'Flash interface': (0x40022000, 1 * KiB),
  'GPIOA': (0x48000000, 1 * KiB),
  'GPIOB': (0x48000400, 1 * KiB),
  'GPIOC': (0x48000800, 1 * KiB),
  'GPIOD': (0x48000c00, 1 * KiB),
  'GPIOE': (0x48001000, 1 * KiB),
  'GPIOF': (0x48001400, 1 * KiB),
}

STM32F303xB_info = {
  'name': 'STM32F303xB',
  'memmap': memmap0,
}
STM32F303xC_info = {
  'name': 'STM32F303xC',
  'cpu_type': 'cortex-m4',
  'priority_bits': 4,
  'vtable': vtable0,
  'memmap': memmap0,
}
STM32F358xC_info = {
  'name': 'STM32F358xC',
  'memmap': memmap0,
}
STM32F303xD_info = {
}
STM32F303xE_info = {
}
STM32F398xE_info = {
}
STM32F303x6_info = {
}
STM32F303x8_info = {
}
STM32F328x8_info = {
}

#-----------------------------------------------------------------------------

soc_db = {}

def db_insert(info):
  soc_db[info['name']] = info

def lookup(name):
  if soc_db.has_key(name):
    return soc_db[name]
  assert False, 'unknown SoC device %s' % device

db_insert(STM32F303xB_info)
db_insert(STM32F303xC_info)
db_insert(STM32F358xC_info)
db_insert(STM32F303xD_info)
db_insert(STM32F303xE_info)
db_insert(STM32F398xE_info)
db_insert(STM32F303x6_info)
db_insert(STM32F303x8_info)
db_insert(STM32F328x8_info)

#-----------------------------------------------------------------------------

gpio_help = (
  ('<cr>', 'display all gpios'),
  ('[n]', 'display gpio[n]'),
)

class soc(object):
  """stm32 SoC"""

  def __init__(self, cpu, info):
    self.cpu = cpu
    self.info = info
    self.menu = (
      ('exceptions', 'show exception status', self.cmd_exceptions),
      ('gpio', 'gpio registers', self.cmd_gpio, gpio_help)
    )
    self.exceptions = cortexm.build_exceptions(info['vector_table'])

  def cmd_exceptions(self, ui, args):
    """display the exceptions table"""
    ui.put('%s\n' % cortexm.exceptions_str(self.cpu, self))

  def cmd_gpio(self, ui, args):
    """display gpio registers"""
    num_gpios = 6
    # default is to display all gpios
    gpio_set = list(range(num_gpios))
    if util.wrong_argc(ui, args, (0,1,)):
      return
    if len(args) == 1:
      n = util.int_arg(ui, args[0], (0, num_gpios - 1), 10)
      if n is None:
        return
      gpio_set = (n,)
    # display the gpio registers
    s = []
    for n in gpio_set:
      x = gpio_n(n)
      if x is None:
        break
      (name, base) = x
      s.append('GPIO%s\n%s\n' % (name, gpio_regs.emit(self.cpu, base)))
    ui.put('\n'.join(s))

#-----------------------------------------------------------------------------
