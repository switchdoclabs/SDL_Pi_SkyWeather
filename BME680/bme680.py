# pimori
# modified by SwitchDoc Labs
"""BME680 Temperature, Pressure, Humidity & Gas Sensor."""
#from constants import lookupTable1, lookupTable2
#from constants import BME680Data
#import constants
import math
import time

__version__ = '1.0.5'

"""BME680 constants, structures and utilities."""

# BME680 General config
POLL_PERIOD_MS = 10

# BME680 I2C addresses
I2C_ADDR_PRIMARY = 0x76
I2C_ADDR_SECONDARY = 0x77

# BME680 unique chip identifier
CHIP_ID = 0x61

# BME680 coefficients related defines
COEFF_SIZE = 41
COEFF_ADDR1_LEN = 25
COEFF_ADDR2_LEN = 16

# BME680 field_x related defines
FIELD_LENGTH = 15
FIELD_ADDR_OFFSET = 17

# Soft reset command
SOFT_RESET_CMD = 0xb6

# Error code definitions
OK = 0
# Errors
E_NULL_PTR = -1
E_COM_FAIL = -2
E_DEV_NOT_FOUND = -3
E_INVALID_LENGTH = -4

# Warnings
W_DEFINE_PWR_MODE = 1
W_NO_NEW_DATA = 2

# Info's
I_MIN_CORRECTION = 1
I_MAX_CORRECTION = 2

# Register map
# Other coefficient's address
ADDR_RES_HEAT_VAL_ADDR = 0x00
ADDR_RES_HEAT_RANGE_ADDR = 0x02
ADDR_RANGE_SW_ERR_ADDR = 0x04
ADDR_SENS_CONF_START = 0x5A
ADDR_GAS_CONF_START = 0x64

# Field settings
FIELD0_ADDR = 0x1d

# Heater settings
RES_HEAT0_ADDR = 0x5a
GAS_WAIT0_ADDR = 0x64

# Sensor configuration registers
CONF_HEAT_CTRL_ADDR = 0x70
CONF_ODR_RUN_GAS_NBC_ADDR = 0x71
CONF_OS_H_ADDR = 0x72
MEM_PAGE_ADDR = 0xf3
CONF_T_P_MODE_ADDR = 0x74
CONF_ODR_FILT_ADDR = 0x75

# Coefficient's address
COEFF_ADDR1 = 0x89
COEFF_ADDR2 = 0xe1

# Chip identifier
CHIP_ID_ADDR = 0xd0

# Soft reset register
SOFT_RESET_ADDR = 0xe0

# Heater control settings
ENABLE_HEATER = 0x00
DISABLE_HEATER = 0x08

# Gas measurement settings
DISABLE_GAS_MEAS = 0x00
ENABLE_GAS_MEAS = 0x01

# Over-sampling settings
OS_NONE = 0
OS_1X = 1
OS_2X = 2
OS_4X = 3
OS_8X = 4
OS_16X = 5

# IIR filter settings
FILTER_SIZE_0 = 0
FILTER_SIZE_1 = 1
FILTER_SIZE_3 = 2
FILTER_SIZE_7 = 3
FILTER_SIZE_15 = 4
FILTER_SIZE_31 = 5
FILTER_SIZE_63 = 6
FILTER_SIZE_127 = 7

# Power mode settings
SLEEP_MODE = 0
FORCED_MODE = 1

# Delay related macro declaration
RESET_PERIOD = 10

# SPI memory page settings
MEM_PAGE0 = 0x10
MEM_PAGE1 = 0x00

# Ambient humidity shift value for compensation
HUM_REG_SHIFT_VAL = 4

# Run gas enable and disable settings
RUN_GAS_DISABLE = 0
RUN_GAS_ENABLE = 1

# Buffer length macro declaration
TMP_BUFFER_LENGTH = 40
REG_BUFFER_LENGTH = 6
FIELD_DATA_LENGTH = 3
GAS_REG_BUF_LENGTH = 20
GAS_HEATER_PROF_LEN_MAX = 10

