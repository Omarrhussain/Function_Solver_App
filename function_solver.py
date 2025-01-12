import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FunctionSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver and Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the status bar
        self.statusBar().showMessage("Ready")  # Initialize with a default message

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input fields for functions
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText("Enter first function of x, e.g., 5*x^3 + 2*x")
        self.layout.addWidget(self.function1_input)

        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText("Enter second function of x, e.g., 3*x^2 - 4*x")
        self.layout.addWidget(self.function2_input)

        # Solve and Plot button
        self.solve_button = QPushButton("Solve and Plot", self)
        self.solve_button.clicked.connect(self.solve_and_plot)
        self.layout.addWidget(self.solve_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def solve_and_plot(self):
        """Solve the functions and plot them."""
        try:
            # Get and validate user input
            func1_str = self.function1_input.text().strip()
            func2_str = self.function2_input.text().strip()
            if not func1_str or not func2_str:
                raise ValueError("Please enter both functions.")

            # Validate function syntax
            if not self._validate_function(func1_str) or not self._validate_function(func2_str):
                raise ValueError("Invalid function syntax. Supported operators: + - / * ^ log10() sqrt().")

            # Define the functions
            func1 = self._create_function(func1_str)
            func2 = self._create_function(func2_str)

            # Solve for intersection point
            x_vals = np.linspace(-10, 10, 1000)
            y1_vals = func1(x_vals)
            y2_vals = func2(x_vals)
            intersection_x = self._find_intersection(x_vals, y1_vals, y2_vals)

            if intersection_x is None:
                raise ValueError("No intersection point found within the range.")

            intersection_y = func1(intersection_x)

            # Plot the functions
            self.ax.clear()
            self.ax.plot(x_vals, y1_vals, label="Function 1")
            self.ax.plot(x_vals, y2_vals, label="Function 2")
            self.ax.scatter(intersection_x, intersection_y, color="red", label="Intersection")
            self.ax.annotate(
                f"({intersection_x:.2f}, {intersection_y:.2f})",
                (intersection_x, intersection_y),
                textcoords="offset points",
                xytext=(10, 10),
                ha="center",
            )
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()

            # Clear any previous error messages
            self.statusBar().showMessage("Ready")

        except ValueError as e:
            # Display the error message in the status bar
            self.statusBar().showMessage(str(e))

    def _validate_function(self, func_str):
        """Validate the function syntax."""
        # Check for allowed operators and functions
        allowed_pattern = re.compile(r"^[0-9x+\-*/^ ().log10sqrt]+$")
        return bool(allowed_pattern.match(func_str))

    def _create_function(self, func_str):
        """Create a lambda function from the input string."""
        # Replace ^ with ** for Python syntax
        func_str = func_str.replace("^", "**")
        # Define the function
        return lambda x: eval(func_str, {"x": x, "log10": np.log10, "sqrt": np.sqrt})

    def _find_intersection(self, x_vals, y1_vals, y2_vals):
        """Find the intersection point of the two functions."""
        diff = np.abs(y1_vals - y2_vals)
        idx = np.argmin(diff)
        if diff[idx] < 1e-1:  # Tolerance for intersection
            return x_vals[idx]
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionSolverApp()
    window.show()
    sys.exit(app.exec_())