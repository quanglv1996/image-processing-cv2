# PyQt5 GUI Application

## Overview

This project is a PyQt5-based GUI application that allows users to interact with different tools for image processing and camera operations, such as:
- **HSV Filter**
- **Camera Calibration**
- **Sharpness Analyzer**

The user can select the desired mode using radio buttons and click on the "Apply" button to open a new window for the selected mode.

## Features

- **HSV Filter**: Provides a UI for users to apply HSV filtering to images.
- **Camera Calibration**: Allows users to perform camera calibration using images or live video feed.
- **Sharpness Analyzer**: Tool for analyzing the sharpness of an image or a video stream.
  
## Requirements

- Python 3.9+
- PyQt5

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. (Optional) Create a virtual environment to manage dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1. Ensure you have installed the dependencies listed in the `requirements.txt` file.
2. Run the main application:

    ```bash
    python main.py
    ```

3. The main window will open. Use the radio buttons to select a mode:
    - **HSV Filter**
    - **Camera Calibration**
    - **Sharpness Analyzer**

4. Click the "Apply" button to open the corresponding window.

## Usage

- **HSV Filter**: Use this tool to apply an HSV filter to your images and see how color adjustments affect the output.
- **Camera Calibration**: Calibrate your camera using a set of images or a live feed to improve accuracy in image capture.
- **Sharpness Analyzer**: Analyze the sharpness of an image or video feed to assess clarity and focus.

## Contributing

Feel free to contribute to the project by submitting issues or pull requests. Please make sure to follow the contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the PyQt5 and OpenCV communities for their resources and support.
