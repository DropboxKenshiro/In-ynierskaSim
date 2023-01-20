from abc import abstractmethod
from typing import Tuple, Optional
from math import sqrt, isclose
import logging
import numpy
from cirq import GridQubit, StepResult, CNOT, CZ, H, X, T, Z, measure, Circuit, Simulator, InsertStrategy, \
    SparseSimulatorStep, Qid, NamedQubit, Gate
from entdetector.entdetector import schmidt_decomposition_for_vector_pure_state


def detect_entanglement_bipartite(result: SparseSimulatorStep) -> bool:
    coefficients, eg1, eg2 = schmidt_decomposition_for_vector_pure_state(result.state_vector(), (2, 2))
    rounded_coeffs = numpy.around(coefficients, 6)

    logging.info(f"Współczynniki Schmidta: {coefficients}")

    return not (numpy.count_nonzero(rounded_coeffs == 1.0) == 1 and
                numpy.count_nonzero(rounded_coeffs == 0.0) == numpy.size(rounded_coeffs) - 1)


def detect_entanglement_tripartite(result: SparseSimulatorStep, qubits: Tuple[Qid, ...]) -> \
        Tuple[bool, str, Optional[Tuple[Qid, ...]]]:
    # density matrices needed to compute I_n
    rhoC = result.density_matrix_of([qubits[2]])
    rhoAB = result.density_matrix_of([qubits[0], qubits[1]])
    rhoA = result.density_matrix_of([qubits[0]])
    rhoB = result.density_matrix_of([qubits[1]])

    # now compute I_n
    i1 = float(numpy.trace(rhoA @ rhoA))
    i2 = float(numpy.trace(rhoB @ rhoB))
    i3 = float(numpy.trace(rhoC @ rhoC))
    tensorAB = numpy.kron(rhoA, rhoB)
    i4 = float(numpy.trace(tensorAB @ rhoAB))

    # i5 is little more complicated...
    cstate = result.state_vector().reshape((2, 2, 2))
    hdet = ((cstate[0][0][0] ** 2) * (cstate[1][1][1] ** 2)) + ((cstate[0][0][1] ** 2) * (cstate[1][1][0] ** 2)) + \
           ((cstate[0][1][0] ** 2) * (cstate[1][0][1] ** 2)) + ((cstate[1][0][0] ** 2) * (cstate[0][1][1] ** 2)) - \
        2 * cstate[0][0][0] * cstate[0][0][1] * cstate[1][1][0] * cstate[1][1][1] - \
        2 * cstate[0][0][0] * cstate[0][1][0] * cstate[1][0][1] * cstate[1][1][1] - \
        2 * cstate[0][0][0] * cstate[0][1][1] * cstate[1][0][0] * cstate[1][1][1] - \
        2 * cstate[0][0][1] * cstate[0][1][0] * cstate[1][0][1] * cstate[1][1][0] - \
        2 * cstate[0][0][1] * cstate[0][1][1] * cstate[1][1][0] * cstate[1][0][0] - \
        2 * cstate[0][1][0] * cstate[0][1][1] * cstate[1][0][1] * cstate[1][0][0] + \
        4 * cstate[0][0][0] * cstate[0][1][1] * cstate[1][0][1] * cstate[1][1][0] + \
        4 * cstate[0][0][1] * cstate[0][1][0] * cstate[1][0][0] * cstate[1][1][1]
    i5 = abs(hdet) ** 2

    # having i's, let's compute j's
    j1 = (1/4) * (1 + i1 - i2 - i3 - 2 * sqrt(i5))
    j2 = (1/4) * (1 - i1 + i2 - i3 - 2 * sqrt(i5))
    j3 = (1/4) * (1 - i1 - i2 + i3 - 2 * sqrt(i5))
    j4 = sqrt(i5)
    j5 = (1/4) * (3 - 3 * i1 - 3 * i2 - i3 + 4 * i4 - 2 * sqrt(i5))

    # due to precision errors, we would round down j's to 6 decimal places. It's enough for our purposes
    rj1 = round(j1, 6)
    rj2 = round(j2, 6)
    rj3 = round(j3, 6)
    rj4 = round(j4, 6)
    rj5 = round(j5, 6)

    # checking all the possibilities
    # case 1: product state, fully separable
    if isclose(rj1, 0.0) and isclose(rj2, 0.0) and isclose(rj3, 0.0) and isclose(rj4, 0.0) and isclose(rj5, 0.0):
        return False, "fully_separable", None
    # case 2a: B and C are bipartite entangled
    elif not isclose(rj1, 0.0) and isclose(rj2, 0.0) and isclose(rj3, 0.0) and isclose(rj4, 0.0) and isclose(rj5, 0.0):
        return True, "bipartite", (qubits[1], qubits[2])
    # case 2b: A and C are bipartite entangled
    elif isclose(rj1, 0.0) and not isclose(rj2, 0.0) and isclose(rj3, 0.0) and isclose(rj4, 0.0) and isclose(rj5, 0.0):
        return True, "bipartite", (qubits[0], qubits[2])
    # case 2c: A and B are bipartite entangled
    elif isclose(rj1, 0.0) and isclose(rj2, 0.0) and not isclose(rj3, 0.0) and isclose(rj4, 0.0) and isclose(rj5, 0.0):
        return True, "bipartite", (qubits[0], qubits[1])
    # case 3: any other kind of tripartite entanglement
    else:
        return True, "tripartite", (qubits[0], qubits[1], qubits[2])