# Settings selector
OST_SEL = 1
OSP_SEL = 2
OSH_SEL = 4
GAS_MEAS_SEL = 8
FILTER_SEL = 16
HCNTRL_SEL = 32
RUN_GAS_SEL = 64
NBCONV_SEL = 128
GAS_SENSOR_SEL = GAS_MEAS_SEL | RUN_GAS_SEL | NBCONV_SEL

# Number of conversion settings
NBCONV_MIN = 0
NBCONV_MAX = 9  # Was 10, but there are only 10 settings: 0 1 2 ... 8 9

# Mask definitions
GAS_MEAS_MSK = 0x30
NBCONV_MSK = 0X0F
FILTER_MSK = 0X1C
OST_MSK = 0XE0
OSP_MSK = 0X1C
OSH_MSK = 0X07
HCTRL_MSK = 0x08
RUN_GAS_MSK = 0x10
MODE_MSK = 0x03
RHRANGE_MSK = 0x30
RSERROR_MSK = 0xf0
NEW_DATA_MSK = 0x80
GAS_INDEX_MSK = 0x0f
GAS_RANGE_MSK = 0x0f
GASM_VALID_MSK = 0x20
HEAT_STAB_MSK = 0x10
MEM_PAGE_MSK = 0x10
SPI_RD_MSK = 0x80
SPI_WR_MSK = 0x7f
BIT_H1_DATA_MSK = 0x0F

# Bit position definitions for sensor settings
GAS_MEAS_POS = 4
FILTER_POS = 2
OST_POS = 5
OSP_POS = 2
OSH_POS = 0
RUN_GAS_POS = 4
MODE_POS = 0
NBCONV_POS = 0

# Array Index to Field data mapping for Calibration Data
T2_LSB_REG = 1
T2_MSB_REG = 2
T3_REG = 3
P1_LSB_REG = 5
P1_MSB_REG = 6
P2_LSB_REG = 7
P2_MSB_REG = 8
P3_REG = 9
P4_LSB_REG = 11
P4_MSB_REG = 12
P5_LSB_REG = 13
P5_MSB_REG = 14
P7_REG = 15
P6_REG = 16
P8_LSB_REG = 19
P8_MSB_REG = 20
P9_LSB_REG = 21
P9_MSB_REG = 22
P10_REG = 23
H2_MSB_REG = 25
H2_LSB_REG = 26
H1_LSB_REG = 26
H1_MSB_REG = 27
H3_REG = 28
H4_REG = 29
H5_REG = 30
H6_REG = 31
H7_REG = 32
T1_LSB_REG = 33
T1_MSB_REG = 34
GH2_LSB_REG = 35
GH2_MSB_REG = 36
GH1_REG = 37
GH3_REG = 38

# BME680 register buffer index settings
REG_FILTER_INDEX = 5
REG_TEMP_INDEX = 4
REG_PRES_INDEX = 4
REG_HUM_INDEX = 2
REG_NBCONV_INDEX = 1
REG_RUN_GAS_INDEX = 1
REG_HCTRL_INDEX = 0

# Look up tables for the possible gas range values
lookupTable1 = [2147483647, 2147483647, 2147483647, 2147483647,
                2147483647, 2126008810, 2147483647, 2130303777, 2147483647,
                2147483647, 2143188679, 2136746228, 2147483647, 2126008810,
                2147483647, 2147483647]

lookupTable2 = [4096000000, 2048000000, 1024000000, 512000000,
                255744255, 127110228, 64000000, 32258064,
                16016016, 8000000, 4000000, 2000000,
                1000000, 500000, 250000, 125000]


def bytes_to_word(msb, lsb, bits=16, signed=False):
    """Convert a most and least significant byte into a word."""
    # TODO: Reimpliment with struct
    word = (msb << 8) | lsb
    if signed:
        word = twos_comp(word, bits)
    return word


