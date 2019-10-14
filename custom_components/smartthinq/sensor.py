import logging
import voluptuous as vol
import json
from datetime import timedelta
import time


from homeassistant.components import sensor
from custom_components.smartthinq import (
        DOMAIN, LGE_DEVICES, LGEDevice)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA  # noqa
from homeassistant.const import (
    ATTR_ENTITY_ID, CONF_NAME, CONF_TOKEN, CONF_ENTITY_ID)
from homeassistant.exceptions import PlatformNotReady


import wideq

DEPENDENCIES = ['smartthinq']

LGE_WASHER_DEVICES = 'lge_washer_devices'
LGE_DRYER_DEVICES = 'lge_dryer_devices'
LGE_WATERPURIFIER_DEVICES = 'lge_waterpurifier_devices'

CONF_MAC = 'mac'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
})

# For WASHER
#-----------------------------------------------------------
ATTR_CURRENT_STATUS = 'curent_status'
ATTR_RUN_STATE = 'run_state'
ATTR_PRE_STATE = 'previous_state'
ATTR_REMAIN_TIME = 'remaining_time'
ATTR_INITIAL_TIME = 'initial_time'
ATTR_RESERVE_TIME = 'reserve_time'
ATTR_CURRENT_COURSE = 'course'
ATTR_WASH_OPTION_STATE = 'soil'
ATTR_SPIN_OPTION_STATE = 'spin'
ATTR_WATER_TEMP_OPTION_STATE = 'water_temp'
ATTR_ERROR_STATE = 'error_state'
ATTR_RINSECOUNT_OPTION_STATE = 'rinsecount_option_state'
ATTR_DRYLEVEL_STATE = 'drylevel_state'
ATTR_CHILDLOCK_MODE = 'childlock_mode'
ATTR_STEAM_MODE = 'steam_mode'
#csirk
ATTR_TURBOWASH_MODE = 'turbowash_mode'
ATTR_CREASECARE_MODE = 'creasecare_mode'
ATTR_STEAMSOFTENER_MODE = 'steamsoftener_mode'
ATTR_ECOHYBRID_MODE = 'ecohybrid_mode'
ATTR_MEDICRINSE_MODE = 'medicrinse_mode'
ATTR_RINSESPIN_MODE = 'rinsespin_mode'
ATTR_PREWASH_MODE = 'prewash_mode'
ATTR_INITIALBIT_MODE = 'initialbit_mode'
ATTR_REMOTESTART_MODE = 'remotestart_mode'
ATTR_DOORLOCK_MODE = 'doorlock_mode'
#csirk
ATTR_TUBCLEAN_COUNT = 'tubclean_count'
ATTR_LOAD_LEVEL = 'load_level'

WASHERRUNSTATES = {
    'OFF': wideq.STATE_WASHER_OFF,
    'INITIAL': wideq.STATE_WASHER_INITIAL,
    'COMPLETE' : wideq.STATE_WASHER_COMPLETE,
    'PAUSE': wideq.STATE_WASHER_PAUSE,
    'ERROR_AUTO_OFF': wideq.STATE_WASHER_ERROR_AUTO_OFF,
    'RESERVE': wideq.STATE_WASHER_RESERVE,
    'DETECTING': wideq.STATE_WASHER_DETECTING,
    'ADD_DRAIN': wideq.STATE_WASHER_ADD_DRAIN,
    'DETERGENT_AMOUNT': wideq.STATE_WASHER_DETERGENT_AMOUT,
    'RUNNING': wideq.STATE_WASHER_RUNNING,
    'PREWASH': wideq.STATE_WASHER_PREWASH,
    'RINSING': wideq.STATE_WASHER_RINSING,
    'RINSE_HOLD': wideq.STATE_WASHER_RINSE_HOLD,
    'SPINNING': wideq.STATE_WASHER_SPINNING,
    'DRYING': wideq.STATE_WASHER_DRYING,
    'FRESHCARE': wideq.STATE_WASHER_FRESHCARE,
    'TCL_ALARM_NORMAL': wideq.STATE_WASHER_TCL_ALARM_NORMAL,
    'FROZEN_PREVENT_INITIAL': wideq.STATE_WASHER_FROZEN_PREVENT_INITIAL,
    'FROZEN_PREVENT_RUNNING': wideq.STATE_WASHER_FROZEN_PREVENT_RUNNING,
    'FROZEN_PREVENT_PAUSE': wideq.STATE_WASHER_FROZEN_PREVENT_PAUSE,
    'ERROR': wideq.STATE_WASHER_ERROR,
#csirk
	'STATE_WASHER_COOLDOWN' : wideq.STATE_WASHER_COOLDOWN
	'STATE_WASHER_RINSEHOLD' : wideq.STATE_WASHER_RINSEHOLD
	'STATE_WASHER_REFRESHING' : wideq.STATE_WASHER_REFRESHING
	'STATE_WASHER_STEAMSOFTENING' : wideq.STATE_WASHER_STEAMSOFTENING
	'STATE_WASHER_DEMO' : wideq.STATE_WASHER_DEMO
#csirk

}

