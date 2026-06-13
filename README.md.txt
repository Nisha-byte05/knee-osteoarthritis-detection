# Knee Osteoarthritis Grading using ResNet18

## Overview
This project uses a ResNet18 deep learning model to classify Knee Osteoarthritis (OA) severity from X-ray images.

The model predicts OA grades ranging from 0 to 4 based on the severity of the disease.

## OA Grades
| Grade | Description |
|---------|------------|
| 0 | Normal |
| 1 | Doubtful OA |
| 2 | Mild OA |
| 3 | Moderate OA |
| 4 | Severe OA |

## Features
- Knee X-ray image classification
- Deep learning using ResNet18
- OA grade prediction (0–4)
- Automated severity assessment

## Technologies Used
- Python
- PyTorch
- ResNet18
- OpenCV
- NumPy
- Matplotlib

## Project Structure

```text
backend_knee_ortheo.ipynb
frontend_knee_ortheo.py
knee_oa_model.pth
outputs/
knee_gif.gif
```

## How to Run

1. Install required libraries.
2. Load the trained model.
3. Run the frontend application.
4. Upload a knee X-ray image.
5. Receive the predicted OA grade.

## Results

The model classifies knee X-ray images into five osteoarthritis severity levels (0–4).

## Author

Nisha Panneer