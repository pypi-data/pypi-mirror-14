# -*- coding: utf-8 -*-
"""Caster object for either real or virtual Monotype composition caster"""
# Built-in time module
from time import time, sleep
# Custom exceptions module
from . import exceptions as e
# Constants module
from . import constants as c
# Default user interface
from .global_settings import UI
# Configuration parsing
from . import cfg_parser
try:
    SIGNALS = (str(cfg_parser.get_config('SignalsArrangements',
                                         'signals_arrangement')).upper())
except e.NotConfigured:
    SIGNALS = c.ALNUM_ARR


class MonotypeCaster(object):
    """Methods common for Caster classes, used for instantiating
    caster driver objects (whether real hardware or mockup for simulation)."""
    def __init__(self):
        self.mode = CasterMode()
        self.sensor = SimulationSensor()
        self.output = SimulationOutput()
        self.stop = EmergencyStop()
        self.lock = False
        # Attach a pump
        self.pump = Pump(self)

    def __enter__(self):
        """Lock the resource so that only one object can use it
        with context manager"""
        if self.lock:
            UI.display('Caster is already busy!')
        else:
            self.lock = True
            UI.debug_pause('Entering the caster context...')
            return self

    def __exit__(self, *_):
        UI.debug_pause('Caster no longer in use.')
        self.lock = False

    @property
    def parameters(self):
        """Gets a list of parameters"""
        # Collect data from I/O drivers
        return ([('\n', '\nCaster data')] + self.sensor.parameters +
                self.stop.parameters + self.output.parameters)

    def process(self, signals, timeout=5):
        """process(signals, timeout):

        Checks for the machine's rotation, sends the signals (activates
        solenoid valves) after the caster is in the "air bar down" position.

        If no machine rotation is detected (sensor input doesn't change
        its state) during cycle_timeout, calls a function to ask user
        what to do (can be useful for resuming casting after manually
        stopping the machine for a short time - not recommended as the
        mould cools down and type quality can deteriorate).

        If the pump was working, the program will store 0075/0005 wedge
        positions, send 0005 to stop the pump and display the menu.
        If the operator decides to go on with casting, the aborted sequence
        will be re-cast so as to avoid missing characters in the composition.
        If the pump was working before, its operation will be resumed
        and the wedges will be reset to previous positions.

        When casting, the pace is dictated by the caster and its RPM. Thus,
        we can't arbitrarily set the intervals between valve ON and OFF
        signals. We need to get feedback from the machine, and we can use
        contact switch (unreliable in the long run), magnet & reed switch
        (not precise enough) or a photocell sensor + LED (very precise).
        We can use a paper tower's operating lever for obscuring the sensor
        (like John Cornelisse did), or we can use a partially obscured disc
        attached to the caster's shaft (like Bill Welliver did).
        Both ways are comparable; the former can be integrated with the
        valve block assembly, and the latter allows for very precise tweaking
        of duty cycle (bright/dark area ratio) and phase shift (disc's position
        relative to 0 degrees caster position).
        """
        while True:
            # Escape this only by returning True on success,
            # or raising exceptions.CastingAborted, exceptions.ExitProgram
            # (which will be handled by the methods of the Casting class)
            try:
                # Casting cycle
                # (sensor on - valves on - sensor off - valves off)
                self.sensor.wait_for(True, timeout)
                self.output.valves_on(signals)
                self.sensor.wait_for(False, timeout)
                self.output.valves_off()
                # self._send_signals_to_caster(signals, cycle_timeout)
                # Successful ending - the combination has been cast
                return True
            except (e.MachineStopped, KeyboardInterrupt, EOFError):
                # Machine stopped during casting - clean up and ask what to do
                self.pump.stop()
                stop_menu()
                # If user continues, pump will be restarted if it was working
                self.pump.start()


class Pump(object):
    """Pump class for storing the pump working/non-working status."""
    def __init__(self, caster):
        self.caster = caster
        self.is_working = self.was_working = False
        # Remember wedge positions on resume
        self.current_0005 = self.last_0005 = '15'
        self.current_0075 = self.last_0075 = '15'

    def stop(self):
        """Forces pump stop - won't end until it is turned off"""
        UI.display('Turning all valves off - just in case...')
        self.caster.output.valves_off()
        self.last_0075, self.last_0005 = self.current_0075, self.current_0005
        self.was_working = self.is_working
        while self.is_working:
            UI.display('The pump is still working - turning it off...')
            try:
                # Run a full machine cycle to turn the pump off
                self.caster.sensor.wait_for(True, 30)
                self.caster.output.valves_on(c.PUMP_STOP)
                self.caster.sensor.wait_for(False, 30)
                self.caster.output.valves_off()
                UI.display('Pump is now off.')
                return True
            except (e.MachineStopped, KeyboardInterrupt, EOFError):
                pass

    def start(self):
        """Starts the pump with given wedge positions"""
        if self.was_working:
            UI.display('Resuming pump action...')
            # Set the wedge positions from before stop
            self.caster.process(c.PUMP_STOP + [self.last_0005])
            self.caster.process(c.PUMP_START + [self.last_0075])
            UI.display('Pump action resumed.')


