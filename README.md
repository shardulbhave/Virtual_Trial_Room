
---

# Virtual Trial Room

**Virtual Trial Room for Online Shopping Platforms**  
This project allows users to try on clothes virtually using their webcam, providing a simple demo for online shopping applications.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
The Virtual Trial Room simulates a fitting experience for users shopping online. Using a webcam, the program captures live footage and overlays clothing items (shirts and pants) onto the user's body in real-time.

---

## Features
- Real-time body tracking using a webcam
- Clothing overlays (shirts and pants) for virtual trials
- Support for both male and female models
- Simple and intuitive interface

---

## Requirements
To run this project, you will need the following:
- Python 3.x
- A webcam (integrated or external)
- Libraries: 
  - Mediapipe
  - OpenCV
  - Cvzone

---

## Installation

Follow these steps to set up the project locally.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shardulbhave/Virtual_Trial_Room.git
   cd Virtual_Trial_Room
   ```

2. **Set up a Python virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install the required libraries**:
   Run the following command to install all the necessary libraries:
   ```bash
   pip install mediapipe opencv-python-headless cvzone
   ```

---

## How to Run

Follow these steps to run the Virtual Trial Room project:

1. **Download all files**:  
   Clone the repository or download all the project files from the repository.

2. **Modify the file paths**:  
   Open `VTR.py` in your IDE (we recommend PyCharm).  
   Change the file paths for the shirt and pant images for both male and female models (MalePants,MaleShirts,FemaleShirts & FemalePants). Additionally, provide paths for the button images (there are button images in 'Buttons' directory use malebutton.png , femalebutton.png & resetbutton.png ).

   Example:
   ```python
   shirtFolderPath_male = "path/to/MaleShirts"
   pantFolderPath_male = "path/to/FemaleShirts"
   shirtFolderPath_female = "path/to/FemaleShirts"
   pantFolderPath_female = "path/to/FemalePant"
   imgButtonMale = "path/to/Buttons/malebutton.png"
   imgButtonFemale = "path/to/Buttons/femalebutton.png"
   imgButtonReset = "path/to/Buttons/resetbutton.png"
   ```

3. **Run the program**:
   Once you've updated the file paths, run the program using your IDE or through the terminal:
   ```bash
   python "VTR.py"
   ```

---

## Usage
- After running the program, ensure your webcam is turned on.
- The program will detect your body and overlay the selected clothing items (shirts and pants) onto your body in real-time.
- You can switch between different clothing items (shirts, pants) by using the on-screen buttons.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
