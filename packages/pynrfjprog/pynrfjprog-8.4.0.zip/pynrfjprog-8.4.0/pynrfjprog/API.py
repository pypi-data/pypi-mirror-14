
#   Package structure:
#       pynrfjprog:
#           __init__.py         -   Module definition file
#           API.py              -   Python wrappers around NRFJPROG DLL functions.
#           Hex.py              -   Provides a way to parse a hex file in order to program it into the device using API.write().
#           JLink.py            -   Provides a function to find the latest Segger JLinkARM.dll installed in the PC.


#    Note:
#        Please look in the nrfjprogdll.h file provided with the tools for a more elaborate 
#        description of the API functions.

# Imports from future that make Python2 behave as Python3.
from __future__ import division
from __future__ import print_function

from builtins import int

import sys
import os
import ctypes
import multiprocessing
from enum import IntEnum, unique

try:
    from . import JLink
except Exception:
    import JLink

py2 = sys.version_info[0] == 2
py3 = sys.version_info[0] == 3

DEBUG_OUTPUT = False

 
@unique
class DeviceFamily(IntEnum):
    """Wraps device_family_t values from DllCommonDefinitions.h """
    NRF51              = 0
    NRF52              = 1

@unique
class DeviceVersion(IntEnum):
    """Wraps device_version_t values from DllCommonDefinitions.h"""
    UNKNOWN                   = 0
    NRF51_XLR1                = 1
    NRF51_XLR2                = 2
    NRF51_XLR3                = 3
    NRF51_L3                  = 4
    NRF51_XLR3P               = 5
    NRF51_XLR3LC              = 6
    NRF52_FP1_ENGA            = 7
    NRF52_FP1_ENGB            = 8
    NRF52_FP1                 = 9
    
@unique
class NrfjprogdllErr(IntEnum):
    """Wraps nrfjprogdll_err_t values from DllCommonDefinitions.h"""
    SUCCESS                                     =  0
    OUT_OF_MEMORY                               = -1 
    INVALID_OPERATION                           = -2
    INVALID_PARAMETER                           = -3
    INVALID_DEVICE_FOR_OPERATION                = -4
    WRONG_FAMILY_FOR_DEVICE                     = -5
    EMULATOR_NOT_CONNECTED                      = -10
    CANNOT_CONNECT                              = -11
    LOW_VOLTAGE                                 = -12
    NO_EMULATOR_CONNECTED                       = -13
    NVMC_ERROR                                  = -20
    NOT_AVAILABLE_BECAUSE_PROTECTION            = -90
    JLINKARM_DLL_NOT_FOUND                      = -100
    JLINKARM_DLL_COULD_NOT_BE_OPENED            = -101
    JLINKARM_DLL_ERROR                          = -102
    JLINKARM_DLL_TOO_OLD                        = -103
    NRFJPROG_SUB_DLL_NOT_FOUND                  = -150
    NRFJPROG_SUB_DLL_COULD_NOT_BE_OPENED        = -151
    NOT_IMPLEMENTED_ERROR                       = -255

@unique    
class ReadbackProtection(IntEnum):
    """Wraps readback_protection_status_t values from DllCommonDefinitions.h"""
    NONE                       = 0
    REGION_0                   = 1
    ALL                        = 2
    BOTH                       = 3

@unique
class Region0Source(IntEnum):
    """Wraps region_0_source_t values from DllCommonDefinitions.h"""
    NO_REGION_0                = 0
    FACTORY                    = 1
    USER                       = 2
    
@unique
class RamPower(IntEnum):
    """Wraps ram_power_status_t values from DllCommonDefinitions.h"""
    OFF                    = 0
    ON                     = 1
    
@unique
class RTTChannelDirection(IntEnum):
    """Wraps rtt_direction_t values from DllCommonDefinitions.h"""
    UP_DIRECTION           = 0
    DOWN_DIRECTION         = 1

@unique
class CpuRegister(IntEnum):
    """Wraps cpu_registers_t values from DllCommonDefinitions.h"""
    R0                        = 0
    R1                        = 1
    R2                        = 2
    R3                        = 3
    R4                        = 4
    R5                        = 5
    R6                        = 6
    R7                        = 7
    R8                        = 8
    R9                        = 9
    R10                       = 10
    R11                       = 11
    R12                       = 12
    R13                       = 13
    R14                       = 14
    R15                       = 15
    XPSR                      = 16
    MSP                       = 17
    PSP                       = 18
    

class APIError(Exception):
    """Subclass for reporting errors."""

    def __init__(self, err_str, err_code=None):
        """Constructs a new object and saves the err_code in addition to the message err_str."""
        super(Exception, self).__init__(err_str)
        self.err_code = err_code

    @classmethod
    def from_nrfjprog_err(cls, err_code):
        """Creates a new APIError with a string describing the given err_code value."""
        if err_code in [member.value for name, member in NrfjprogdllErr.__members__.items()]:
            return APIError("An error was reported by NRFJPROG DLL: %d ('%s')." % (err_code, NrfjprogdllErr(err_code).name), err_code)
        
        return APIError(("An error was reported by NRFJPROG DLL: %d." % err_code), err_code)