def twos_comp(val, bits=16):
    """Convert two bytes into a two's compliment signed word."""
    # TODO: Reimpliment with struct
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val


class FieldData:
    """Structure for storing BME680 sensor data."""

    def __init__(self):  # noqa D107
        # Contains new_data, gasm_valid & heat_stab
        self.status = None
        self.heat_stable = False
        # The index of the heater profile used
        self.gas_index = None
        # Measurement index to track order
        self.meas_index = None
        # Temperature in degree celsius x100
        self.temperature = None
        # Pressure in Pascal
        self.pressure = None
        # Humidity in % relative humidity x1000
        self.humidity = None
        # Gas resistance in Ohms
        self.gas_resistance = None


class CalibrationData:
    """Structure for storing BME680 calibration data."""

    def __init__(self):  # noqa D107
        self.par_h1 = None
        self.par_h2 = None
        self.par_h3 = None
        self.par_h4 = None
        self.par_h5 = None
        self.par_h6 = None
        self.par_h7 = None
        self.par_gh1 = None
        self.par_gh2 = None
        self.par_gh3 = None
        self.par_t1 = None
        self.par_t2 = None
        self.par_t3 = None
        self.par_p1 = None
        self.par_p2 = None
        self.par_p3 = None
        self.par_p4 = None
        self.par_p5 = None
        self.par_p6 = None
        self.par_p7 = None
        self.par_p8 = None
        self.par_p9 = None
        self.par_p10 = None
        # Variable to store t_fine size
        self.t_fine = None
        # Variable to store heater resistance range
        self.res_heat_range = None
        # Variable to store heater resistance value
        self.res_heat_val = None
        # Variable to store error range
        self.range_sw_err = None

    def set_from_array(self, calibration):
        """Set paramaters from an array of bytes."""
        # Temperature related coefficients
        self.par_t1 = bytes_to_word(calibration[T1_MSB_REG], calibration[T1_LSB_REG])
        self.par_t2 = bytes_to_word(calibration[T2_MSB_REG], calibration[T2_LSB_REG], bits=16, signed=True)
        self.par_t3 = twos_comp(calibration[T3_REG], bits=8)

        # Pressure related coefficients
        self.par_p1 = bytes_to_word(calibration[P1_MSB_REG], calibration[P1_LSB_REG])
        self.par_p2 = bytes_to_word(calibration[P2_MSB_REG], calibration[P2_LSB_REG], bits=16, signed=True)
        self.par_p3 = twos_comp(calibration[P3_REG], bits=8)
        self.par_p4 = bytes_to_word(calibration[P4_MSB_REG], calibration[P4_LSB_REG], bits=16, signed=True)
        self.par_p5 = bytes_to_word(calibration[P5_MSB_REG], calibration[P5_LSB_REG], bits=16, signed=True)
        self.par_p6 = twos_comp(calibration[P6_REG], bits=8)
        self.par_p7 = twos_comp(calibration[P7_REG], bits=8)
        self.par_p8 = bytes_to_word(calibration[P8_MSB_REG], calibration[P8_LSB_REG], bits=16, signed=True)
        self.par_p9 = bytes_to_word(calibration[P9_MSB_REG], calibration[P9_LSB_REG], bits=16, signed=True)
        self.par_p10 = calibration[P10_REG]

        # Humidity related coefficients
        self.par_h1 = (calibration[H1_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H1_LSB_REG] & BIT_H1_DATA_MSK)
        self.par_h2 = (calibration[H2_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H2_LSB_REG] >> HUM_REG_SHIFT_VAL)
        self.par_h3 = twos_comp(calibration[H3_REG], bits=8)
        self.par_h4 = twos_comp(calibration[H4_REG], bits=8)
        self.par_h5 = twos_comp(calibration[H5_REG], bits=8)
        self.par_h6 = calibration[H6_REG]
        self.par_h7 = twos_comp(calibration[H7_REG], bits=8)

        # Gas heater related coefficients
        self.par_gh1 = twos_comp(calibration[GH1_REG], bits=8)
        self.par_gh2 = bytes_to_word(calibration[GH2_MSB_REG], calibration[GH2_LSB_REG], bits=16, signed=True)
        self.par_gh3 = twos_comp(calibration[GH3_REG], bits=8)

    def set_other(self, heat_range, heat_value, sw_error):
        """Set other values."""
        self.res_heat_range = (heat_range & RHRANGE_MSK) // 16
        self.res_heat_val = heat_value
        self.range_sw_err = (sw_error & RSERROR_MSK) // 16