SOILLEVELSTATES = {
    'NO_SELECT': wideq.STATE_WASHER_TERM_NO_SELECT,
    'LIGHT': wideq.STATE_WASHER_SOILLEVEL_LIGHT,
    'NORMAL': wideq.STATE_WASHER_SOILLEVEL_NORMAL,
    'HEAVY': wideq.STATE_WASHER_SOILLEVEL_HEAVY,
    'PRE_WASH': wideq.STATE_WASHER_SOILLEVEL_PRE_WASH,
    'SOAKING': wideq.STATE_WASHER_SOILLEVEL_SOAKING,
    'OFF': wideq.STATE_WASHER_POWER_OFF,
}

WATERTEMPSTATES = {
    'NO_SELECT': wideq.STATE_WASHER_TERM_NO_SELECT,
    'TAP_COLD' : wideq.STATE_WASHER_WATERTEMP_TAP_COLD,
    'COLD' : wideq.STATE_WASHER_WATERTEMP_COLD,
    'SEMI_WARM' : wideq.STATE_WASHER_WATERTEMP_SEMI_WARM,
    'WARM': wideq.STATE_WASHER_WATERTEMP_WARM,
    'HOT': wideq.STATE_WASHER_WATERTEMP_HOT,
    'EXTRA_HOTE': wideq.STATE_WASHER_WATERTEMP_EXTRA_HOT,
    'OFF': wideq.STATE_WASHER_POWER_OFF,
#csirk
	'TEMP_COLD' : wideq.STATE_WASHER_TEMP_COLD,
	'TEMP_20' : wideq.STATE_WASHER_TEMP_20,
	'TEMP_30' : wideq.STATE_WASHER_TEMP_30,
	'TEMP_40' : wideq.STATE_WASHER_TEMP_40,
	'TEMP_50' : wideq.STATE_WASHER_TEMP_50,
	'TEMP_60' : wideq.STATE_WASHER_TEMP_60,
	'TEMP_95' : wideq.STATE_WASHER_TEMP_95,
#csirk
}

SPINSPEEDSTATES = {
    'NO_SELECT': wideq.STATE_WASHER_TERM_NO_SELECT,
    'EXTRA_LOW' : wideq.STATE_WASHER_SPINSPEED_EXTRA_LOW,
    'LOW' : wideq.STATE_WASHER_SPINSPEED_LOW,
    'MEDIUM' : wideq.STATE_WASHER_SPINSPEED_MEDIUM,
    'HIGH': wideq.STATE_WASHER_SPINSPEED_HIGH,
    'EXTRA_HIGH': wideq.STATE_WASHER_SPINSPEED_EXTRA_HIGH,
    'OFF': wideq.STATE_WASHER_POWER_OFF,
	'SPIN_NO' : wideq.STATE_WASHER_SPINSPEED_SPIN_NO,
	'SPIN_400' : wideq.STATE_WASHER_SPINSPEED_SPIN_400,
	'SPIN_600' : wideq.STATE_WASHER_SPINSPEED_SPIN_600,
	'SPIN_700' : wideq.STATE_WASHER_SPINSPEED_SPIN_700,
	'SPIN_800' : wideq.STATE_WASHER_SPINSPEED_SPIN_800,
	'SPIN_900' : wideq.STATE_WASHER_SPINSPEED_SPIN_900,
	'SPIN_1000' : wideq.STATE_WASHER_SPINSPEED_SPIN_1000,
	'SPIN_1100' : wideq.STATE_WASHER_SPINSPEED_SPIN_1100,
	'SPIN_1200' : wideq.STATE_WASHER_SPINSPEED_SPIN_1200,
	'SPIN_1400' : wideq.STATE_WASHER_SPINSPEED_SPIN_1400,
	'SPIN_1600' : wideq.STATE_WASHER_SPINSPEED_SPIN_1600,
	'SPIN_MAX' : wideq.STATE_WASHER_SPINSPEED_SPIN_MAX,
}

