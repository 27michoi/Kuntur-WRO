# Step 2


import importlib
import os
import subprocess
import sys


# Helper function for recording test results
def print_result(test_name, passed, error_message=None):
    """
    Prints the result of an import or environment test.

    Parameters:
        test_name (str):
            Name of the test.

        passed (bool):
            Whether the test passed.

        error_message (str, optional):
            Error message produced if the test failed.
    """

    if passed:
        print(f"\n{test_name}: Pass")
    else:
        print(f"\n{test_name}: Fail")

        if error_message:
            print(f"Error: {error_message}")


# Check the current project directory
def check_project_directory():
    """
    Checks whether the current directory appears to be the project's
    root directory.

    The project should contain folders such as:

        classes/
        utils/
    """

    print("\nChecking current project directory")

    current_directory = os.getcwd()

    print(f"Current directory: {current_directory}")

    classes_exists = os.path.isdir("classes")
    utils_exists = os.path.isdir("utils")

    if classes_exists and utils_exists:
        print_result(
            "Project directory check",
            True
        )
        return True

    print_result(
        "Project directory check",
        False,
        "Could not find both 'classes' and 'utils' folders."
    )

    print(
        "\nMake sure this script is being run from the project root."
        "\nFor example:"
        "\ncd ~/Projects/WRO2026-CLM/code/XX_2025_package"
    )

    return False


# Check Python information
def check_python_version():
    """
    Prints the Python version and executable currently being used.
    """

    print("\nChecking Python information")

    try:
        version_result = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True
        )

        executable_result = subprocess.run(
            ["which", "python3"],
            capture_output=True,
            text=True
        )

        if version_result.returncode == 0:
            print(f"Python version: {version_result.stdout.strip()}")
        else:
            print("Could not determine the Python version.")

        if executable_result.returncode == 0:
            print(
                f"Python executable: "
                f"{executable_result.stdout.strip()}"
            )
        else:
            print("Could not determine the Python executable.")

        if version_result.returncode == 0:
            print_result(
                "Python 3 availability",
                True
            )
            return True

        print_result(
            "Python 3 availability",
            False
        )
        return False

    except FileNotFoundError as error:
        print_result(
            "Python 3 availability",
            False,
            str(error)
        )
        return False


# Test an individual import
def test_import(module_name, display_name=None):
    """
    Attempts to import a Python module.

    Parameters:
        module_name (str):
            Import path used by Python.

        display_name (str, optional):
            Name displayed in the test output.

    Returns:
        bool:
            True if the import succeeds.
            False if the import fails.
    """

    if display_name is None:
        display_name = module_name

    print(f"\nTesting import: {display_name}")

    try:
        importlib.import_module(module_name)

        print_result(
            f"{display_name} import",
            True
        )

        return True

    except Exception as error:
        print_result(
            f"{display_name} import",
            False,
            str(error)
        )

        return False


# Test a specific object from a module
def test_from_import(module_name, object_name, display_name=None):
    """
    Attempts to import a specific object from a Python module.

    Parameters:
        module_name (str):
            Module containing the object.

        object_name (str):
            Object to import from the module.

        display_name (str, optional):
            Name displayed in the test output.

    Returns:
        bool:
            True if the import succeeds.
            False if the import fails.
    """

    if display_name is None:
        display_name = f"{object_name} from {module_name}"

    print(f"\nTesting import: {display_name}")

    try:
        module = importlib.import_module(module_name)
        getattr(module, object_name)

        print_result(
            f"{display_name} import",
            True
        )

        return True

    except Exception as error:
        print_result(
            f"{display_name} import",
            False,
            str(error)
        )

        return False


# Test the basic external libraries
def test_basic_external_imports():
    """
    Tests the basic external libraries used by the project:

        cv2
        numpy
        serial
    """

    print("\nTesting basic external libraries")

    results = []

    results.append(
        test_import(
            "cv2",
            "OpenCV (cv2)"
        )
    )

    results.append(
        test_import(
            "numpy",
            "NumPy"
        )
    )

    results.append(
        test_import(
            "serial",
            "PySerial (serial)"
        )
    )

    return all(results)


