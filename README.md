# Grounding DINO ROS2 (grounding\_dino\_ros)

[](https://docs.ros.org/en/humble/index.html)
[](https://www.python.org/)
[](https://pytorch.org/)

A ROS2 node for zero-shot object detection using Grounding DINO, compatible with ROS 2 Foxy/Humble/Iron.

This node subscribes to a camera image (`sensor_msgs/msg/Image`) and a text prompt (as a ROS2 parameter) to detect specified objects in real-time.

Detection results are published in the standard `vision_msgs/msg/Detection2DArray` format (ROI info) and as a processed `sensor_msgs/msg/Image` (for visualization).

## 1\. Node Features

  - **Zero-Shot Object Detection**: Detects any object specified by a natural language text prompt.
  - **Dynamic Prompt Reconfiguration**: The text prompt can be changed dynamically via ROS2 parameters without restarting the node.
  - **Standard ROS2 Interfaces**: Uses standard message types (`sensor_msgs`, `vision_msgs`) for easy integration with existing ROS2 systems (camera drivers, Rviz, etc.).

## 2\. Interface Specification

### Node Name

  - `grounding_dino_node`

### 📥 Subscriptions (Input)

  - **`~/input/image_raw`** (`sensor_msgs/msg/Image`)
      - The raw input image for detection.

### 📤 Publications (Output)

  - **`~/output/detections`** (`vision_msgs/msg/Detection2DArray`)
      - An array of detected objects. Includes bounding box (`bbox`), confidence score, and class name (`results.hypothesis.class_id`).
  - **`~/output/image_processed`** (`sensor_msgs/msg/Image`)
      - A copy of the input image with bounding boxes and labels drawn for visualization.

### 🔧 Parameters

  - **`text_prompt`** (string, default: `"a person . a chair"`)
      - The text prompt describing objects to detect. Use `.` (dot) to separate multiple classes.
      - **[Dynamically Reconfigurable]**
  - **`model_config_path`** (string)
      - Absolute path to the Grounding DINO model configuration file (`.py`).
  - **`model_checkpoint_path`** (string)
      - Absolute path to the Grounding DINO model weights file (`.pth`).
  - **`box_threshold`** (double, default: `0.35`)
      - Confidence threshold for bounding box detection.
  - **`text_threshold`** (double, default: `0.25`)
      - Confidence threshold for text-image feature matching.
  - **`device`** (string, default: `"cuda"`)
      - The device to use for inference (e.g., `"cuda"` or `"cpu"`).

## 3\. Setup

### 3.1. Install Dependencies

#### ROS 2 Dependencies

```bash
sudo apt update
sudo apt install ros-${ROS_DISTRO}-vision-msgs ros-${ROS_DISTRO}-cv-bridge
```

#### Python Dependencies (PyTorch & GroundingDINO)

```bash
# Use the requirements.txt file in the root of this repository
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
torch
torchvision
numpy
opencv-python-headless
# Grounding DINO and its visualization library
groundingdino-py
supervision
```

### 3.2. Download Models

Download the pre-trained Grounding DINO models and place them in an appropriate directory within the package (e.g., `weights/`).

```bash
# Create a weights directory in your package
mkdir -p src/grounding_dino_ros/weights

# Download a pre-trained model (e.g., Swin-T)
cd src/grounding_dino_ros/weights
wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
cd ../../../.. 
# (The config file should also be placed in a config/ dir)
```

### 3.3. Build

```bash
# Build from your workspace root
colcon build --packages-select grounding_dino_ros
```

## 4\. How to Run

### Directly from Terminal

An example for testing before creating a launch file.

```bash
# Source your workspace
source install/setup.bash

# Run the node, providing paths to the model and a prompt
ros2 run grounding_dino_ros grounding_dino_node \
    --ros-args -p model_config_path:="$(ros2 pkg prefix grounding_dino_ros)/share/grounding_dino_ros/config/GroundingDINO_SwinT_OGC.py" \
    --ros-args -p model_checkpoint_path:="$(ros2 pkg prefix grounding_dino_ros)/share/grounding_dino_ros/weights/groundingdino_swint_ogc.pth" \
    --ros-args -p text_prompt:="a blue cup . a red bottle"
```

### Check in Rviz

1.  Launch `rviz2`.
2.  Add an `Image` display and subscribe to the `~/output/image_processed` topic to see the visualization.
3.  Add a `Detection2DArray` display (if you have a plugin) to visualize the `~/output/detections` topic.

### Dynamic Prompt Changing

While the node is running, open a new terminal and execute:

```bash
ros2 param set /grounding_dino_node text_prompt "laptop . keyboard"
```

The node will immediately start detecting the new objects.

-----

## 5\. Development TODO List (Task Breakdown)

A checklist for efficiently developing the node.

### 📌 Phase 1: Environment Setup (Human-led)

  - [x] Create `grounding_dino_ros` package in ROS2 workspace (`ament_python`).
  - [x] Add ROS dependencies (`rclpy`, `sensor_msgs`, `vision_msgs`, `cv_bridge`) to `package.xml`.
  - [x] Add Python dependencies to `setup.py` and `requirements.txt`.
  - [x] Download model and config files and place them in `weights/` and `config/` directories.
  - [x] Create the skeleton code for `grounding_dino_node.py` (with `main` function and `Node` class).

### 🚀 Phase 2: Node Implementation (AI-assisted)

  - [ ] **Task 2.1: `__init__` - Initialize ROS Interfaces**

      - [ ] Call `rclpy.node.Node` constructor.
      - [ ] Create a `cv_bridge.CvBridge` instance.
      - [ ] Create a subscriber for `~/input/image_raw` (triggers `image_callback`).
      - [ ] Create a publisher for `~/output/detections`.
      - [ ] Create a publisher for `~/output/image_processed`.

  - [ ] **Task 2.2: `__init__` - Declare Parameters**

      - [ ] Use `declare_parameter` for `text_prompt`, `model_config_path`, `model_checkpoint_path`, `box_threshold`, `text_threshold`, and `device`.
      - [ ] Set the parameter descriptor for `text_prompt` to allow dynamic reconfiguration.

  - [ ] **Task 2.3: `__init__` - Load Model**

      - [ ] Log "Loading model..." using `get_logger()`.
      - [ ] Get paths and device settings from parameters.
      - [ ] Load the model using `groundingdino.util.inference.load_model`.
      - [ ] Move the model to the specified device using `.to(device)`.
      - [ ] Log "Model loaded successfully." using `get_logger()`.

  - [ ] **Task 2.4: `image_callback` - Run Inference**

      - [ ] Convert ROS Image message to OpenCV image (BGR8) using `cv_bridge.imgmsg_to_cv2`.
      - [ ] Get the current `text_prompt` value using `get_parameter("text_prompt")`.
      - [ ] (Important) Convert the OpenCV image (BGR) to the format expected by `predict` (e.g., RGB).
      - [ ] Call `groundingdino.util.inference.predict` to get `boxes`, `logits`, and `phrases`.

  - [ ] **Task 2.5: `image_callback` - Publish Detections (ROI)**

      - [ ] Initialize a `vision_msgs.msg.Detection2DArray` message (copy header from input image).
      - [ ] Loop through the inference results (`boxes`, `logits`, `phrases`).
      - [ ] Convert each result into a `vision_msgs.msg.Detection2D` message.
      - [ ] Set the `bbox` (center x, y, size\_x, size\_y) and `results` (score, class\_id).
      - [ ] Add to the `Detection2DArray` and publish to `~/output/detections`.

  - [ ] **Task 2.6: `image_callback` - Publish Visualized Image**

      - [ ] Create a `supervision.Detections` object from the inference results.
      - [ ] Use `supervision.BoxAnnotator` to draw boxes and labels on the input OpenCV image.
      - [ ] Convert the annotated OpenCV image back to a ROS Image message using `cv_bridge.cv2_to_imgmsg`.
      - [ ] Publish the result to `~/output/image_processed`.

  - [ ] **Task 2.7: Create Launch File**

      - [ ] Create a `.launch.py` file to start the node with parameters (especially model paths).
      - [ ] Configure `setup.py` (`data_files`) to install the `weights/` and `config/` directories alongside the package.