RINSECOUNTSTATES = {
    'NO_SELECT': wideq.STATE_WASHER_TERM_NO_SELECT,
    'ONE' : wideq.STATE_WASHER_RINSECOUNT_1,
    'TWO' : wideq.STATE_WASHER_RINSECOUNT_2,
    'THREE' : wideq.STATE_WASHER_RINSECOUNT_3,
    'FOUR': wideq.STATE_WASHER_RINSECOUNT_4,
    'FIVE': wideq.STATE_WASHER_RINSECOUNT_5,
    'OFF': wideq.STATE_WASHER_POWER_OFF,
}

DRYLEVELSTATES = {
    'NO_SELECT': wideq.STATE_WASHER_TERM_NO_SELECT,
    'WIND' : wideq.STATE_WASHER_DRYLEVEL_WIND,
    'TURBO' : wideq.STATE_WASHER_DRYLEVEL_TURBO,
    'TIME_30' : wideq.STATE_WASHER_DRYLEVEL_TIME_30,
    'TIME_60': wideq.STATE_WASHER_DRYLEVEL_TIME_60,
    'TIME_90': wideq.STATE_WASHER_DRYLEVEL_TIME_90,
    'TIME_120': wideq.STATE_WASHER_DRYLEVEL_TIME_120,
    'TIME_150': wideq.STATE_WASHER_DRYLEVEL_TIME_150,
    'OFF': wideq.STATE_WASHER_POWER_OFF,
#csirk
	'DRY_NORMAL' : wideq.STATE_WASHER_DRYLEVEL_DRY_NORMAL,
	'DRY_30' : wideq.STATE_WASHER_DRYLEVEL_DRY_30,
	'DRY_60' : wideq.STATE_WASHER_DRYLEVEL_DRY_60,
	'DRY_90' : wideq.STATE_WASHER_DRYLEVEL_DRY_90,
	'DRY_120' : wideq.STATE_WASHER_DRYLEVEL_DRY_120,
	'DRY_150' : wideq.STATE_WASHER_DRYLEVEL_DRY_150,
	'DRY_ECO' : wideq.STATE_WASHER_DRYLEVEL_DRY_ECO,
	'DRY_VERY' : wideq.STATE_WASHER_DRYLEVEL_DRY_VERY,
	'DRY_IRON' : wideq.STATE_WASHER_DRYLEVEL_DRY_IRON,
	'DRY_LOW' : wideq.STATE_WASHER_DRYLEVEL_DRY_LOW,
	'DRY_ENERGY' : wideq.STATE_WASHER_DRYLEVEL_DRY_ENERGY,
	'DRY_SPEED' : wideq.STATE_WASHER_DRYLEVEL_DRY_SPEED,
	'DRY_COOLING' : wideq.STATE_WASHER_DRYLEVEL_DRY_COOLING,
#csirk
}

WASHERCOURSES = {

    'NORMAL' : wideq.STATE_WASHER_COURSE_NORMAL,
    'HEAVY_DUTY' : wideq.STATE_WASHER_COURSE_HEAVY_DUTY,
    'DELICATES' : wideq.STATE_WASHER_COURSE_DELICATES,
    'WATER_PROOF' : wideq.STATE_WASHER_COURSE_WATER_PROOF,
    'SPEED_WASH' : wideq.STATE_WASHER_COURSE_SPEED_WASH,
    'BEDDING' : wideq.STATE_WASHER_COURSE_BEDDING,
    'TUB_CLEAN' : wideq.STATE_WASHER_COURSE_TUB_CLEAN,
    'RINSE_SPIN' : wideq.STATE_WASHER_COURSE_RINSE_SPIN,
    'SPIN_ONLY' : wideq.STATE_WASHER_COURSE_SPIN_ONLY,
    'PREWASH_PLUS' : wideq.STATE_WASHER_COURSE_PREWASH_PLUS,
    'OFF' : wideq.STATE_WASHER_POWER_OFF,
#csirk
	'Cotton' : wideq.STATE_WASHER_COURSE_COTTON,
	'Easy Care' : wideq.STATE_WASHER_COURSE_EASY_CARE,
	'Cotton+' : wideq.STATE_WASHER_COURSE_COTTON_P,
	'Duvet' : wideq.STATE_WASHER_COURSE_DUVET,
	'Mix' : wideq.STATE_WASHER_COURSE_MIX,
	'Sports Wear' : wideq.STATE_WASHER_COURSE_SPORTS_WEAR,
	'Gentle Care' : wideq.STATE_WASHER_COURSE_GENTLE_CARE,
	'Wash+Dry 5' : wideq.STATE_WASHER_COURSE_WASHDRY_5,
	'Delicate' : wideq.STATE_WASHER_COURSE_DELICATE,
	'Quick 30' : wideq.STATE_WASHER_COURSE_QUICK_30,
	'Direct Wear' : wideq.STATE_WASHER_COURSE_DIRECT_WEAR,
	'Baby Steam Care' : wideq.STATE_WASHER_COURSE_BABY_STEAM_CARE,
	'Allergy SpaSteam' : wideq.STATE_WASHER_COURSE_ALLERGY_SPASTEAM,
#csirk
}

