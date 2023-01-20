from abc import abstractmethod
import logging
from typing import Tuple

import numpy

from PySide6.QtCore import Slot, QRegularExpression
from PySide6.QtGui import QValidator, QRegularExpressionValidator
from PySide6.QtWidgets import QWidget
from cirq import Qid, SparseSimulatorStep

from ui.simwindowbase_ui import Ui_Form as Teleportation_Ui
from ui.teleportationsetup_ui import Ui_Form as Teleportation_Setup
from ui.deutschsetup_ui import Ui_Form as Deutsch_Setup
from quantumsimulation import QuantumTeleportation, DeutschJozsa, DeutschJozsaOracle3Q, SimpleEntanglement
from customwidgets import BlochFigure


class BadConfigurationException(Exception):
    pass


class BasicSimulationWindow(QWidget):
    def __init__(self):
        super(BasicSimulationWindow, self).__init__()
        self.ui = Teleportation_Ui()
        self.ui.setupUi(self)

        # additional UI setup that can't be done in autogenerated class
        self.ui.step_button.released.connect(self.execute_step)
        self.ui.setup_button.released.connect(self.create_simulator)

        self.sim = None
        self.last_state = None

        self.success_message = ""
        self.failure_message = ""

    @Slot()
    def execute_step(self):
        try:
            state, info_str, entangled, is_entangled = self.fetch_simulation_step()
            self.last_state = state

            self.add_line_to_log(info_str)
            self.ui.stateVectorLabel.setText(str(state.state_vector()))

            self.update_ui(state, entangled)

            if is_entangled:
                self.add_line_to_log(f"WYKRYTO SPLĄTANIE! Splątanie pomiędzy: {[e.name for e in entangled]}")
        except StopIteration:
            self.ui.step_button.setEnabled(False)
            if self.sim.check_results(self.last_state):
                self.add_line_to_log(self.success_message)
            else:
                self.add_line_to_log(self.failure_message)

    @abstractmethod
    @Slot()
    def create_simulator(self):
        pass

    @abstractmethod
    def update_ui(self, sim_state: SparseSimulatorStep, entangled_list: Tuple[Qid]):
        pass

    def fetch_simulation_step(self):
        state, info_str, entangled = next(self.sim.step())
        is_entangled = len(entangled) > 0
        return state, info_str, entangled, is_entangled

    def disable_configuration_elements(self) -> None:
        pass

    def add_line_to_log(self, line: str) -> None:
        self.ui.listWidget.addItem(line)


class SimpleEntaglementWindow(BasicSimulationWindow):
    def __init__(self):
        super(SimpleEntaglementWindow, self).__init__()

        self.bloch1 = BlochFigure("alicja")
        self.bloch2 = BlochFigure("bob")
        self.ui.bloch_space.addWidget(self.bloch1)
        self.ui.bloch_space.addWidget(self.bloch2)

        self.setWindowTitle("Proste splątanie")

        self.success_message = "Tutaj nie ma co sprawdzać ;)"
        self.failure_message = "Hej, czemu to w ogóle widzisz?"

    def create_simulator(self):
        self.sim = SimpleEntanglement()

        self.ui.setup_button.setEnabled(False)
        self.ui.step_button.setEnabled(True)

    def update_ui(self, sim_state: SparseSimulatorStep, entangled_list: Tuple[Qid]):
        self.bloch1.update_plot(sim_state.bloch_vector_of(self.sim.qubits["alice"]),
                                self.sim.qubits["alice"] in entangled_list)
        self.bloch2.update_plot(sim_state.bloch_vector_of(self.sim.qubits["bob"]),
                                self.sim.qubits["bob"] in entangled_list)


class TeleportationSetup(QWidget):
    def __init__(self):
        super(TeleportationSetup, self).__init__()
        self.ui = Teleportation_Setup()
        self.ui.setupUi(self)

        self.ui.phaseSlider.valueChanged.connect(self.slider_value_change)

    @Slot(int)
    def slider_value_change(self, new_value: int) -> None:
        self.ui.label.setText(f"Faza bramki: {new_value / 100.0}")