class TPHSettings:
    """Structure for storing BME680 sensor settings.

    Comprises of output data rate, over-sampling and filter settings.

    """

    def __init__(self):  # noqa D107
        # Humidity oversampling
        self.os_hum = None
        # Temperature oversampling
        self.os_temp = None
        # Pressure oversampling
        self.os_pres = None
        # Filter coefficient
        self.filter = None


class GasSettings:
    """Structure for storing BME680 gas settings and status."""

    def __init__(self):  # noqa D107
        # Variable to store nb conversion
        self.nb_conv = None
        # Variable to store heater control
        self.heatr_ctrl = None
        # Run gas enable value
        self.run_gas = None
        # Pointer to store heater temperature
        self.heatr_temp = None
        # Pointer to store duration profile
        self.heatr_dur = None


class BME680Data:
    """Structure to represent BME680 device."""

    def __init__(self):  # noqa D107
        # Chip Id
        self.chip_id = None
        # Device Id
        self.dev_id = None
        # SPI/I2C interface
        self.intf = None
        # Memory page used
        self.mem_page = None
        # Ambient temperature in Degree C
        self.ambient_temperature = None
        # Field Data
        self.data = FieldData()
        # Sensor calibration data
        self.calibration_data = CalibrationData()
        # Sensor settings
        self.tph_settings = TPHSettings()
        # Gas Sensor settings
        self.gas_settings = GasSettings()
        # Sensor power modes
        self.power_mode = None
        # New sensor fields
        self.new_fields = None