WASHERERRORS = {
#csirk
	'No Error' : wideq.STATE_WASHER_ERROR_NO,
	'DE2 Error' : wideq.STATE_WASHER_ERROR_DE2,
	'DE1 Error' : wideq.STATE_WASHER_ERROR_DE1,
	'IE Error' : wideq.STATE_WASHER_ERROR_IE,
	'OE Error' : wideq.STATE_WASHER_ERROR_OE,
	'UE Error' : wideq.STATE_WASHER_ERROR_UE,
	'FE Error' : wideq.STATE_WASHER_ERROR_FE,
	'PE Error' : wideq.STATE_WASHER_ERROR_PE,
	'tE error' : wideq.STATE_WASHER_ERROR_TE,
	'LE error' : wideq.STATE_WASHER_ERROR_LE,
	'dHE error' : wideq.STATE_WASHER_ERROR_DHE,
	'PF error' : wideq.STATE_WASHER_ERROR_PF,
	'FF error' : wideq.STATE_WASHER_ERROR_FF,
	'dCE Error' : wideq.STATE_WASHER_ERROR_DCE,
	'AE Error (AquaLock)' : wideq.STATE_WASHER_ERROR_AE ERROR,
	'EE error' : wideq.STATE_WASHER_ERROR_EE,
	'PS Error' : wideq.STATE_WASHER_ERROR_PS,
	'dE4 Error' : wideq.STATE_WASHER_ERROR_DE4,
#csirk
}

OPTIONITEMMODES = {
    'ON': wideq.STATE_OPTIONITEM_ON,
    'OFF': wideq.STATE_OPTIONITEM_OFF,
}

MAX_RETRIES = 5

LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    import wideq
    refresh_token = hass.data[CONF_TOKEN]
    client = wideq.Client.from_token(refresh_token)
    name = config[CONF_NAME]
    conf_mac = config[CONF_MAC]

    """Set up the LGE entity."""
    for device_id in hass.data[LGE_DEVICES]:
        device = client.get_device(device_id)
        model = client.model_info(device)
        model_type = model.model_type
        mac = device.macaddress
        if device.type == wideq.DeviceType.WASHER:
            LGE_WASHER_DEVICES = []
            if mac == conf_mac.lower():
                LOGGER.debug("Creating new LGE Washer")
                try:
                    washer_entity = LGEWASHERDEVICE(client, device, name, model_type)
                except wideq.NotConnectError:
                    LOGGER.info('Connection Lost. Retrying.')
                    raise PlatformNotReady
                LGE_WASHER_DEVICES.append(washer_entity)
                add_entities(LGE_WASHER_DEVICES)
                LOGGER.debug("LGE Washer is added")

# WASHER Main 
class LGEWASHERDEVICE(LGEDevice):
    def __init__(self, client, device, name, model_type):
        
        """initialize a LGE Washer Device."""
        LGEDevice.__init__(self, client, device)

        import wideq
        self._washer = wideq.WasherDevice(client, device)

        self._washer.monitor_start()
        self._washer.monitor_start()
        self._washer.delete_permission()
        self._washer.delete_permission()

        # The response from the monitoring query.
        self._state = None
        self._name = name
        self._type = model_type

        self.update()

    @property
    def name(self):
        return self._name

    @property
    def device_type(self):
        return self._type

    @property
    def supported_features(self):
        """ none """

    @property
    def state_attributes(self):
        """Return the optional state attributes."""
        data={}
        data[ATTR_DEVICE_TYPE] = self.device_type
        data[ATTR_RUN_STATE] = self.current_run_state
        data[ATTR_PRE_STATE] = self.pre_state
        data[ATTR_REMAIN_TIME] = self.remain_time
        data[ATTR_INITIAL_TIME] = self.initial_time
        data[ATTR_RESERVE_TIME] = self.reserve_time
        data[ATTR_CURRENT_COURSE] = self.current_course