# Test the Picamera2 library
def test_picamera2_import():
    """
    Tests:

        from picamera2 import Picamera2

    This only checks whether the Python module can be imported.
    It does not test whether the physical camera can capture an image.
    """

    print("\nTesting Picamera2")

    return test_from_import(
        "picamera2",
        "Picamera2",
        "Picamera2"
    )


# Test the project's CameraManager import
def test_camera_manager_import():
    """
    Tests:

        from classes.camera_manager import CameraManager
    """

    print("\nTesting CameraManager")

    return test_from_import(
        "classes.camera_manager",
        "CameraManager",
        "CameraManager"
    )


# Test the main project imports
def test_project_imports():
    """
    Tests the main imports required by the project's main program.

    The test imports the modules without starting the full robot program.
    """

    print("\nTesting project imports")

    results = []

    results.append(
        test_from_import(
            "utils.image_transform_utils",
            "ImageTransformUtils",
            "ImageTransformUtils"
        )
    )

    results.append(
        test_from_import(
            "classes.image_algoriths",
            "ImageAlgorithms",
            "ImageAlgorithms"
        )
    )

    results.append(
        test_from_import(
            "classes.context_manager",
            "ContextManager",
            "ContextManager"
        )
    )

    results.append(
        test_from_import(
            "classes.lap_tracker",
            "LapTracker",
            "LapTracker"
        )
    )

    results.append(
        test_from_import(
            "utils.enums",
            "Direction",
            "Direction"
        )
    )

    results.append(
        test_from_import(
            "utils.enums",
            "StartPosition",
            "StartPosition"
        )
    )

    results.append(
        test_from_import(
            "utils.image_drawing_utils",
            "ImageDrawingUtils",
            "ImageDrawingUtils"
        )
    )

    results.append(
        test_from_import(
            "classes.arduino_comms",
            "ArduinoComms",
            "ArduinoComms"
        )
    )

    return all(results)


# Troubleshooting
def print_troubleshooting():
    """
    Prints troubleshooting instructions if one or more tests fail.
    """

    print("\nTroubleshooting")

    print(
        "\nA. Identify the exact failing import"
        "\nDo not immediately install multiple packages."
        "\nCheck which specific import produced the error."
    )

    print(
        "\nB. If an external library is missing"
        "\nRecord the complete error message, such as:"
        "\nModuleNotFoundError: No module named '...'"
        "\nThen identify the specific missing dependency before"
        "\ninstalling or changing anything."
    )

    print(
        "\nC. If a project module cannot be found"
        "\nCheck the current directory and confirm that the project"
        "\ncontains the required folders, including:"
        "\n- classes/"
        "\n- utils/"
    )

    print(
        "\nD. If CameraManager fails but individual libraries succeed"
        "\nRecord the complete error message."
        "\nThe problem may be caused by an additional project-level"
        "\ndependency imported by camera_manager.py."
    )




def main():

    print("\nStep 2: Python Imports Test")

    all_results = []

    # Check that Python 3 is available.
    python_available = check_python_version()
    all_results.append(python_available)

    # Check that the script is being run from the project root.
    correct_directory = check_project_directory()
    all_results.append(correct_directory)

    # Stop the project import tests if the required project folders
    # are not available from the current directory.

    if not correct_directory:

        print(
            "\nProject imports were not tested because the required"
            "\nproject directory structure was not found."
        )

        print_troubleshooting()

        return
      
    basic_imports = test_basic_external_imports()
    all_results.append(basic_imports)

    picamera2_import = test_picamera2_import()
    all_results.append(picamera2_import)

    camera_manager_import = test_camera_manager_import()
    all_results.append(camera_manager_import)
  
    project_imports = test_project_imports()
    all_results.append(project_imports)

    if all(all_results):

        print("\nStep 2 result: Pass")

        print(
            "\nAll required Python imports were successful."
            "\nThe project can proceed to the next testing step."
        )

    else:

        print("\nStep 2 result: Fail")

        print(
            "\nOne or more imports or environment checks failed."
            "\nRecord the exact error message before making changes."
        )

        print_troubleshooting()



if __name__ == "__main__":
    main()