class TeleportationWindow(BasicSimulationWindow):
    def __init__(self):
        super(TeleportationWindow, self).__init__()

        self.teleportationSetup = TeleportationSetup()
        self.ui.buttonsAndSetupLayout.addWidget(self.teleportationSetup)

        self.bloch1 = BlochFigure("msg")
        self.bloch2 = BlochFigure("alice")
        self.bloch3 = BlochFigure("bob")
        self.ui.bloch_space.addWidget(self.bloch1)
        self.ui.bloch_space.addWidget(self.bloch2)
        self.ui.bloch_space.addWidget(self.bloch3)

        self.setWindowTitle("Kwantowa teleportacja")

        self.bloch_at_start = None

        self.success_message = "Teleportacja udana!"
        self.failure_message = "Ups, teleportacja nieudana..."

    @Slot()
    def create_simulator(self):
        self.sim = QuantumTeleportation("X" if self.teleportationSetup.ui.xGateRadio.isChecked() else "T",
                                        self.teleportationSetup.ui.phaseSlider.value() / 100.0)

        self.ui.setup_button.setEnabled(False)
        self.ui.step_button.setEnabled(True)
        self.teleportationSetup.setVisible(False)

    def update_ui(self, sim_state: SparseSimulatorStep, entangled_list: Tuple[Qid]):
        self.bloch1.update_plot(sim_state.bloch_vector_of(self.sim.qubits["msg"]),
                                self.sim.qubits["msg"] in entangled_list)
        self.bloch2.update_plot(sim_state.bloch_vector_of(self.sim.qubits["alice"]),
                                self.sim.qubits["alice"] in entangled_list)
        self.bloch3.update_plot(sim_state.bloch_vector_of(self.sim.qubits["bob"]),
                                self.sim.qubits["bob"] in entangled_list)


class DeutschSequenceValidator(QValidator):

    _regexp = QRegularExpression("^[1-8]{8}$")
    _partial_regexp = QRegularExpression("[1-8]*")

    def __init__(self):
        super(DeutschSequenceValidator, self).__init__()

    def validate(self, arg__1: str, arg__2: int) -> object:
        has_repeats = True in map(lambda x: x > 1, [arg__1.count(x) for x in ["1", "2", "3", "4", "5", "6", "7", "8"]])

        if not DeutschSequenceValidator._regexp.match(arg__1).hasMatch():
            if DeutschSequenceValidator._partial_regexp.match(arg__1).hasMatch():
                if has_repeats:
                    return QValidator.State.Invalid
                else:
                    return QValidator.State.Intermediate
            else:
                return QValidator.State.Invalid
        elif has_repeats:
            return QValidator.State.Invalid
        else:
            return QValidator.State.Acceptable


class DeutschSetup(QWidget):
    def __init__(self):
        super(DeutschSetup, self).__init__()
        self.ui = Deutsch_Setup()
        self.ui.setupUi(self)

        self.validator = DeutschSequenceValidator()
        self.ui.lineEdit.setValidator(self.validator)


class DeutschJozsaWindow(BasicSimulationWindow):
    def __init__(self):
        super(DeutschJozsaWindow, self).__init__()

        self.deutschSetup = DeutschSetup()
        self.ui.buttonsAndSetupLayout.addWidget(self.deutschSetup)

        self.bloch1 = BlochFigure("q1")
        self.bloch2 = BlochFigure("q2")
        self.bloch3 = BlochFigure("control")
        self.ui.bloch_space.addWidget(self.bloch1)
        self.ui.bloch_space.addWidget(self.bloch2)
        self.ui.bloch_space.addWidget(self.bloch3)

        self.setWindowTitle("Algorytm Deutscha-Jozsy")

        self.success_message = "Funkcja jest stała"
        self.failure_message = "Funkcja jest zbilansowana"

    @Slot()
    def create_simulator(self):
        if self.deutschSetup.ui.lineEdit.validator().validate(self.deutschSetup.ui.lineEdit.text(), 0)\
                == QValidator.State.Acceptable:
            oracle_def_str = self.deutschSetup.ui.lineEdit.text()
            array_def = [[1.0 if c == row_num else 0.0 for c in range(1, 9)] for row_num in map(int, oracle_def_str)]
            oracle_matrix = numpy.array(array_def, dtype=numpy.complex128)

            self.sim = DeutschJozsa(oracle_matrix)

            self.ui.setup_button.setEnabled(False)
            self.ui.step_button.setEnabled(True)
            self.deutschSetup.setVisible(False)
        else:
            self.add_line_to_log("Ups, twój ciąg cyfr jest niepełny. Popraw go i spróbuj jeszcze raz.")

    def update_ui(self, sim_state: SparseSimulatorStep, entangled_list: Tuple[Qid]):
        self.bloch1.update_plot(sim_state.bloch_vector_of(self.sim.qubits['q1']),
                                self.sim.qubits['q1'] in entangled_list)
        self.bloch2.update_plot(sim_state.bloch_vector_of(self.sim.qubits['q2']),
                                self.sim.qubits['q2'] in entangled_list)
        self.bloch3.update_plot(sim_state.bloch_vector_of(self.sim.qubits['control']),
                                self.sim.qubits['control'] in entangled_list)