#        data[ATTR_WATER_TEMP_OPTION_STATE] = self.water_temp_option_state
#        data[ATTR_WASH_OPTION_STATE] = self.wash_option_state
        data[ATTR_SPIN_OPTION_STATE] = self.spin_option_state
        data[ATTR_ERROR_STATE] = self.error_state
#        data[ATTR_RINSECOUNT_OPTION_STATE] = self.rinsecount_option_state
        data[ATTR_DRYLEVEL_STATE] = self.drylevel_state
        data[ATTR_CHILDLOCK_MODE] = self.childlock_mode
        data[ATTR_STEAM_MODE] = self.steam_mode
        data[ATTR_TUBCLEAN_COUNT] = self.tubclean_count
        data[ATTR_LOAD_LEVEL] = self.load_level
#csirk
		data[ATTR_TURBOWASH_MODE] = self.turbowash_mode
		data[ATTR_CREASECARE_MODE] = self.creasecare_mode
		data[ATTR_STEAMSOFTENER_MODE] = self.steamsoftener_mode
		data[ATTR_ECOHYBRID_MODE] = self.ecohybrid_mode
		data[ATTR_MEDICRINSE_MODE] = self.medicrinse_mode
		data[ATTR_RINSESPIN_MODE] = self.rinsespin_mode
		data[ATTR_PREWASH_MODE] = self.prewash_mode
		data[ATTR_INITIALBIT_MODE] = self.initialbit_mode
		data[ATTR_REMOTESTART_MODE] = self.remotestart_mode
		data[ATTR_DOORLOCK_MODE] = self.doorlock_mode
