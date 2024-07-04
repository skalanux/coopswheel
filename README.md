# Spin the Wheel!!
Simple quiz game using OpenCV for user input.

To setup and run the program follow the steps below:
1. Create a Python virtual environment and activate it (optional):
```bash
python -m venv env
env\bin\activate
```
2. Install neccessary libraries:
```bash
pip install -r requirements.txt
```

3. Create a Fifo:
```bash
mkfifo gesture
```

4. Run gesture capture:
```bash
python gestures.py
```

5. Run wheel:
```bash
python wheel.py
```