class API(object):
    """Provides simplified access to the nrfjprog.dll API."""

    # A copy of NRFJPROG.DLL must be found in the working directory for the API to work.
    
    _DEFAULT_JLINK_SPEED_KHZ            = 2000
    

    class DLLFunction(object):
        """Wrapper for calls into a DLL via ctypes."""

        _LOG_CB = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        _NRFJPROG_ERROR = ctypes.c_int32


        def __init__(self, key, restype, argtypes):
            """Creates a wrapper for the functional with the given symbol of a DLL."""
            self._key = key
            self._restype = restype
            self._argtypes = argtypes
            self._callbacks = []


        def set_lib(self, lib):
            """Configures the parameters for this wrapper's function."""
            if (self._key is not None):
                self._lib = lib
                self._lib[self._key].restype  = self._restype
                self._lib[self._key].argtypes = self._argtypes
                del(self._callbacks[:])


        def __call__(self, *args):
            """Casts the given arguments into the expected types and then calls this wrapper's function."""
            params = []

            if (self._key is None):
                raise APIError('Object construction cannot be called without a valid symbol.')

            for i in range(0, len(args)):
                if (args[i] is not None):
                    param = self._argtypes[i](args[i])
                else:
                    param = self._argtypes[i]()

                params.append(param)
                if (self._LOG_CB == self._argtypes[i]):
                    self._callbacks.append(param)

            if (self._restype is not None):
                return self._lib[self._key](*params)
            else:
                self._lib[self._key](*params)


    _DLL_FUNCTIONS = {
                    'dll_version':                      DLLFunction( 'NRFJPROG_dll_version', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint8)]),
                    
                    'open_dll':                         DLLFunction( 'NRFJPROG_open_dll', DLLFunction._NRFJPROG_ERROR, [ctypes.c_char_p, DLLFunction._LOG_CB, ctypes.c_uint32]),

                    'close_dll':                        DLLFunction( 'NRFJPROG_close_dll', None, None),

                    'enum_emu_snr':                     DLLFunction( 'NRFJPROG_enum_emu_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),

                    'is_connected_to_emu':              DLLFunction( 'NRFJPROG_is_connected_to_emu', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'connect_to_emu_with_snr':          DLLFunction( 'NRFJPROG_connect_to_emu_with_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),                                               

                    'connect_to_emu_without_snr':       DLLFunction( 'NRFJPROG_connect_to_emu_without_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]), 

                    'disconnect_from_emu':              DLLFunction( 'NRFJPROG_disconnect_from_emu', DLLFunction._NRFJPROG_ERROR, None),                    
                    
                    'recover':                          DLLFunction( 'NRFJPROG_recover', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'is_connected_to_device':           DLLFunction( 'NRFJPROG_is_connected_to_device', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'connect_to_device':                DLLFunction( 'NRFJPROG_connect_to_device', DLLFunction._NRFJPROG_ERROR, None),                                               
                    
                    'readback_protect':                 DLLFunction( 'NRFJPROG_readback_protect', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),

                    'readback_status':                  DLLFunction( 'NRFJPROG_readback_status', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'read_region_0_size_and_source':    DLLFunction( 'NRFJPROG_read_region_0_size_and_source', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]),

                    'debug_reset':                      DLLFunction( 'NRFJPROG_debug_reset', DLLFunction._NRFJPROG_ERROR, None),

                    'sys_reset':                        DLLFunction( 'NRFJPROG_sys_reset', DLLFunction._NRFJPROG_ERROR, None),

                    'pin_reset':                        DLLFunction( 'NRFJPROG_pin_reset', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'disable_bprot':                    DLLFunction( 'NRFJPROG_disable_bprot', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'erase_all':                        DLLFunction( 'NRFJPROG_erase_all', DLLFunction._NRFJPROG_ERROR, None),

                    'erase_page':                       DLLFunction( 'NRFJPROG_erase_page', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),

                    'erase_uicr':                       DLLFunction( 'NRFJPROG_erase_uicr', DLLFunction._NRFJPROG_ERROR, None),                                                   

                    'write_u32':                        DLLFunction( 'NRFJPROG_write_u32', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool]),

                    'read_u32':                         DLLFunction( 'NRFJPROG_read_u32', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),

                    'write':                            DLLFunction( 'NRFJPROG_write', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.c_bool]),
                    
                    'read':                             DLLFunction( 'NRFJPROG_read', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32]),

                    'is_halted':                        DLLFunction( 'NRFJPROG_is_halted', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'halt':                             DLLFunction( 'NRFJPROG_halt', DLLFunction._NRFJPROG_ERROR, None),   

                    'run':                              DLLFunction( 'NRFJPROG_run', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),

                    'go':                               DLLFunction( 'NRFJPROG_go', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'step':                             DLLFunction( 'NRFJPROG_step', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'is_ram_powered':                   DLLFunction( 'NRFJPROG_is_ram_powered', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32) , ctypes.POINTER(ctypes.c_uint32)]),   
                    
                    'power_ram_all':                    DLLFunction( 'NRFJPROG_power_ram_all', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'unpower_ram_section':              DLLFunction( 'NRFJPROG_unpower_ram_section', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),   
                    
                    'read_cpu_register':                DLLFunction( 'NRFJPROG_read_cpu_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_cpu_register':               DLLFunction( 'NRFJPROG_write_cpu_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),

                    'read_device_version':              DLLFunction( 'NRFJPROG_read_device_version', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'read_debug_port_register':         DLLFunction( 'NRFJPROG_read_debug_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_debug_port_register':        DLLFunction( 'NRFJPROG_write_debug_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint32]),
                    
                    'read_access_port_register':        DLLFunction( 'NRFJPROG_read_access_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_access_port_register':       DLLFunction( 'NRFJPROG_write_access_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint32]),
                    
                    'rtt_set_control_block_address':    DLLFunction( 'NRFJPROG_rtt_set_control_block_address', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),
                    
                    'rtt_start':                        DLLFunction( 'NRFJPROG_rtt_start', DLLFunction._NRFJPROG_ERROR, None),

                    'rtt_is_control_block_found':       DLLFunction( 'NRFJPROG_rtt_is_control_block_found', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),
                    
                    'rtt_stop':                         DLLFunction( 'NRFJPROG_rtt_stop', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'rtt_read':                         DLLFunction( 'NRFJPROG_rtt_read', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'rtt_write':                        DLLFunction( 'NRFJPROG_rtt_write', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'rtt_read_channel_count':           DLLFunction( 'NRFJPROG_rtt_read_channel_count', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'rtt_read_channel_info':            DLLFunction( 'NRFJPROG_rtt_read_channel_info', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)])
                }

    def __init__(self, device_family, jlink_arm_dll_path=None, log_str_cb=None):
        """The log_str_cb callback can be used to receive log and error information. These callbacks should expect to
        receive a string as the only parameter and do not need to return anything."""
        # Decode the family of devices to use
        self._device_family = self._decode_enum(device_family, DeviceFamily)
        if self._device_family is None:
            raise APIError('Parameter device_family must be of type int, str or DeviceFamily enumeration.')
        
        # Obtain the path to JLINKARM.dll
        self._jlink_arm_dll_path = None
        if jlink_arm_dll_path is None:
            jlink_arm_dll_path = JLink.find_latest_dll()
            if jlink_arm_dll_path is None:
                raise APIError('Could not locate a JLinkARM.dll in the default SEGGER installation path.')
        else:
            if not self._is_string(jlink_arm_dll_path):
                raise APIError('Parameter jlink_arm_dll_path must be the path to JLinkARM.dll in str type.')
        
        self._jlink_arm_dll_path = os.path.abspath(jlink_arm_dll_path)
        if py3:
            self._jlink_arm_dll_path = self._jlink_arm_dll_path.encode('ascii')
        
        # Obtain the possible logging callback function
        if log_str_cb is not None:
            if not hasattr(log_str_cb, '__call__'):
                raise APIError('Parameter log_str_cb is not callable.')
        elif DEBUG_OUTPUT:
            log_str_cb = lambda x: self._debug_print(x, '[NRFJPROG DLL LOG]')                    
        self._log_str_cb = log_str_cb        
                
        # Find the NRFJPROG DLL in the working directory.
        this_dir, this_file = os.path.split(__file__) 
        
        if sys.platform.lower().startswith('win'):
            nrfjprog_dll_folder = 'win_dll'
            nrfjprog_dll_name = 'nrfjprog.dll'
        elif sys.platform.lower().startswith('linux'):
            if sys.maxsize > 2**32:
                nrfjprog_dll_folder = 'linux_64bit_so'
            else:
                nrfjprog_dll_folder = 'linux_32bit_so'
            nrfjprog_dll_name = 'libnrfjprogdll.so'
        elif sys.platform.startswith('dar'):
            nrfjprog_dll_folder = 'osx_dylib'
            nrfjprog_dll_name = 'libnrfjprogdll.dylib'
        
        nrfjprog_dll_path = os.path.join(os.path.abspath(this_dir), nrfjprog_dll_folder, nrfjprog_dll_name)

        if not nrfjprog_dll_path:
            raise APIError("Failed to locate the NRFJPROG DLL in the pynrfjprog directory.")
        
        try:
            self._lib = ctypes.CDLL(nrfjprog_dll_path)
        except Exception as err:
            raise APIError("Could not load the NRFJPROG DLL: '%s'." % err)
        
        # Load the functions from the library
        for key in self._DLL_FUNCTIONS:
            self._DLL_FUNCTIONS[key].set_lib(self._lib)
        

    def dll_version(self):
        """ Returns the JLinkARM.dll version."""
        
        major = ctypes.c_uint32()
        minor = ctypes.c_uint32()
        revision = ctypes.c_uint8()
        
        result = self._DLL_FUNCTIONS['dll_version'](major, minor, revision)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
        return (major.value, minor.value, chr(revision.value))
        
            
    def open(self):
        """ Opens the JLinkARM DLL and prepares the dll to work with a specific nRF device family."""
        
        result = self._DLL_FUNCTIONS['open_dll'](self._jlink_arm_dll_path, self._log_str_cb, self._device_family.value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def close(self):
        """ Closes and frees the JLinkARM DLL."""
        
        self._DLL_FUNCTIONS['close_dll']()
    
    
    def enum_emu_snr(self):
        """ Enumerates the serial numbers of connected USB J-Link emulators.
            Return: List with the serial numbers of connected emulators."""
        
        serial_numbers_len  = 50
        serial_numbers      = (ctypes.c_uint32 * serial_numbers_len)()
        num_available       = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['enum_emu_snr'](serial_numbers, serial_numbers_len, num_available)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
       
        snr = [int(serial_numbers[i]) for i in range(0, min(num_available.value, serial_numbers_len))]

        if len(snr) == 0:
            return None
        else:
            return snr

            
    def is_connected_to_emu(self):
        """ Checks if the emulator has an established connection with Segger emulator/debugger. 
            Return: True or False."""
        
        is_connected_to_emu = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_connected_to_emu'](is_connected_to_emu)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_connected_to_emu.value
        
    
    def connect_to_emu_with_snr(self, serial_number, jlink_speed_khz=_DEFAULT_JLINK_SPEED_KHZ):
        """ Connects to a given emulator/debugger.
            Input: Serial number of the emulator to connect to. Optional: Speed for the SWD communication."""
        
        if not self._is_u32(serial_number):
            raise APIError('The serial_number parameter must be an unsigned 32bit value.')
        
        if not self._is_u32(jlink_speed_khz):
            raise APIError('The jlink_speed_khz parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['connect_to_emu_with_snr'](serial_number, jlink_speed_khz)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        
    def connect_to_emu_without_snr(self, jlink_speed_khz=_DEFAULT_JLINK_SPEED_KHZ):
        """ Connects to an emulator/debugger. If more than one emulator is available, a pop-up window will appear.
            Input: Optional: Speed for the SWD communication."""
        
        if not self._is_u32(jlink_speed_khz):
            raise APIError('The jlink_speed_khz parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['connect_to_emu_without_snr'](jlink_speed_khz)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
            
    def disconnect_from_emu(self):
        """ Disconnects from a connected emulator. """
        
        result = self._DLL_FUNCTIONS['disconnect_from_emu']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        
    def recover(self):
        """ Recovers the device."""
        
        result = self._DLL_FUNCTIONS['recover']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def is_connected_to_device(self):
        """ Checks if the emulator has an established connection with an nRF device.
            Return: True or False."""
        
        is_connected_to_device  = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_connected_to_device'](is_connected_to_device)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_connected_to_device.value
    
    
    def connect_to_device(self):
        """ Connects to the nRF device and halts it."""
        
        result = self._DLL_FUNCTIONS['connect_to_device']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def readback_protect(self, desired_protection_level):
        """ Protects the device against read or debug.
            Input: Desired protection level of readback protection (ReadbackProtection)."""
        
        if not self._is_enum(desired_protection_level, ReadbackProtection):
            raise APIError('Parameter desired_protection_level must be of type int, str or ReadbackProtection enumeration.')
            
        desired_protection_level = self._decode_enum(desired_protection_level, ReadbackProtection)
        if desired_protection_level is None:
            raise APIError('Parameter desired_protection_level must be of type int, str or ReadbackProtection enumeration.')
        
        result = self._DLL_FUNCTIONS['readback_protect'](desired_protection_level.value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def readback_status(self):
        """ Returns the status of the readback protection.
            Return: ReadbackProtection status."""
        
        status  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['readback_status'](status)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return ReadbackProtection(status.value).name
        
        
    def read_region_0_size_and_source(self):
        """ Returns the region 0 size and source of protection if any.
            Return: Region size, and ReadbackProtection."""
        
        size  = ctypes.c_uint32()
        source  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_region_0_size_and_source'](size, source)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return size.value, Region0Source(source.value).name
   
   
    def debug_reset(self):
        """ Executes a reset using the CTRL-AP."""
        
        result = self._DLL_FUNCTIONS['debug_reset']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

            
    def sys_reset(self):
        """ Executes a system reset request."""
        
        result = self._DLL_FUNCTIONS['sys_reset']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def pin_reset(self):
        """ Executes a pin reset."""
        
        result = self._DLL_FUNCTIONS['pin_reset']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def disable_bprot(self):
        """ Disables BPROT."""
        
        result = self._DLL_FUNCTIONS['disable_bprot']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
        
    def erase_all(self):
        """ Erases all flash."""
        
        result = self._DLL_FUNCTIONS['erase_all']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

    
    def erase_page(self, addr):
        """ Erases a page of code flash.
            Input: Address of the code flash page to erase."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')
    
        result = self._DLL_FUNCTIONS['erase_page'](addr)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
        
    def erase_uicr(self):
        """ Erases UICR."""
        
        result = self._DLL_FUNCTIONS['erase_uicr']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            

    def write_u32(self, addr, data, control):
        """ Writes one uint32_t data at the given address.
            Input: Address to write to. Value to write. If the target address needs NVMC control."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_u32(data):
            raise APIError('The data parameter must be an unsigned 32bit value.')
            
        if not self._is_bool(control):
            raise APIError('The control parameter must be a boolean value.')

        result = self._DLL_FUNCTIONS['write_u32'](addr, data, control)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            

    def read_u32(self, addr):
        """ Reads one uint32 address.
            Input: Address to read from.
            Return: uint32 value at address."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        data  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_u32'](addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        

    def write(self, addr, data, control):
        """ Writes data from the buffer starting at the given address.
            Input: Start address of the region to write to. Buffer with data to write. If the target 
            address needs NVMC control."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_valid_buf(data):
            raise APIError('The data parameter must be a tuple or a list with at least one item.')
            
        if not self._is_bool(control):
            raise APIError('The control parameter must be a boolean value.')
        
        data = (ctypes.c_uint8 * len(data))(*data)

        result = self._DLL_FUNCTIONS['write'](addr, data, len(data), control)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

   
    def read(self, addr, length):
        """ Reads length bytes starting at address addr.
            Input: Address to read from. Number of bytes to read.
            Return: Returns list with uint8 values from addr."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_u32(length):
            raise APIError('The length parameter must be an unsigned 32bit value.')

        data = (ctypes.c_uint8 * length)()

        result = self._DLL_FUNCTIONS['read'](addr, data, length)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return list(data)


    def is_halted(self):
        """ Checks if the nRF CPU is halted.
            Return: True or False."""
        
        is_halted  = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_halted'](is_halted)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_halted.value
        

    def halt(self):
        """ Halts the nRF CPU."""
        
        result = self._DLL_FUNCTIONS['halt']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

            
    def run(self, pc, sp):
        """ Starts the nRF CPU with the given pc and sp.
            Input: Program Counter to start running from. Stack Pointer to use when running."""
        
        if (not self._is_u32(pc)):
            raise APIError('The pc parameter must be an unsigned 32bit value.')

        if (not self._is_u32(sp)):
            raise APIError('The sp parameter must be an unsigned 32bit value.')

        result = self._DLL_FUNCTIONS['run'](pc, sp)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def go(self):
        """ Starts the nRF CPU."""
        
        result = self._DLL_FUNCTIONS['go']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
            
    def step(self):
        """ Steps the nRF CPU."""
        
        result = self._DLL_FUNCTIONS['step']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def is_ram_powered(self):
        """ Reads the RAM power status.
            Return: List with RAM power information; array of results, number of sections in device, size of sections."""
        
        status_size = 64
        status = (ctypes.c_uint32 * status_size)()
        number  = ctypes.c_uint32()
        size  = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['is_ram_powered'](status, status_size, number, size)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        return [RamPower(elem).name for elem in list(status)[0:number.value]], number.value, size.value
       
    
    def power_ram_all(self):
        """ Powers all RAM sections of the device."""
        
        result = self._DLL_FUNCTIONS['power_ram_all']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
     
     
    def unpower_ram_section(self, section_index):
        """ Unpowers a RAM section of the device.
            Input: Index of RAM section to power_off."""
        
        if (not self._is_u32(section_index)):
            raise APIError('The section_index parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['unpower_ram_section'](section_index)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_cpu_register(self, register_name):
        """ Reads a CPU register.
            Input: CPU Register name to read (CpuRegister).
            Return: uint32 value from register."""
        
        if not self._is_enum(register_name, CpuRegister):
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
            
        register_name = self._decode_enum(register_name, CpuRegister)
        if register_name is None:
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
        
        value  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_cpu_register'](register_name.value, value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return value.value
        
        
    def write_cpu_register(self, register_name, value):
        """ Writes a CPU register.
            Input: CPU register to write (CpuRegister). uint32 Value to write."""
        
        if (not self._is_u32(value)):
            raise APIError('The value parameter must be an unsigned 32bit value.')

        if not self._is_enum(register_name, CpuRegister):
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
            
        register_name = self._decode_enum(register_name, CpuRegister)
        if register_name is None:
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
        
        result = self._DLL_FUNCTIONS['write_cpu_register'](register_name, value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_device_version(self):
        """ Reads the device version connected to the device.
            Return: uint32 DeviceVersion number."""
        
        version = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['read_device_version'](version)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return DeviceVersion(version.value).name
        
        
    def read_debug_port_register(self, reg_addr):
        """ Reads a debugger debug port register.
            Input: Register address to read.
            Return: uin32 data Value from register."""
        
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
        
        data  = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['read_debug_port_register'](reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        
    
    def write_debug_port_register(self, reg_addr, data):
        """ Writes a debugger debug port register.
            Input: Register address to write. uint32 data to write into register."""
        
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
            
        if (not self._is_u32(data)):
            raise APIError('The data parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['write_debug_port_register'](reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_access_port_register(self, ap_index, reg_addr):
        """ Reads a debugger access port register.
            Input: Access port index for red if ap_access. Register address to read.
            Return: uint32 data value from register."""
        
        if (not self._is_u8(ap_index)):
            raise APIError('The ap_index parameter must be an unsigned 8bit value.')
            
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
        
        data  = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['read_access_port_register'](ap_index, reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        
    
    def write_access_port_register(self, ap_index, reg_addr, data):
        """ Writes a debugger access port register.
            Input: Access port index for write if ap_access. Register address to write. Data to write to register."""
        
        if (not self._is_u8(ap_index)):
            raise APIError('The ap_index parameter must be an unsigned 8bit value.')
            
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
            
        if (not self._is_u32(data)):
            raise APIError('The data parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['write_access_port_register'](ap_index, reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

            
    def rtt_set_control_block_address(self, address):
        """ Sets the address of the RTT control block for a quicker rtt_start().
            Input: Address of RTT control block in the device memory."""
        
        if (not self._is_u32(address)):
            raise APIError('The address parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['rtt_set_control_block_address'](address)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def rtt_start(self):
        """ Starts RTT processing."""
        
        result = self._DLL_FUNCTIONS['rtt_start']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def rtt_is_control_block_found(self):
        """ Checks if RTT control block has been found.  
            Return: True or False."""
        
        is_control_block_found = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['rtt_is_control_block_found'](is_control_block_found)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_control_block_found.value
    
    
    def rtt_stop(self):
        """ Stops RTT processing."""
        
        result = self._DLL_FUNCTIONS['rtt_stop']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def rtt_read(self, channel_index, length):
        """ Reads data from the RTT.
            Input: Index of the RTT channel to read from. Data length to read if data present.
            Return: Data read."""
            
        if not self._is_u32(channel_index):
            raise APIError('The channel_index parameter must be an unsigned 32bit value.')

        if not self._is_u32(length):
            raise APIError('The length parameter must be an unsigned 32bit value.')
            
        data = (ctypes.c_uint8 * length)()
        data_read = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['rtt_read'](channel_index, data, length, data_read)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        return ''.join(chr(i) for i in data[0:data_read.value])
        
        
    def rtt_write(self, channel_index, msg):
        """ Writes data to the RTT.
            Input: Index of the RTT channel to write to. Message to write.
            Return: Number of data written."""
            
        if not self._is_u32(channel_index):
            raise APIError('The channel_index parameter must be an unsigned 32bit value.')

        if not self._is_string(msg):
            raise APIError('The msg parameter must be a text message of str type.')
        
        if py2:
            data = (ctypes.c_char * len(msg))(*msg)
        elif py3:
            data = (ctypes.c_char * len(msg))(*msg.encode('ascii'))
            
        data_written = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['rtt_write'](channel_index, data, len(msg), data_written)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        return data_written.value
        
    
    def rtt_read_channel_count(self):
        """ Reads the number of RTT channels in the target device.
            Return: Number of RTT down channels. Number of RTT up channels."""
        
        down_channel_number = ctypes.c_uint32()
        up_channel_number = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['rtt_read_channel_count'](down_channel_number, up_channel_number)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return down_channel_number.value, up_channel_number.value
        
    
    def rtt_read_channel_info(self, channel_index, direction):
        """ Reads the information of one RTT channel.
            Input: Index of the RTT channel. Direction of the channel.
            Return: Name of RTT channel. size of RTT channel."""
        
        if not self._is_u32(channel_index):
            raise APIError('The channel_index parameter must be an unsigned 32bit value.')
            
        if not self._is_enum(direction, RTTChannelDirection):
            raise APIError('Parameter direction must be of type int, str or RTTChannelDirection enumeration.')
            
        name = (ctypes.c_uint8 * 32)()
        size = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['rtt_read_channel_info'](channel_index, direction, name, 32, size)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return ''.join(chr(i) for i in name if i != 0), size.value

        
    def _is_u32(self, value):
        """ Checks if a value is uint32."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 0xFFFFFFFF)
        
        
    def _is_u8(self, value):
        """ Checks if a value is uint8."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 0xFF)

        
    def _is_bool(self, value):
        """ Checks if value is boolean."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 1)
        

    def _is_valid_buf(self, buf):
        """ Checks if a buffer is valid or not."""
        if not isinstance(buf, tuple) and not isinstance(buf, list):
            return False

        for value in buf:
            if value < 0:
                return False

        return (len(buf) != 0)
        
        
    def _is_number(self, value):
        """ Checks if value is number."""
        if not isinstance(value, int):
            return False
            
        return True
        
        
    def _is_string(self, string):
        """ Checks if string is string."""
        return isinstance(string, str)
        
        
    def _is_enum(self, param, enum_type):
        """ Checks if param is enum_type."""
        if self._is_number(param):
            if param in [member.value for name, member in enum_type.__members__.items()]:
                return True
        elif self._is_string(param):
            if param in [name for name, member in enum_type.__members__.items()]:
                return True
        elif param in enum_type.__members__.items():
            return True
        
        return False

    def _decode_enum(self, param, enum_type):
        """ Decodes param of enum_type."""
        if not self._is_enum(param, enum_type):
            return None
        
        if self._is_number(param):
            return enum_type(param)
        elif self._is_string(param):
            return enum_type[param]
        else: 
            return param
        

    def __enter__(self):
        """ Called automatically when the 'with' construct is used."""
        self.open()
        return self


    def __exit__(self, type, value, traceback):
        """ Called automatically when the 'with' construct is used."""
        self.close()


    def _debug_print(self, msg_str, prefix='[nrfjprog.API]'):
        print("{} {}".format(prefix, msg_str.strip()), file=sys.stderr)
        
        
class _Command(object):
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args

        
class _CommandAck(object):
    def __init__(self, exception=None, result=None):
        self.exception = exception
        self.result = result

        
def _runner(CmdQueue, CmdAckQueue, device_family, jlink_arm_dll_path, log_str_cb):
    
    # Mapping of commands to API class member functions. It has to be mapped in this function since class member functions cannot be sent to a subprocess, only deault types.
    _API_FUNCTIONS = {  'dll_version':                   API.dll_version,
                   
                        'open':                          API.open,
                        'close':                         API.close,
                   
                        'enum_emu_snr':                  API.enum_emu_snr,
                   
                        'is_connected_to_emu':           API.is_connected_to_emu,
                        'connect_to_emu_with_snr':       API.connect_to_emu_with_snr,
                        'connect_to_emu_without_snr':    API.connect_to_emu_without_snr,
                        'disconnect_from_emu':           API.disconnect_from_emu,
                   
                        'recover':                       API.recover,
                        'is_connected_to_device':        API.is_connected_to_device,
                        'connect_to_device':             API.connect_to_device,
                   
                        'readback_protect':              API.readback_protect,
                        'readback_status':               API.readback_status,
                        'read_region_0_size_and_source': API.read_region_0_size_and_source,
                   
                        'debug_reset':                   API.debug_reset,
                        'sys_reset':                     API.sys_reset,
                        'pin_reset':                     API.pin_reset,
                   
                        'disable_bprot':                 API.disable_bprot,
                   
                        'erase_all':                     API.erase_all,
                        'erase_page':                    API.erase_page,
                        'erase_uicr':                    API.erase_uicr,
                   
                        'write_u32':                     API.write_u32,
                        'read_u32':                      API.read_u32,
                        'write':                         API.write,
                        'read':                          API.read,
                   
                        'is_halted':                     API.is_halted,
                        'halt':                          API.halt,
                        'run':                           API.run,
                        'go':                            API.go,
                        'step':                          API.step,
                    
                        'is_ram_powered':                API.is_ram_powered,
                        'power_ram_all':                 API.power_ram_all,
                        'unpower_ram_section':           API.unpower_ram_section,
                   
                        'read_cpu_register':             API.read_cpu_register,
                        'write_cpu_register':            API.write_cpu_register,
                    
                        'read_device_version':           API.read_device_version,
                   
                        'read_debug_port_register':      API.read_debug_port_register,
                        'write_debug_port_register':     API.write_debug_port_register,
                        'read_access_port_register':     API.read_access_port_register,
                        'write_access_port_register':    API.write_access_port_register,
                   
                        'rtt_set_control_block_address': API.rtt_set_control_block_address,
                        'rtt_start':                     API.rtt_start,
                        'rtt_is_control_block_found':    API.rtt_is_control_block_found,
                        'rtt_stop':                      API.rtt_stop,
                        'rtt_read':                      API.rtt_read,
                        'rtt_write':                     API.rtt_write,
                        'rtt_read_channel_count':        API.rtt_read_channel_count,
                        'rtt_read_channel_info':         API.rtt_read_channel_info
                 }
    
    # Create API object to executes commands. the operation loads the nrfjprog and JLinkArm libraries in a separate process, creating a local copy those libraries.
    api = API(device_family, jlink_arm_dll_path, log_str_cb)

    # Run in loop executing received commands
    while True:
        
        cmd = CmdQueue.get()
        
        try:
            res = _API_FUNCTIONS[cmd.cmd](api, *cmd.args)
            
        except Exception as e:
            CmdAckQueue.put(_CommandAck(exception=e))
            
        else: 
            CmdAckQueue.put(_CommandAck(result=res))
            

class MultiAPI(object):

    def __init__(self, device_family, jlink_arm_dll_path=None, log_str_cb=None):
        
        # Create queues for command comunication with _runner function. 
        self.CmdQueue = multiprocessing.Queue()
        self.CmdAckQueue = multiprocessing.Queue()
        
        # Create subprocess and run it.
        self.runner = multiprocessing.Process(target=_runner, args=(self.CmdQueue, self.CmdAckQueue, device_family, jlink_arm_dll_path, log_str_cb))
        self.runner.daemon = True
        self.runner.start()
        
        
    def __del__(self):
        if self.runner.is_alive():
            self.close()
            self.runner.terminate()
        
    
    def __enter__(self):
        """ Called automatically when the 'with' construct is used."""
        self.open()
        return self


    def __exit__(self, type, value, traceback):
        """ Called automatically when the 'with' construct is used."""
        self.close()
        self.runner.terminate()
        
    
    def dll_version(self):
        self.CmdQueue.put(_Command('dll_version'))
        return self._wait_for_completion()
        
    
    def open(self):
        self.CmdQueue.put(_Command('open'))
        return self._wait_for_completion()
        
        
    def close(self):
        self.CmdQueue.put(_Command('close'))
        return self._wait_for_completion()
        
        
    def enum_emu_snr(self):
        self.CmdQueue.put(_Command('enum_emu_snr'))
        return self._wait_for_completion()
        
        
    def is_connected_to_emu(self):
        self.CmdQueue.put(_Command('is_connected_to_emu'))
        return self._wait_for_completion()
        
    
    def connect_to_emu_with_snr(self, serial_number, jlink_speed_khz=API._DEFAULT_JLINK_SPEED_KHZ):
        self.CmdQueue.put(_Command('connect_to_emu_with_snr', serial_number, jlink_speed_khz))
        return self._wait_for_completion()
        
    
    def connect_to_emu_without_snr(self, jlink_speed_khz=API._DEFAULT_JLINK_SPEED_KHZ):
        self.CmdQueue.put(_Command('connect_to_emu_without_snr', jlink_speed_khz))
        return self._wait_for_completion()
        
        
    def disconnect_from_emu(self):
        self.CmdQueue.put(_Command('disconnect_from_emu'))
        return self._wait_for_completion()
        
    
    def recover(self):
        self.CmdQueue.put(_Command('recover'))
        return self._wait_for_completion()
        
        
    def is_connected_to_device(self):
        self.CmdQueue.put(_Command('is_connected_to_device'))
        return self._wait_for_completion()
        
    
    def connect_to_device(self):
        self.CmdQueue.put(_Command('connect_to_device'))
        return self._wait_for_completion()
        
    
    def readback_protect(self, desired_protection_level):
        self.CmdQueue.put(_Command('readback_protect', desired_protection_level))
        return self._wait_for_completion()
        
    
    def readback_status(self):
        self.CmdQueue.put(_Command('readback_status'))
        return self._wait_for_completion()
        
    
    def read_region_0_size_and_source(self):
        self.CmdQueue.put(_Command('read_region_0_size_and_source'))
        return self._wait_for_completion()
        
    
    def debug_reset(self):
        self.CmdQueue.put(_Command('debug_reset'))
        return self._wait_for_completion()
        
    
    def sys_reset(self):
        self.CmdQueue.put(_Command('sys_reset'))
        return self._wait_for_completion()
        
    
    def pin_reset(self):
        self.CmdQueue.put(_Command('pin_reset'))
        return self._wait_for_completion()
        
    
    def disable_bprot(self):
        self.CmdQueue.put(_Command('disable_bprot'))
        return self._wait_for_completion()
        
    
    def erase_all(self):
        self.CmdQueue.put(_Command('erase_all'))
        return self._wait_for_completion()
        
        
    def erase_page(self, addr):
        self.CmdQueue.put(_Command('erase_page', addr))
        return self._wait_for_completion()
        
        
    def erase_uicr(self):
        self.CmdQueue.put(_Command('erase_uicr'))
        return self._wait_for_completion()
        
    
    def write_u32(self, addr, data, control):
        self.CmdQueue.put(_Command('write_u32', addr, data, control))
        return self._wait_for_completion()
        
    
    def read_u32(self, addr):
        self.CmdQueue.put(_Command('read_u32', addr))
        return self._wait_for_completion()
        
        
    def write(self, addr, data, control):
        self.CmdQueue.put(_Command('write', addr, data, control))
        return self._wait_for_completion()
        
        
    def read(self, addr, length):
        self.CmdQueue.put(_Command('read', addr, length))
        return self._wait_for_completion()
        
    
    def is_halted(self):
        self.CmdQueue.put(_Command('is_halted'))
        return self._wait_for_completion()
        
    
    def halt(self):
        self.CmdQueue.put(_Command('halt'))
        return self._wait_for_completion()
        
        
    def run(self, pc, sp):
        self.CmdQueue.put(_Command('run', pc, sp))
        return self._wait_for_completion()
        
        
    def go(self):
        self.CmdQueue.put(_Command('go'))
        return self._wait_for_completion()
        
        
    def step(self):
        self.CmdQueue.put(_Command('step'))
        return self._wait_for_completion()
        
        
    def is_ram_powered(self):
        self.CmdQueue.put(_Command('is_ram_powered'))
        return self._wait_for_completion()
        
    
    def power_ram_all(self):
        self.CmdQueue.put(_Command('power_ram_all'))
        return self._wait_for_completion()
        
        
    def unpower_ram_section(self, section_index):
        self.CmdQueue.put(_Command('unpower_ram_section', section_index))
        return self._wait_for_completion()
        
    
    def read_cpu_register(self, register_name):
        self.CmdQueue.put(_Command('read_cpu_register', register_name))
        return self._wait_for_completion()
        
        
    def write_cpu_register(self, register_name, value):
        self.CmdQueue.put(_Command('write_cpu_register', register_name, value))
        return self._wait_for_completion()
        
    
    def read_device_version(self):
        self.CmdQueue.put(_Command('read_device_version'))
        return self._wait_for_completion()
        
    
    def read_debug_port_register(self, reg_addr):
        self.CmdQueue.put(_Command('read_debug_port_register', reg_addr))
        return self._wait_for_completion()
        
    
    def write_debug_port_register(self, reg_addr, data):
        self.CmdQueue.put(_Command('write_debug_port_register', reg_addr, data))
        return self._wait_for_completion()
        
        
    def read_access_port_register(self, ap_index, reg_addr):
        self.CmdQueue.put(_Command('read_access_port_register', ap_index, reg_addr))
        return self._wait_for_completion()
        
        
    def write_access_port_register(self, ap_index, reg_addr, data):
        self.CmdQueue.put(_Command('write_access_port_register', ap_index, reg_addr, data))
        return self._wait_for_completion()
        
    
    def rtt_set_control_block_address(self, address):
        self.CmdQueue.put(_Command('rtt_set_control_block_address', address))
        return self._wait_for_completion()
        
    
    def rtt_start(self):
        self.CmdQueue.put(_Command('rtt_start'))
        return self._wait_for_completion()


    def rtt_is_control_block_found(self):
        self.CmdQueue.put(_Command('rtt_is_control_block_found'))
        return self._wait_for_completion()
        
        
    def rtt_stop(self):
        self.CmdQueue.put(_Command('rtt_stop'))
        return self._wait_for_completion()
        
    
    def rtt_read(self, channel_index, length):
        self.CmdQueue.put(_Command('rtt_read', channel_index, length))
        return self._wait_for_completion()
        
        
    def rtt_write(self, channel_index, msg):
        self.CmdQueue.put(_Command('rtt_write', channel_index, msg))
        return self._wait_for_completion()
        
        
    def rtt_read_channel_count(self):
        self.CmdQueue.put(_Command('rtt_read_channel_count'))
        return self._wait_for_completion()
        
        
    def rtt_read_channel_info(self, channel_index, direction):
        self.CmdQueue.put(_Command('rtt_read_channel_info', channel_index, direction))
        return self._wait_for_completion()
        
    
    def _wait_for_completion(self):
        
        ack = self.CmdAckQueue.get()
        
        if ack.exception is not None:
            raise ack.exception
            
        if ack.result is not None:
            return ack.result
    
        