class BME680(BME680Data):
    """BOSCH BME680.

    Gas, pressure, temperature and humidity sensor.

    :param i2c_addr: One of I2C_ADDR_PRIMARY (0x76) or I2C_ADDR_SECONDARY (0x77)
    :param i2c_device: Optional smbus or compatible instance for facilitating i2c communications.

    """


    def __init__(self, i2c_addr=I2C_ADDR_PRIMARY, i2c_device=None):
        """Initialise BME680 sensor instance and verify device presence.

        :param i2c_addr: i2c address of BME680
        :param i2c_device: Optional SMBus-compatible instance for i2c transport

        """
        BME680Data.__init__(self)

        self.i2c_addr = i2c_addr
        self._i2c = i2c_device
        if self._i2c is None:
            import smbus
            self._i2c = smbus.SMBus(1)

        self.chip_id = self._get_regs(CHIP_ID_ADDR, 1)
        if self.chip_id != CHIP_ID:
            raise RuntimeError('BME680 Not Found. Invalid CHIP ID: 0x{0:02x}'.format(self.chip_id))

        self.soft_reset()
        self.set_power_mode(SLEEP_MODE)

        self._get_calibration_data()

        self.set_humidity_oversample(OS_2X)
        self.set_pressure_oversample(OS_4X)
        self.set_temperature_oversample(OS_8X)
        self.set_filter(FILTER_SIZE_3)
        self.set_gas_status(ENABLE_GAS_MEAS)
        self.set_temp_offset(0)
        self.get_sensor_data()

    def _get_calibration_data(self):
        """Retrieve the sensor calibration data and store it in .calibration_data."""
        calibration = self._get_regs(COEFF_ADDR1, COEFF_ADDR1_LEN)
        calibration += self._get_regs(COEFF_ADDR2, COEFF_ADDR2_LEN)

        heat_range = self._get_regs(ADDR_RES_HEAT_RANGE_ADDR, 1)
        heat_value = twos_comp(self._get_regs(ADDR_RES_HEAT_VAL_ADDR, 1), bits=8)
        sw_error = twos_comp(self._get_regs(ADDR_RANGE_SW_ERR_ADDR, 1), bits=8)

        self.calibration_data.set_from_array(calibration)
        self.calibration_data.set_other(heat_range, heat_value, sw_error)

    def soft_reset(self):
        """Trigger a soft reset."""
        self._set_regs(SOFT_RESET_ADDR, SOFT_RESET_CMD)
        time.sleep(RESET_PERIOD / 1000.0)

    def set_temp_offset(self, value):
        """Set temperature offset in celsius.

        If set, the temperature t_fine will be increased by given value in celsius.
        :param value: Temperature offset in Celsius, eg. 4, -8, 1.25

        """
        if value == 0:
            self.offset_temp_in_t_fine = 0
        else:
            self.offset_temp_in_t_fine = int(math.copysign((((int(abs(value) * 100)) << 8) - 128) / 5, value))

    def set_humidity_oversample(self, value):
        """Set humidity oversampling.

        A higher oversampling value means more stable sensor readings,
        with less noise and jitter.

        However each step of oversampling adds about 2ms to the latency,
        causing a slower response time to fast transients.

        :param value: Oversampling value, one of: OS_NONE, OS_1X, OS_2X, OS_4X, OS_8X, OS_16X

        """
        self.tph_settings.os_hum = value
        self._set_bits(CONF_OS_H_ADDR, OSH_MSK, OSH_POS, value)

    def get_humidity_oversample(self):
        """Get humidity oversampling."""
        return (self._get_regs(CONF_OS_H_ADDR, 1) & OSH_MSK) >> OSH_POS

    def set_pressure_oversample(self, value):
        """Set temperature oversampling.

        A higher oversampling value means more stable sensor readings,
        with less noise and jitter.

        However each step of oversampling adds about 2ms to the latency,
        causing a slower response time to fast transients.

        :param value: Oversampling value, one of: OS_NONE, OS_1X, OS_2X, OS_4X, OS_8X, OS_16X

        """
        self.tph_settings.os_pres = value
        self._set_bits(CONF_T_P_MODE_ADDR, OSP_MSK, OSP_POS, value)

    def get_pressure_oversample(self):
        """Get pressure oversampling."""
        return (self._get_regs(CONF_T_P_MODE_ADDR, 1) & OSP_MSK) >> OSP_POS

    def set_temperature_oversample(self, value):
        """Set pressure oversampling.

        A higher oversampling value means more stable sensor readings,
        with less noise and jitter.

        However each step of oversampling adds about 2ms to the latency,
        causing a slower response time to fast transients.

        :param value: Oversampling value, one of: OS_NONE, OS_1X, OS_2X, OS_4X, OS_8X, OS_16X

        """
        self.tph_settings.os_temp = value
        self._set_bits(CONF_T_P_MODE_ADDR, OST_MSK, OST_POS, value)

    def get_temperature_oversample(self):
        """Get temperature oversampling."""
        return (self._get_regs(CONF_T_P_MODE_ADDR, 1) & OST_MSK) >> OST_POS

    def set_filter(self, value):
        """Set IIR filter size.

        Optionally remove short term fluctuations from the temperature and pressure readings,
        increasing their resolution but reducing their bandwidth.

        Enabling the IIR filter does not slow down the time a reading takes, but will slow
        down the BME680s response to changes in temperature and pressure.

        When the IIR filter is enabled, the temperature and pressure resolution is effectively 20bit.
        When it is disabled, it is 16bit + oversampling-1 bits.

        """
        self.tph_settings.filter = value
        self._set_bits(CONF_ODR_FILT_ADDR, FILTER_MSK, FILTER_POS, value)

    def get_filter(self):
        """Get filter size."""
        return (self._get_regs(CONF_ODR_FILT_ADDR, 1) & FILTER_MSK) >> FILTER_POS

    def select_gas_heater_profile(self, value):
        """Set current gas sensor conversion profile.

        Select one of the 10 configured heating durations/set points.

        :param value: Profile index from 0 to 9

        """
        if value > NBCONV_MAX or value < NBCONV_MIN:
            raise ValueError("Profile '{}' should be between {} and {}".format(value, NBCONV_MIN, NBCONV_MAX))

        self.gas_settings.nb_conv = value
        self._set_bits(CONF_ODR_RUN_GAS_NBC_ADDR, NBCONV_MSK, NBCONV_POS, value)

    def get_gas_heater_profile(self):
        """Get gas sensor conversion profile: 0 to 9."""
        return self._get_regs(CONF_ODR_RUN_GAS_NBC_ADDR, 1) & NBCONV_MSK

    def set_gas_status(self, value):
        """Enable/disable gas sensor."""
        self.gas_settings.run_gas = value
        self._set_bits(CONF_ODR_RUN_GAS_NBC_ADDR, RUN_GAS_MSK, RUN_GAS_POS, value)

    def get_gas_status(self):
        """Get the current gas status."""
        return (self._get_regs(CONF_ODR_RUN_GAS_NBC_ADDR, 1) & RUN_GAS_MSK) >> RUN_GAS_POS

    def set_gas_heater_profile(self, temperature, duration, nb_profile=0):
        """Set temperature and duration of gas sensor heater.

        :param temperature: Target temperature in degrees celsius, between 200 and 400
        :param durarion: Target duration in milliseconds, between 1 and 4032
        :param nb_profile: Target profile, between 0 and 9

        """
        self.set_gas_heater_temperature(temperature, nb_profile=nb_profile)
        self.set_gas_heater_duration(duration, nb_profile=nb_profile)

    def set_gas_heater_temperature(self, value, nb_profile=0):
        """Set gas sensor heater temperature.

        :param value: Target temperature in degrees celsius, between 200 and 400

        When setting an nb_profile other than 0,
        make sure to select it with select_gas_heater_profile.

        """
        if nb_profile > NBCONV_MAX or value < NBCONV_MIN:
            raise ValueError('Profile "{}" should be between {} and {}'.format(nb_profile, NBCONV_MIN, NBCONV_MAX))

        self.gas_settings.heatr_temp = value
        temp = int(self._calc_heater_resistance(self.gas_settings.heatr_temp))
        self._set_regs(RES_HEAT0_ADDR + nb_profile, temp)

    def set_gas_heater_duration(self, value, nb_profile=0):
        """Set gas sensor heater duration.

        Heating durations between 1 ms and 4032 ms can be configured.
        Approximately 20-30 ms are necessary for the heater to reach the intended target temperature.

        :param value: Heating duration in milliseconds.

        When setting an nb_profile other than 0,
        make sure to select it with select_gas_heater_profile.

        """
        if nb_profile > NBCONV_MAX or value < NBCONV_MIN:
            raise ValueError('Profile "{}" should be between {} and {}'.format(nb_profile, NBCONV_MIN, NBCONV_MAX))

        self.gas_settings.heatr_dur = value
        temp = self._calc_heater_duration(self.gas_settings.heatr_dur)
        self._set_regs(GAS_WAIT0_ADDR + nb_profile, temp)

    def set_power_mode(self, value, blocking=True):
        """Set power mode."""
        if value not in (SLEEP_MODE, FORCED_MODE):
            raise ValueError('Power mode should be one of SLEEP_MODE or FORCED_MODE')

        self.power_mode = value

        self._set_bits(CONF_T_P_MODE_ADDR, MODE_MSK, MODE_POS, value)

        while blocking and self.get_power_mode() != self.power_mode:
            time.sleep(POLL_PERIOD_MS / 1000.0)

    def get_power_mode(self):
        """Get power mode."""
        self.power_mode = self._get_regs(CONF_T_P_MODE_ADDR, 1)
        return self.power_mode

    def get_sensor_data(self):
        """Get sensor data.

        Stores data in .data and returns True upon success.

        """
        self.set_power_mode(FORCED_MODE)

        for attempt in range(10):
            status = self._get_regs(FIELD0_ADDR, 1)

            if (status & NEW_DATA_MSK) == 0:
                time.sleep(POLL_PERIOD_MS / 1000.0)
                continue

            regs = self._get_regs(FIELD0_ADDR, FIELD_LENGTH)

            self.data.status = regs[0] & NEW_DATA_MSK
            # Contains the nb_profile used to obtain the current measurement
            self.data.gas_index = regs[0] & GAS_INDEX_MSK
            self.data.meas_index = regs[1]

            adc_pres = (regs[2] << 12) | (regs[3] << 4) | (regs[4] >> 4)
            adc_temp = (regs[5] << 12) | (regs[6] << 4) | (regs[7] >> 4)
            adc_hum = (regs[8] << 8) | regs[9]
            adc_gas_res = (regs[13] << 2) | (regs[14] >> 6)
            gas_range = regs[14] & GAS_RANGE_MSK

            self.data.status |= regs[14] & GASM_VALID_MSK
            self.data.status |= regs[14] & HEAT_STAB_MSK

            self.data.heat_stable = (self.data.status & HEAT_STAB_MSK) > 0

            temperature = self._calc_temperature(adc_temp)
            self.data.temperature = temperature / 100.0
            self.ambient_temperature = temperature  # Saved for heater calc

            self.data.pressure = self._calc_pressure(adc_pres) / 100.0
            self.data.humidity = self._calc_humidity(adc_hum) / 1000.0
            self.data.gas_resistance = self._calc_gas_resistance(adc_gas_res, gas_range)
            return True

        return False

    def _set_bits(self, register, mask, position, value):
        """Mask out and set one or more bits in a register."""
        temp = self._get_regs(register, 1)
        temp &= ~mask
        temp |= value << position
        self._set_regs(register, temp)

    def _set_regs(self, register, value):
        """Set one or more registers."""
        if isinstance(value, int):
            self._i2c.write_byte_data(self.i2c_addr, register, value)
        else:
            self._i2c.write_i2c_block_data(self.i2c_addr, register, value)

    def _get_regs(self, register, length):
        """Get one or more registers."""
        if length == 1:
            return self._i2c.read_byte_data(self.i2c_addr, register)
        else:
            return self._i2c.read_i2c_block_data(self.i2c_addr, register, length)

    def _calc_temperature(self, temperature_adc):
        """Convert the raw temperature to degrees C using calibration_data."""
        var1 = (temperature_adc >> 3) - (self.calibration_data.par_t1 << 1)
        var2 = (var1 * self.calibration_data.par_t2) >> 11
        var3 = ((var1 >> 1) * (var1 >> 1)) >> 12
        var3 = ((var3) * (self.calibration_data.par_t3 << 4)) >> 14

        # Save teperature data for pressure calculations
        self.calibration_data.t_fine = (var2 + var3) + self.offset_temp_in_t_fine
        calc_temp = (((self.calibration_data.t_fine * 5) + 128) >> 8)

        return calc_temp

    def _calc_pressure(self, pressure_adc):
        """Convert the raw pressure using calibration data."""
        var1 = ((self.calibration_data.t_fine) >> 1) - 64000
        var2 = ((((var1 >> 2) * (var1 >> 2)) >> 11) *
                self.calibration_data.par_p6) >> 2
        var2 = var2 + ((var1 * self.calibration_data.par_p5) << 1)
        var2 = (var2 >> 2) + (self.calibration_data.par_p4 << 16)
        var1 = (((((var1 >> 2) * (var1 >> 2)) >> 13) *
                ((self.calibration_data.par_p3 << 5)) >> 3) +
                ((self.calibration_data.par_p2 * var1) >> 1))
        var1 = var1 >> 18

        var1 = ((32768 + var1) * self.calibration_data.par_p1) >> 15
        calc_pressure = 1048576 - pressure_adc
        calc_pressure = ((calc_pressure - (var2 >> 12)) * (3125))

        if calc_pressure >= (1 << 31):
            calc_pressure = ((calc_pressure // var1) << 1)
        else:
            calc_pressure = ((calc_pressure << 1) // var1)

        var1 = (self.calibration_data.par_p9 * (((calc_pressure >> 3) *
                (calc_pressure >> 3)) >> 13)) >> 12
        var2 = ((calc_pressure >> 2) *
                self.calibration_data.par_p8) >> 13
        var3 = ((calc_pressure >> 8) * (calc_pressure >> 8) *
                (calc_pressure >> 8) *
                self.calibration_data.par_p10) >> 17

        calc_pressure = (calc_pressure) + ((var1 + var2 + var3 +
                                           (self.calibration_data.par_p7 << 7)) >> 4)

        return calc_pressure

    def _calc_humidity(self, humidity_adc):
        """Convert the raw humidity using calibration data."""
        temp_scaled = ((self.calibration_data.t_fine * 5) + 128) >> 8
        var1 = (humidity_adc - ((self.calibration_data.par_h1 * 16))) -\
               (((temp_scaled * self.calibration_data.par_h3) // (100)) >> 1)
        var2 = (self.calibration_data.par_h2 *
                (((temp_scaled * self.calibration_data.par_h4) // (100)) +
                 (((temp_scaled * ((temp_scaled * self.calibration_data.par_h5) // (100))) >> 6) //
                 (100)) + (1 * 16384))) >> 10
        var3 = var1 * var2
        var4 = self.calibration_data.par_h6 << 7
        var4 = ((var4) + ((temp_scaled * self.calibration_data.par_h7) // (100))) >> 4
        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1
        calc_hum = (((var3 + var6) >> 10) * (1000)) >> 12

        return min(max(calc_hum, 0), 100000)

    def _calc_gas_resistance(self, gas_res_adc, gas_range):
        """Convert the raw gas resistance using calibration data."""
        var1 = ((1340 + (5 * self.calibration_data.range_sw_err)) * (lookupTable1[gas_range])) >> 16
        var2 = (((gas_res_adc << 15) - (16777216)) + var1)
        var3 = ((lookupTable2[gas_range] * var1) >> 9)
        calc_gas_res = ((var3 + (var2 >> 1)) / var2)

        if calc_gas_res < 0:
            calc_gas_res = (1 << 32) + calc_gas_res

        return calc_gas_res

    def _calc_heater_resistance(self, temperature):
        """Convert raw heater resistance using calibration data."""
        temperature = min(max(temperature, 200), 400)

        var1 = ((self.ambient_temperature * self.calibration_data.par_gh3) / 1000) * 256
        var2 = (self.calibration_data.par_gh1 + 784) * (((((self.calibration_data.par_gh2 + 154009) * temperature * 5) / 100) + 3276800) / 10)
        var3 = var1 + (var2 / 2)
        var4 = (var3 / (self.calibration_data.res_heat_range + 4))
        var5 = (131 * self.calibration_data.res_heat_val) + 65536
        heatr_res_x100 = (((var4 / var5) - 250) * 34)
        heatr_res = ((heatr_res_x100 + 50) / 100)

        return heatr_res

    def _calc_heater_duration(self, duration):
        """Calculate correct value for heater duration setting from milliseconds."""
        if duration < 0xfc0:
            factor = 0

            while duration > 0x3f:
                duration /= 4
                factor += 1

            return int(duration + (factor * 64))

        return 0xff