class SteppingSimInterface:
    def __init__(self, names: Tuple[str, ...]):
        # initialize qubits
        self.qubits: dict[str, NamedQubit] = {n: NamedQubit(n) for n in names}

        self.circuit = Circuit(self.circuit_definition(), strategy=InsertStrategy.NEW)
        logging.info(f"Początkowy układ kwantowy:\n{self.circuit}")
        self.bloch_states = []
        self._sim = Simulator(dtype=numpy.complex128, split_untangled_states=False)
        self._sim_iter = self._sim.simulate_moment_steps(self.circuit)
        self._desc = self.description_sequence()
        self._measurements = self.measurements()

        self.currently_entangled = set()

    @abstractmethod
    def circuit_definition(self):
        pass

    @abstractmethod
    def description_sequence(self):
        pass

    @abstractmethod
    def measurements(self):
        pass

    @abstractmethod
    def check_results(self, final_step: Optional[SparseSimulatorStep] = None):
        pass

    @abstractmethod
    def detect_entanglement(self, simulation_step: SparseSimulatorStep) -> Tuple[Qid]:
        pass

    def step(self) -> (SparseSimulatorStep, str, Optional[Tuple[Qid]]):
        try:
            logging.info("--- Następny krok ---")
            sim_step = next(self._sim_iter)
            entangled = self.detect_entanglement(sim_step)
            bloch_vectors = [numpy.around(sim_step.bloch_vector_of(q), 6) for q in self.qubits.values()]
            self.bloch_states.append(bloch_vectors)
            logging.info(f"Wektor stanu dla bieżącego kroku: {sim_step.dirac_notation(4)}")
            logging.info(f"Wektory Blocha dla bieżącego kroku: {bloch_vectors}")
            logging.info(f"Macierz gęstości dla bieżącego kroku: {sim_step.density_matrix_of()}")

            measured = next(self._measurements)
            if entangled is not None:
                for qid in entangled:
                    self.currently_entangled.add(qid)
            if measured is not None and measured in self.currently_entangled:
                self.currently_entangled.remove(measured)
                if len(self.currently_entangled) <= 1:  # one qubit can't be entangled with itself
                    self.currently_entangled.clear()

            logging.info(f"W bieżącym kroku splątane są kubity: {self.currently_entangled}")

            yield sim_step, next(self._desc), self.currently_entangled
        except StopIteration:
            return

    def simulate_at_once(self) -> None:
        simulator = Simulator()

        for i, step in enumerate(simulator.simulate_moment_steps(self.circuit)):
            print(f'{i}: {step.state_vector()}')


class SimpleEntanglement(SteppingSimInterface):
    def __init__(self):
        super().__init__(("alice", "bob"))

    def circuit_definition(self):
        yield H(self.qubits["alice"])
        yield CNOT(self.qubits["alice"], self.qubits["bob"])
        yield Z(self.qubits["alice"])
        yield Z(self.qubits["bob"])
        yield measure(self.qubits["alice"])
        yield measure(self.qubits["bob"])

    def description_sequence(self):
        yield "Ustawienie kubitów w stan Bella"
        yield "Ustawienie kubitów w stan Bella"
        yield "Operacja na kubicie splątanym Alicji"
        yield "Operacja na kubicie splątanym Boba"
        yield "Pomiar kubitu Alicji"
        yield "Pomiar kubitu Boba"

    def measurements(self):
        yield None
        yield None
        yield None
        yield None
        yield self.qubits["alice"]
        yield self.qubits["bob"]

    def detect_entanglement(self, simulation_step: SparseSimulatorStep) -> Tuple[Qid] | Tuple:
        return self.qubits["alice"], self.qubits["bob"] if detect_entanglement_bipartite(simulation_step) else ()

    def check_results(self, final_step: Optional[SparseSimulatorStep] = None):
        return True  # there is nothing to check here


