1. Creating the virtual env
    1.1. Pre-requisits:
        1. sudo apt install python3-venv
    1.2. python3 -m venv .venv
    1.3. source .venv/bin/activate
    1.4. deactivate

2. Install the requirements from the requirements,txt
    pip install -r requirements.txt

3. After installing the packages, you need to register your virtual environment as a Jupyter kernel:
    python -m ipykernel install --user --name=your_env_name
Replace "your_env_name" with a descriptive name for your environment

4. Creating the audio recorder component (for python) or we can use the android recorder API to do so aswell (simply records audio in .mp3 format)

5. Created the transcripter using the Whisper-small model(~1GB space)

6. Creating the Transcripter_API.

