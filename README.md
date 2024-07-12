# pyperize: scalable no-code pipelines

## Overview
Build scalable no-code pipelines with pyperize.
- Pipes are assembled into pipelines in the UI without any code
- Pipes can be composed of any Python code
- Pipes can be installed/removed from pyperize as packages
- REST and WebSockets APIs to integrate with external apps
- Open source, anyone can create and share pipes
- Completely written in Python

## Usage

### Prequisites
- Linux
- Python ≥ 3.10

### Downloading extra packages
Download the desired packages from https://github.com/pyperize/

### Installing packages
For each package
1. Copy package into ```./packages/```
2. Edit ```./packages/__init__.py``` to import the package
3. Add the package name and instance to the ```PACKAGES``` global variable in ```./packages/__init__.py```

### Setup
- Make setup script executable: ```chmod 755 ./scripts/setup.sh```
- Run setup script: ```sh ./scripts/setup.sh```

### Run
- Enter venv: ```source ./venv/bin/activate```
- Run app (web, debug UI, no API): ```flet run -d -r --web --port 8000 main-ui.py```
- Run app (web, full): ```python main.py```

### Developing packages
- Create a subclass of ```src.package.Package``` defining the new package
- Check out https://github.com/pyperize/sample_package

## Project structure

    ./
    ├── assets/                     # Static assets (images, videos, etc.)
    ├── src/                        # Project source code
    │   ├── api/                    # API server
    │   ├── manager/                # Global object manager
    │   ├── package/                # Package management utilities
    │   ├── ui/                     # UI interfaces
    │   └── pipe/                   # Abstract pipe classes
    ├── scripts/                    # Convenience scripts
    │   ├── setup.sh                # Setup script
    │   └── install_requirements.sh # Script to recursively install all python requirements
    ├── packages/                   # Installed packages
    ├── test/                       # Testing scripts
    ├── main-ui.py                  # Entrypoint without API functionality
    ├── main.py                     # Entrypoint
    ├── requirements.txt            # Python dependencies
    └── README.md                   # This document

## Roadmap
1. YOLO training and inference pipes
2. Pipes refactoring
    1. Reference existing pipes in pipe selector
    2. Single Pipes to List Pipes
    3. Pipe filtering and validation
3. More premade pipes
    1. Output Video
    2. Multi
    3. Multi Process/Thread
    4. Data processing pipes
    5. YOLO evaluation pipes
4. Package manager
5. Extra UI functionality
    1. Data Page, Save & Load Data, Data Editor
    2. API Page
    3. Packages Page
    4. Settings Page
6. Pipe execution progress bar
7. Tests
8. Launcher, Grid Live View, Live Results
9. Update to FaceRecognition
    1. InsightFace model selector
    2. Refactoring
10. Update to LicensePlateRecognition
11. Update to InputVideo: ffmpegcv, ffmpeg GPU support, RTSP support, extra options for InputVideo
12. Save & load pipelines and configurations, copy & paste pipes, drag & drop
13. Templates
14. Manager API
15. Documentation, tooltip documentation

## Further extensions
- Dockerize

-----
