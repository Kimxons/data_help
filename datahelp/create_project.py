"""
Datahelp: A Python library for common data science project utilities.

Author: {__author__}
Contact: {__email__}
"""

import json
import pickle
from pathlib import Path

import joblib
from __version__ import __author__, __author_email__
from custom_logger import Logger

from datahelp.utils import _get_path

# __author__ = "Meshack Kitonga"
# __email__ = "kitongameshack9@gmail.com"

logger = Logger(logger_name="dh_logger", filename="logs.log")


def create_directory(path: Path):
    """Create a directory if it does not exist already."""
    path.mkdir(parents=True, exist_ok=True)


def create_project(project_name: str):
    """
    Creates a standard data science project directory structure.

    Parameters:
        project_name (str): Name of the directory to contain folders.

    Returns:
        None
    """
    # Create project directories
    base_path = Path.cwd() / project_name
    data_path = base_path / "datasets"
    processed_path = data_path / "processed"
    raw_path = data_path / "raw"
    output_path = base_path / "outputs"
    models_path = output_path / "models"
    src_path = base_path / "src"
    scripts_path = src_path / "scripts"
    ingest_path = scripts_path / "ingest"
    preparation_path = scripts_path / "preparation"
    modeling_path = scripts_path / "modeling"
    test_path = scripts_path / "test"
    notebooks_path = src_path / "notebooks"

    # The project directories
    dirs = [
        base_path,
        data_path,
        processed_path,
        raw_path,
        output_path,
        models_path,
        src_path,
        scripts_path,
        ingest_path,
        preparation_path,
        modeling_path,
        test_path,
        notebooks_path,
    ]

    for directory in dirs:
        create_directory(directory)

    # Project config settings
    config = {
        "description": "Holds the project config settings",
        "base_path": str(base_path),
        "data_path": str(data_path),
        "processed_data_path": str(processed_path),
        "raw_data_path": str(raw_path),
        "output_path": str(output_path),
        "models_path": str(models_path),
    }

    config_path = base_path / ".datahelprc"
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)

    readme_path = base_path / "README.txt"
    with open(readme_path, "w") as readme:
        readme.write("Creates a standard data science project directory structure.")

    logger.info(f"Project created successfully in {base_path}")


def model_save(model, name="model", method="joblib"):
    """
    Save a trained machine learning model in the models folder.

    Parameters:
        model: binary file, Python object
            Trained model file to save in the models folder.
        name: str, optional (default='model')
            Name of the model to save it with.
        method: str, optional (default='joblib')
            Format to use in saving the model. It can be one of ['joblib', 'pickle', 'keras'].

    Returns:
        None
    """
    if model is None:
        raise ValueError("Expecting a binary model file, got 'None'")

    SUPPORTED_METHODS = {
        "joblib": joblib.dump,
        "pickle": pickle.dump,
        # "keras": tf.keras.models.save_model,
    }

    if method not in SUPPORTED_METHODS:
        raise ValueError(
            f"Method {method} not supported. Supported methods are: {list(SUPPORTED_METHODS.keys())}"
        )

    try:
        model_path = _get_path("modelpath")
        filename = f"{model_path}/{name}.{method}"

        SUPPORTED_METHODS[method](model, filename)

        logger.info(f"Model saved successfully to {filename}")
    except FileNotFoundError:
        msg = (
            f"Models folder does not exist. Saving model to the {name} folder. "
            f"It is recommended that you start your project using datahelp's start_project function"
        )
        logger.info(msg)

        filename = f"{name}.{method}"

        SUPPORTED_METHODS[method](model, filename)

        logger.info(f"Model saved successfully to {filename}")
    except PermissionError as e:
        logger.error(
            f"Permission error while saving model. Check file permissions. {e}"
        )
    except Exception as e:
        logger.error(f"Failed to save model due to {e}")


__doc__ = __doc__.format(author=__author__, email=__author_email__)
create_project.__doc__ = create_project.__doc__.format(
    author=__author__, email=__author_email__
)
model_save.__doc__ = model_save.__doc__.format(
    author=__author__, email=__author_email__
)
