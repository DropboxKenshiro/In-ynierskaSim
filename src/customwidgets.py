from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy


class BlochFigure(FigureCanvasQTAgg):
    def __init__(self, title: str = ""):
        self.figure = Figure(figsize=(5, 3))
        self.subplot: Axes3D = self.figure.add_subplot(111, projection='3d')
        self.title = title

        super(BlochFigure, self).__init__(self.figure)

    def update_plot(self, bloch_vector: numpy.ndarray, is_entangled: bool):
        filtered_bloch = bloch_vector.copy()
        filtered_bloch = numpy.around(filtered_bloch, 3)

        self.subplot.clear()

        self.subplot.set_xlim(-1, 1)
        self.subplot.set_ylim(-1, 1)
        self.subplot.set_zlim(-1, 1)

        self.subplot.text(0, 0, 1, '|0>')
        self.subplot.text(0, 0, -1, '|1>')

        if is_entangled:
            self.subplot.set_title(f"{self.title}\nSplątany")
            self.subplot.text(0, 0, 0, 'Splątany')
        else:
            self.subplot.set_title(f"{self.title}\n{str(numpy.around(bloch_vector, 3))}")
            self.subplot.quiver(0, 0, 0, *filtered_bloch)

        self.draw()