class QuantumTeleportation(SteppingSimInterface):
    def __init__(self, what_gate: str, phase: float):
        if what_gate == "X":
            self.setup_gate = X
        else:
            self.setup_gate = T
        self.phase = phase

        logging.info(f"Początkowy układ kwantowy: {self.setup_gate} ** {self.phase}")

        super().__init__(("msg", "alice", "bob"))

    def circuit_definition(self):
        # initialize msg to some arbitrary value
        # this might change
        init_gate = self.setup_gate ** self.phase
        yield init_gate(self.qubits["msg"])
        # initialize qubits 1 and 2 into Bell state
        yield H(self.qubits["alice"])
        yield CNOT(self.qubits["alice"], self.qubits["bob"])
        # superpose qubit to be teleported
        yield CNOT(self.qubits["msg"], self.qubits["alice"])
        yield H(self.qubits["msg"])
        # measure a and b
        yield measure(self.qubits["msg"])
        yield measure(self.qubits["alice"])
        # apply recovering process, the measured qubits
        # would simply be states with sure probability
        yield CNOT(self.qubits["alice"], self.qubits["bob"])
        yield CZ(self.qubits["msg"], self.qubits["bob"])

    def description_sequence(self):
        yield "Ustawianie wartości początkowej kubitów"
        yield "Inicjalizacja kubitów Alicji i Boba w stan Bella"
        yield "Inicjalizacja kubitów Alicji i Boba w stan Bella"
        yield "Wprowadzenie kubitu teleportowanego w stan superpozycji"
        yield "Wprowadzenie kubitu teleportowanego w stan superpozycji"
        yield "Pomiar kubitów Alicji i Boba"
        yield "Pomiar kubitów Alicji i Boba"
        yield "Aplikacja korekcji stanu"
        yield "Aplikacja korekcji stanu"

    def measurements(self):
        yield None
        yield None
        yield None
        yield None
        yield None
        yield self.qubits["msg"]
        yield self.qubits["alice"]
        yield None
        yield None

    def detect_entanglement(self, simulation_step: SparseSimulatorStep) -> Tuple[Qid]:
        are_entangled, what_kind, what_entangled = detect_entanglement_tripartite(simulation_step, tuple(self.qubits.values()))
        if are_entangled:
            logging.info(f"Wykryto splątanie rodzaju: {what_kind}")
            return what_entangled

    def check_results(self, final_step: Optional[SparseSimulatorStep] = None) -> bool:
        return (self.bloch_states[0][0] == self.bloch_states[-1][2]).all()


class DeutschJozsaOracle3Q(Gate):
    def __init__(self, unitary: numpy.ndarray):
        super(DeutschJozsaOracle3Q, self)
        self.unitary = unitary

    def _num_qubits_(self) -> int:
        return 3

    def _unitary_(self):
        return self.unitary

    def _circuit_diagram_info_(self, args):
        return "█", "Uf", "█"


class DeutschJozsa(SteppingSimInterface):
    def __init__(self, oracle: numpy.ndarray):
        self.oracle = DeutschJozsaOracle3Q(unitary=oracle)
        super().__init__(("q1", "q2", "control"))

    def circuit_definition(self):
        # initialize control qubit into |1>
        yield X(self.qubits["control"])
        # initial hadamard operation
        yield H(self.qubits["q1"])
        yield H(self.qubits["q2"])
        yield H(self.qubits["control"])
        # oracle definition
        yield self.oracle.on(self.qubits["q1"], self.qubits["q2"], self.qubits["control"])
        # the defiltering step
        yield H(self.qubits["q1"])
        yield H(self.qubits["q2"])
        yield H(self.qubits["control"])
        # final measurement
        yield measure(self.qubits["q1"])
        yield measure(self.qubits["q2"])
        yield measure(self.qubits["control"])

    def description_sequence(self):
        yield "Ustawienie kubitu kontrolnego w stan |1>"
        yield "Zadziałanie na wszystkie kubity bramką Hadamarda"
        yield "Zadziałanie na wszystkie kubity bramką Hadamarda"
        yield "Zadziałanie na wszystkie kubity bramką Hadamarda"
        yield "Działanie wyroczni"
        yield "Ponowne działanie bramkami Hadamarda"
        yield "Ponowne działanie bramkami Hadamarda"
        yield "Ponowne działanie bramkami Hadamarda"
        yield "Końcowy pomiar"
        yield "Końcowy pomiar"
        yield "Końcowy pomiar"

    def measurements(self):
        yield ()
        yield ()
        yield ()
        yield ()
        yield ()
        yield ()
        yield ()
        yield ()
        yield self.qubits["q1"]
        yield self.qubits["q2"]
        yield self.qubits["control"]

    def detect_entanglement(self, simulation_step: SparseSimulatorStep) -> Tuple[Qid]:
        are_entangled, what_kind, what_entangled = detect_entanglement_tripartite(simulation_step,
                                                                                  tuple(self.qubits.values()))
        if are_entangled:
            logging.info(f"Wykryto splątanie rodzaju: {what_kind}")
            return what_entangled

    # warning: in this case, success means that function represented by oracle is constant
    # otherwise it's balanced
    def check_results(self, final_step: Optional[SparseSimulatorStep] = None):
        measurements = final_step.measurements
        return measurements["q1"][0] == 0 and measurements["q2"][0] == 0