class SimulationSensor(object):
    """Mockup for a machine cycle sensor"""
    def __init__(self):
        self.lock = False
        self.manual_mode = True
        self.last_state = False
        self.name = 'mockup machine cycle sensor'

    def __enter__(self):
        if not self.lock:
            self.lock = True
            UI.debug_pause('Using a %s for machine feedback' % self.name)
            return self

    def __exit__(self, *_):
        UI.debug_pause('The %s is no longer in use' % self.name)
        self.lock = False

    @property
    def parameters(self):
        """Gets a list of parameters"""
        return [(self.name, 'Sensor driver'),
                (self.manual_mode, 'Manual mode')]

    def check_if_machine_is_working(self):
        """Detect machine cycles and alert if it's not working"""
        UI.display('Now checking if the machine is running...')
        cycles = 3
        while True:
            try:
                while cycles:
                    # Run a new cycle
                    UI.display(cycles)
                    self.wait_for(new_state=True, timeout=30)
                    cycles -= 1
                return True
            except (e.MachineStopped,
                    KeyboardInterrupt, EOFError):
                stop_menu()

    def wait_for(self, new_state, timeout=5, time_on=0.1, time_off=0.1):
        """Waits for a keypress to emulate machine cycle, unless user
        switches to auto mode, where all combinations are processed in batch"""
        status = {True: 'ON', False: 'OFF'}
        UI.debug_info('The sensor is going %s' % status[new_state])
        if self.manual_mode:
            start_time = time()
            # Ask whether to cast or simulate machine stop
            prompt = ('[Enter] to continue, [S] to stop '
                      'or [A] to switch to automatic mode? ')
            answer = UI.enter_data_or_blank(prompt) or ' '
            if answer in 'aA':
                self.manual_mode = False
            elif answer in 'sS':
                raise e.MachineStopped
            elif time() - start_time > timeout:
                UI.display('Timeout - you answered after %ds' % timeout)
                raise e.MachineStopped
        elif new_state:
            sleep(time_off)
        else:
            sleep(time_on)


class PunchingSensor(SimulationSensor):
    """A special sensor class for perforators"""
    def __init__(self):
        super().__init__()
        self.name = 'Timer-driven or manual advance for perforator'

    def check_if_machine_is_working(self):
        """Ask for user confirmation before punching"""
        UI.pause('\nRibbon punching: \n'
                 'Put the ribbon on the perforator and turn on the air.')

    def wait_for(self, new_state, timeout=30, time_on=0.25, time_off=0.4):
        """Calls simulation sensor's function, but with different timings"""
        super().wait_for(new_state, timeout, time_on, time_off)


class TestSensor(SimulationSensor):
    """A keyboard-operated "sensor" for testing inputs.
    No automatic mode is supported."""
    def __init__(self):
        super().__init__()
        self.name = 'Timer-driven or manual advance for perforator'

    def wait_for(self, new_state, *_):
        """Waits for keypress before turning the line off"""
        if not new_state:
            UI.pause('Next combination?')


class EmergencyStop(object):
    """Mockup for an emergency stop button"""
    def __init__(self, gpio=None):
        self.gpio = gpio
        self.name = 'Mockup emergency stop button'
        self.signals, self.value_file, self.edge_file = None, None, None

    @property
    def parameters(self):
        """Gets a list of parameters"""
        return [(self.name, 'Emergency stop button driver')]


class SimulationOutput(object):
    """Mockup for a driver for 32 pneumatic outputs"""
    def __init__(self, sig_arr=SIGNALS):
        self.lock = False
        self.name = 'mockup output driver for simulation'
        self.signals_arrangement = [str(x).upper() for x in sig_arr.split(',')]

    def __del__(self):
        UI.debug_pause('Deleting the %s' % self.name)

    def __enter__(self):
        if not self.lock:
            self.lock = True
            UI.debug_pause('Using the %s for sending signals...' % self.name)
            return self

    def __exit__(self, *_):
        self.valves_off()
        UI.debug_pause('Driver for %s no longer in use.' % self.name)
        self.lock = False

    @property
    def parameters(self):
        """Gets a list of parameters"""
        return [(self.name, 'Output driver'),
                (' '.join(self.signals_arrangement), 'Signals arrangement')]

    def one_on(self, sig):
        """Looks a signal up in arrangement and turns it on"""
        try:
            UI.debug_info(sig + ' on')
        except KeyError:
            raise e.WrongConfiguration('Signal %s not defined!' % sig)

    def one_off(self, sig):
        """Looks a signal up in arrangement and turns it on"""
        try:
            UI.debug_info(sig + ' off')
        except KeyError:
            raise e.WrongConfiguration('Signal %s not defined!' % sig)

    def valves_on(self, signals_list):
        """Turns on multiple valves"""
        for sig in signals_list:
            self.one_on(sig)

    def valves_off(self):
        """Turns off all the valves"""
        for sig in self.signals_arrangement:
            self.one_off(sig)


