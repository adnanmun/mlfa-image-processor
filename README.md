# Memorial Light Field Archive (MLFA) Preview Generator

This project provides a tool to generate preview images from high-resolution light field images. It extracts metadata from JSON configuration files and uses that data to produce preview images that help in quickly visualizing the contents without needing to download and process the full light field data.

## Prerequisites

- Python 3.6 or higher
- NumPy library
- OpenCV library

## Setup

To run the project locally, follow these steps:

1. Clone the repository:
```
git clone https://github.com/adnanmun/mlfa-image-processor
```

2. Navigate to the project directory:
```
cd mlfa-preview-generator
```

3. Install the required Python libraries:
  ```
  pip install numpy opencv-python
  ```

## Usage

1. Run the main script from the command line:
  ```
  python main.py
  ```

2. When prompted, enter the path to the input folder containing the light field images and configuration JSON files.

## Output

Generated images and JSON metadata are saved in the output directory. The script appends new metadata entries to the `config.json` file.

## Acknowledgements

This project builds upon the original work by Harsual. This version includes several modifications to improve functionality and user experience, while maintaining the core features developed by Harsual.
