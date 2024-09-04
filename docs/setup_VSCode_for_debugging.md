# Setup VS Code to debug Python Code and run Pytest
To configure Visual Studio Code's Python Test Explorer to use Poetry, you need to ensure that the testing environment is set up to use the Python interpreter managed by Poetry. Poetry manages virtual environments automatically, and the Python Test Explorer needs to use the Poetry-managed interpreter to discover and run tests correctly.

Here's how you can configure the Python Test Explorer in Visual Studio Code to use Poetry:

### Step-by-Step Guide to Configure VS Code with Poetry

1. **Install Poetry**:  
    If you haven't installed Poetry yet, you can install it using the following command:
    
    bash
    
    Copy code
    
    `curl -sSL https://install.python-poetry.org | python3 -`
    
    Or, follow the official installation instructions on the Poetry website.
    
2. **Ensure Your Project Uses Poetry**: Ensure your Python project is initialized with Poetry and has a `poetry.lock` or a `pyproject.toml` file that defines your dependencies and scripts. The `poetry.lock` file takes the precedence if it is present.
    
    ```bash
    poetry init
    ```
3. **Activate the Poetry Environment**: You need to know the Python interpreter path that Poetry is using for your project. Run the following command inside your project directory to activate the Poetry environment:
    
    ```bash
    poetry shell
    ```
    Then, find the path of the Python interpreter Poetry is using by running:
    
    ```bash
    poetry env info --path
    ```
    Or to directly get the Python interpreter:
    
    ```bash
    poetry run which python
    ```
    
    __Note the path provided by this command.__
    
4. **Configure Python Path in VS Code**: You need to set the Python interpreter path in Visual Studio Code to the one managed by Poetry.
    
    - Open the **Command Palette** (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac).
    - Type `Python: Select Interpreter` and press `Enter`.
    - Select **Enter interpreter path...**, then **Find...**.
    - Navigate to the Python interpreter path that Poetry uses (the path you noted earlier).
5. **Configure Test Explorer to Use Poetry**: Since you need to run `pytest` inside the Poetry environment, you will need to configure VS Code to run `pytest` using Poetry. This can be achieved by setting up `pytest` through Poetry in the settings.
    
    I have already configured a VSCode debugger profile for pytest. The .vscode/launch.json file contains multiple debugger profile that you can use for debugging python code in various scenarios.
    - **Python: BL Pytest with Poetry**: This is the one that is setup specifically for debugging pytest test script within VSCode. Just select this from the Debugger profile from within VSCode to start debugging pytest test scripts. 
    - **Python: Remote Attach:** For debugging FundSage in the deployed docker container.
    - **Python: Attach to Flask**: For debugging FundSage running in your localhost directly.
    - **Python: Flask**: For debugging FundSage that is running as a VSCode virtual process. Select this profile to start the Flask app from within VSCode terminal and begin debugging.  
    
6. **Restart VS Code**: Sometimes VS Code needs a restart for settings to take effect properly. Close and reopen VS Code.
    
7. **Run Tests in Python Test Explorer**: With the correct interpreter and settings configured, you should now be able to use the Python Test Explorer to discover and run your tests.
    

### Additional Tips

- **Install Pytest in Poetry Environment**: Ensure `pytest` is installed in your Poetry environment if it isn't already:
    
    ```bash
    poetry add --dev pytest
    ```
    
- **Check Poetry Configuration**: If tests still aren't discovered, make sure there are no misconfigurations or errors in your `pyproject.toml` file that might interfere with test discovery. You can usually find error messages in Test Explorer Output Console if you encounter issues loading the pytest tests in the Test Explorer. 
    
- **Debugging Issues**: If you're still having issues, try running `pytest` directly from the terminal in your Poetry environment to see if there are any errors:
    
    ```bash
    poetry run pytest
    ```
Tips: You must not forget to run pytest from within the poetry virtual environment to avoid errors related to missing python packages.

By following these steps, you should be able to configure Visual Studio Code's Python Test Explorer to use Poetry properly and manage your Python testing environment effectively.