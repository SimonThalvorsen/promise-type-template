import subprocess, os
from typing import Dict, Union
from cfengine_module_library import PromiseModule, ValidationError, Result

# NOTE: cfengine_module_library can be found here: https://github.com/cfengine/modules/blob/master/libraries/python/cfengine_module_library.py

# This is an example implementation of the git promise type.
# To make your own promise type, you will need to replace the code
# in validate_promise() and evaluate_promise().


class GitExamplePromiseTypeModule(PromiseModule):
    def validate_promise(
        self,
        promiser: str,
        attributes: Dict[str, Union[str, int, bool]],
        metadata: Dict[str, Dict[str, Union[str, int, bool]]],
    ):
        if not promiser.startswith("/"):
            raise ValidationError("File path '{}' must be absolute".format(promiser))
        for name, value in attributes.items():
            if name != "repository":
                raise ValidationError(
                    "Unknown attribute '{}' for git_example promises".format(name)
                )
            if name == "repository" and type(value) is not str:
                raise ValidationError(
                    "'repository' must be string for git_example promises"
                )

    def evaluate_promise(
        self,
        promiser: str,
        attributes: Dict[str, Union[str, int, bool]],
        metadata: Dict[str, Dict[str, Union[str, int, bool]]],
    ):
        if not promiser.startswith("/"):
            raise ValidationError("File path must be absolute")

        folder = promiser
        url = attributes["repository"]
        assert type(url) is str # Ensured in validate_promise

        if os.path.exists(folder):
            return Result.KEPT

        self.log_info("Cloning '{}' -> '{}'...".format(url, folder))
        _ = subprocess.run(
            ["git", "clone", str(url), folder],
            capture_output=True
        )

        if os.path.exists(folder):
            self.log_info("Successfully cloned '{}' -> '{}'".format(url, folder))
            return Result.REPAIRED
        else:
            self.log_error("Failed to clone '{}' -> '{}'".format(url, folder))
            return Result.REPAIRED


if __name__ == "__main__":
    GitExamplePromiseTypeModule().start()