#csirk
 return data

    @property
    def state(self):
        if self._state:
            run = self._state.run_state
            return WASHERRUNSTATES[run.name]

    @property
    def current_run_state(self):
        if self._state:
            run = self._state.run_state
            return WASHERRUNSTATES[run.name]

    @property
    def pre_state(self):
        if self._state:
            pre = self._state.pre_state
            return WASHERRUNSTATES[pre.name]

    @property
    def remain_time(self):    
        if self._state:
            remain_hour = self._state.remaintime_hour
            remain_min = self._state.remaintime_min
            remaintime = [remain_hour, remain_min]
            if int(remain_min) < 10:
                return ":0".join(remaintime)
            else:
                return ":".join(remaintime)
            
    @property
    def initial_time(self):
        if self._state:
            initial_hour = self._state.initialtime_hour
            initial_min = self._state.initialtime_min
            initialtime = [initial_hour, initial_min]
            if int(initial_min) < 10:
                return ":0".join(initialtime)
            else:
                return ":".join(initialtime)

    @property
    def reserve_time(self):
        if self._state:
            reserve_hour = self._state.reservetime_hour
            reserve_min = self._state.reservetime_min
            reservetime = [reserve_hour, reserve_min]
            if int(reserve_min) < 10:
                return ":0".join(reservetime)
            else:
                return ":".join(reservetime)

    @property
    def current_course(self):
        if self._state:
            course = self._state.current_course
            smartcourse = self._state.current_smartcourse
            if course == 'APCourse':
                return smartcourse
            elif course == 'OFF':
                return 'OFF'
            else:
                return course


    @property
    def current_course(self):
        if self._state:
            course = self._state.current_course
            return WASHERCOURSES[course]

    @property
    def current_smartcourse(self):
        if self._state:
            smartcourse = self._state.current_smartcourse
            return WASHERSMARTCOURSES[smartcourse]


    @property
    def error_state(self):
        if self._state:
            error = self._state.error_state
            return WASHERERRORS[error]


    @property
    def wash_option_state(self):
        if self._state:
            wash_option = self._state.wash_option_state
            if wash_option == 'OFF':
                return SOILLEVELSTATES['OFF']
            else:
                return SOILLEVELSTATES[wash_option.name]

    @property
    def spin_option_state(self):
        if self._state:
            spin_option = self._state.spin_option_state
            if spin_option == 'OFF':
                return SPINSPEEDSTATES['OFF']
            else:
                return SPINSPEEDSTATES[spin_option.name]

    @property
    def water_temp_option_state(self):
        if self._state:
            water_temp_option = self._state.water_temp_option_state
            if water_temp_option == 'OFF':
                return WATERTEMPSTATES['OFF']
            else:
                return WATERTEMPSTATES[water_temp_option.name]

    @property
    def rinsecount_option_state(self):
        if self._state:
            rinsecount_option = self._state.rinsecount_option_state
            if rinsecount_option == 'OFF':
                return RINSECOUNTSTATES['OFF']
            else:
                return RINSECOUNTSTATES[rinsecount_option.name]

    @property
    def drylevel_state(self):
        if self._state:
            drylevel = self._state.drylevel_option_state
            if drylevel == 'OFF':
                return DRYLEVELSTATES['OFF']
            else:
                return DRYLEVELSTATES[drylevel.name]

    @property
    def tempcontrol_state(self):
        if self._state:
            tempcontrol = self._state.tempcontrol_state
            if tempcontrol == 'OFF':
                return TEMPCONTROLMODES['OFF']
            else:
                return TEMPCONTROLMODES[tempcontrol.name]

    @property
    def tempcontrol_list(self):
        return list(TEMPCONTROLMODES.values())

    @property
    def turbowash_mode(self):
        if self._state:
            mode = self._state.turbowash_state
            return OPTIONITEMMODES[mode]
    @property
    def creasecare_mode(self):
        if self._state:
            mode = self._state.creasecare_state
            return OPTIONITEMMODES[mode]
    @property
    def steamsoftener_mode(self):
        if self._state:
            mode = self._state.steamsoftener_state
            return OPTIONITEMMODES[mode]
    @property
    def ecohybrid_mode(self):
        if self._state:
            mode = self._state.ecohybrid_state
            return OPTIONITEMMODES[mode]
    @property
    def medicrinse_mode(self):
        if self._state:
            mode = self._state.medicrinse_state
            return OPTIONITEMMODES[mode]
    @property
    def rinsespin_mode(self):
        if self._state:
            mode = self._state.rinsespin_state
            return OPTIONITEMMODES[mode]
    @property
    def prewash_mode(self):
        if self._state:
            mode = self._state.prewash_state
            return OPTIONITEMMODES[mode]
    @property
    def steam_mode(self):
        if self._state:
            mode = self._state.steam_state
            return OPTIONITEMMODES[mode]
    @property
    def initialbit_mode(self):
        if self._state:
            mode = self._state.initialbit_state
            return OPTIONITEMMODES[mode]
    @property
    def remotestart_mode(self):
        if self._state:
            mode = self._state.remotestart_state
            return OPTIONITEMMODES[mode]
    @property
    def doorlock_mode(self):
        if self._state:
            mode = self._state.doorlock_state
            return OPTIONITEMMODES[mode]
    @property
    def childlock_mode(self):
        if self._state:
            mode = self._state.childlock_state
            return OPTIONITEMMODES[mode]
#csirk



    @property
    def tubclean_count(self):
        if self._state:
            return self._state.tubclean_count
    
    @property
    def load_level(self):
        if self._state:
            load_level = self._state.load_level
            if load_level == 1:
                return 'handful'
            elif load_level == 2:
                return 'less'
            elif load_level == 3:
                return 'usually'
            elif load_level == 4:
                return 'plenty'
            else:
                return 'none'

    def update(self):

        import wideq

        LOGGER.info('Updating %s.', self.name)
        for iteration in range(MAX_RETRIES):
            LOGGER.info('Polling...')

            try:
                state = self._washer.poll()
            except wideq.NotLoggedInError:
                LOGGER.info('Session expired. Refreshing.')
                self._client.refresh()
                self._washer.monitor_start()
                self._washer.monitor_start()
                self._washer.delete_permission()
                self._washer.delete_permission()

                continue

            except wideq.NotConnectError:
                LOGGER.info('Connection Lost. Retrying.')
                self._client.refresh()
                time.sleep(60)
                continue

            if state:
                LOGGER.info('Status updated.')
                self._state = state
                self._client.refresh()
                self._washer.monitor_start()
                self._washer.monitor_start()
                self._washer.delete_permission()
                self._washer.delete_permission()
                return

            LOGGER.info('No status available yet.')
            time.sleep(2 ** iteration)

        # We tried several times but got no result. This might happen
        # when the monitoring request gets into a bad state, so we
        # restart the task.
        LOGGER.warn('Status update failed.')

        self._washer.monitor_start()
        self._washer.monitor_start()
        self._washer.delete_permission()
        self._washer.delete_permission()