class CasterMode(object):
    """Session mode: casting / simulation / perforation"""
    def __init__(self):
        self.simulation = False
        self.punching = False
        self.testing = False
        self.calibration = False

    @property
    def simulation(self):
        """Simulation mode"""
        return self.__dict__.get('simulation', False)

    @simulation.setter
    def simulation(self, value):
        """Set the simulation mode"""
        self.__dict__['simulation'] = value and True or False

    @property
    def calibration(self):
        """Machine calibration mode"""
        return self.__dict__.get('calibration', False)

    @calibration.setter
    def calibration(self, value):
        """Set the machine calibration mode"""
        self.__dict__['calibration'] = value and True or False

    @property
    def diagnostics(self):
        """Machine diagnostics i.e. testing or calibration"""
        return self.testing or self.calibration

    @diagnostics.setter
    def diagnostics(self, value=False):
        """Turns the testing or calibration mode off"""
        if not value:
            self.testing = self.calibration = False

    @property
    def punching(self):
        """Punching mode"""
        return self.__dict__.get('punching', False)

    @punching.setter
    def punching(self, value):
        """Set the punching mode"""
        self.__dict__['punching'] = value and True or False

    @property
    def testing(self):
        """Testing mode"""
        return self.__dict__.get('testing', False)

    @testing.setter
    def testing(self, value):
        """Set the testing mode"""
        self.__dict__['testing'] = value and True or False

    @property
    def casting(self):
        """Check if the machine is casting"""
        return not self.punching and not self.testing

    @property
    def hmn(self):
        """Check if HMN mode is currently on"""
        return self.__dict__.get('_hmn', False)

    @hmn.setter
    def hmn(self, value):
        """Set the HMN mode"""
        value = value and True or False
        self.__dict__['_hmn'] = value

    @property
    def unitshift(self):
        """Check if the unit shift mode is currently on"""
        return self.__dict__.get('_unit-shift', False)

    @unitshift.setter
    def unitshift(self, value):
        """Set the unit-shift mode"""
        value = value and True or False
        self.__dict__['_unit-shift'] = value

    @property
    def sensor(self):
        """Chooses a proper sensor"""
        return (self.testing and TestSensor or
                self.punching and PunchingSensor or
                self.simulation and SimulationSensor or
                hardware_sensor)

    @property
    def output(self):
        """Chooses a simulation or hardware output driver"""
        return self.simulation and SimulationOutput or hardware_output

    def choose_row16_addressing(self):
        """Let user decide which way to address row 16"""
        def hmn_on():
            """Turn on the HMN 16x17 attachment"""
            UI.display('Turn the HMN attachment ON')
            self.hmn = True

        def unitshift_on():
            """Turn on the unit-shift attachment (introduced in 1960s)"""
            UI.display('Turn the attachment ON - switch under the paper tower')
            self.unitshift = True

        def do_nothing():
            """User can choose not to use any attachment"""
            return None

        prompt = ('You want to cast from a matrix in the 16th row.\n'
                  'Which attachment do you use: HMN, Unit-Shift or none?\n'
                  '(if none - the matrix will be replaced with O15)\n\n'
                  'Your choice: [U]nit-Shift, [H]MN, leave blank for none?: ')
        options = {'U': unitshift_on, 'H': hmn_on, '': do_nothing}
        UI.simple_menu(prompt, options)()


def stop_menu():
    """This allows us to choose whether we want to continue,
    return to menu or exit if the machine is stopped during casting.
    """
    def continue_casting():
        """Helper function - continue casting."""
        return True
    options = {'C': continue_casting,
               'A': e.abort_casting,
               'E': e.exit_program}
    message = ('Machine is not running!\n'
               '[C]ontinue, [A]bort or [E]xit program? ')
    UI.simple_menu(message, options)()


def hardware_sensor():
    """Gets hardware sensor - prevents import loop"""
    from .input_driver_sysfs import SysfsSensor
    return SysfsSensor()


def hardware_output():
    """Gets hardware output - prevents import loop"""
    from .output_driver_wiringpi import WiringPiOutputDriver
    return WiringPiOutputDriver()
