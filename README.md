# KSL Recognition System using MediaPipe
## Preliminaries
1.  Before beginning, you need to install MediaPipe on your machine.[ Here is the link to installing MediaPipe.](https://google.github.io/mediapipe/getting_started/install.html)
Make sure, when you are cloning the MediaPipe repo, to clone it into this directory.
2.  Copy the simple_run_graph_main.cc in the current directory and replace the one in mediapipe/mediapipe/examples/desktop
3.  Run `bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/multi_hand_tracking:multi_hand_tracking_tflite` to build the binaries.

## Work Flow
-   You will first need to build your training set. The training data is .mov clips and each class has it's respective folder, all stored under the test_data folder. 
The training data is currently in an S3 bucket.
-   You run train_sequential.py to start training. 
`execute_mediapipe_csv()` function is the function that will convert all data from `test_data` and extract landmarks, saving the csv to `csv_outputs`, 
and the annotated video at `test_data_annotated`. It then parses the csv files and prepares them for feeding into the model.
-   Three models are saved in `models` folder: 
      1.    Model with the highest validation accuracy,
      2.    Model with the lowest validation loss, and
      3.    General model saved after training.
-   Once the models are generated, `inference.py` is the script used to get predictions from the `test_videos` folder.

## Requirements
1.  MediaPipe
2.  Python 3.7
3.  Numpy
4.  Keras
5.  Tensorflow
6. OpenCV
7.  FFMPEG 
8.  Matplotlib
9.  Scikit-learn


## TL:DR
-   Install MediaPipe and then replace the `.cc` file with the one provided
-   Train using `train_sequential.py`
-   Make predictions using `inference.py`
