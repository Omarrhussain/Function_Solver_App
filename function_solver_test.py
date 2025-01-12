import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from function_solver import FunctionSolverApp


@pytest.fixture
def app(qtbot):
    """Fixture to initialize the application."""
    test_app = QApplication.instance() or QApplication([])
    window = FunctionSolverApp()
    qtbot.addWidget(window)
    return window


def test_input_validation(app, qtbot):
    """Test input validation for invalid function syntax."""
    app.function1_input.setText("5*x^3 + 2*x")
    app.function2_input.setText("invalid_function")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)
    assert "Invalid function syntax" in app.statusBar().currentMessage()


def test_intersection_finding(app, qtbot):
    """Test finding the intersection point."""
    app.function1_input.setText("x^2")
    app.function2_input.setText("2*x")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)
    assert app.ax.lines  # Check if plots are generated
    assert len(app.ax.collections) > 0  # Check if intersection point is plotted


def test_no_intersection(app, qtbot):
    """Test case where no intersection exists."""
    app.function1_input.setText("x^2 + 1")
    app.function2_input.setText("x^2 + 2")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)
    assert "No intersection point" in app.statusBar().currentMessage()