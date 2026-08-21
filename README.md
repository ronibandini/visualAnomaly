# 👁️⚙️ Visual Anomaly

**Real-time visual anomaly detection for industrial quality inspection using Edge Impulse FOMO-AD, a Texas Instruments SK-TDA4VM edge AI board, a USB camera, and Python.**

Visual Anomaly demonstrates how to build an **edge-based visual inspection system** that learns what a correctly assembled product looks like and detects deviations without requiring a training dataset containing every possible defect.

The reference implementation uses:

- **Texas Instruments SK-TDA4VM**
- **USB webcam**
- **Edge Impulse**
- **FOMO-AD**
- **Edge Impulse Linux Runner**
- **Python**

The example dataset consists of correctly assembled electrical components. Once trained, the model can identify unexpected visual differences and report not only that an anomaly exists, but also **where it appears in the image**.

```text
USB camera
    │
    ▼
┌────────────────────┐
│ Texas Instruments  │
│    SK-TDA4VM       │
│                    │
│ Edge Impulse       │
│ Linux Runner       │
└─────────┬──────────┘
          │
          ▼
      FOMO-AD
          │
          ▼
 Anomaly grid + scores
          │
          ▼
     anomaly.py
          │
          ▼
   Terminal matrix

. . . . .
. . X X .
. . X X .
. . . . .
. . . . .
```

---

## ✨ Features

- 👁️ Real-time visual anomaly detection
- 🧠 Edge Impulse FOMO-AD
- 🏭 Designed around manufacturing quality-control use cases
- 📷 USB camera input
- ⚡ Local edge inference
- 🌐 No cloud connection required during inference
- 📊 Per-region anomaly scores
- 📍 Anomaly localization
- 🐍 Python result parser
- 🖥️ Text-based anomaly visualization
- 🧩 Train primarily with normal examples
- 🔄 Adaptable to different products by replacing the dataset
- 🧪 Public Edge Impulse model available
- 🤖 Runs on a dedicated edge AI platform

---

## 🧠 Why anomaly detection?

A conventional image classifier usually requires examples of every class it needs to recognize.

For manufacturing inspection, that can become difficult.

A product may fail in many different ways:

```text
missing component
wrong component
misalignment
surface damage
incorrect assembly
foreign object
deformation
unexpected color
unknown future defect
```

Collecting representative images for every possible failure mode can be impractical.

Visual anomaly detection takes a different approach:

```text
Many examples of GOOD products
             │
             ▼
      Learn normal state
             │
             ▼
       New camera image
             │
             ▼
 Compare against normality
             │
       ┌─────┴─────┐
       ▼           ▼
    Normal      Anomaly
```

The model is trained to understand the distribution of normal visual features.

An image region that differs significantly from that learned distribution receives a higher anomaly score.

---

# 🧠 FOMO-AD

The project uses **FOMO-AD — Faster Objects, More Objects: Anomaly Detection**, developed by Edge Impulse.

FOMO-AD extends the FOMO architecture for visual anomaly detection and is designed specifically for deployment on edge hardware.

Unlike a conventional defect classifier, FOMO-AD can be trained primarily using:

```text
normal
normal
normal
normal
normal
...
```

rather than requiring:

```text
normal
broken connector
missing screw
cracked housing
incorrect label
bent terminal
wrong component
...
```

This makes it particularly useful when the space of possible defects is large or unknown.

---

## Gaussian Mixture Model

FOMO-AD uses a **Gaussian Mixture Model — GMM** for anomaly scoring.

A GMM models the distribution of feature vectors produced by normal training images.

Conceptually:

```text
Normal image
     │
     ▼
Feature extractor
     │
     ▼
Feature vectors
     │
     ▼
Gaussian Mixture Model
     │
     ▼
Probability distribution
```

During inference:

```text
New image region
       │
       ▼
Feature vector
       │
       ▼
How probable is this feature
under the learned distribution?
       │
   ┌───┴───┐
   ▼       ▼
 High     Low
   │       │
Normal   Anomaly
```

A low probability of belonging to the learned normal distribution results in a high anomaly score.

---

## 📍 Localized anomaly detection

A major advantage of FOMO-AD is that it does not only return:

```text
anomaly = yes
```

It can also locate the anomalous region.

The Edge Impulse Linux Runner returns cells containing information such as:

```json
{
  "height": 19,
  "label": "anomaly",
  "value": 3.5148870944976807,
  "width": 19,
  "x": 38,
  "y": 0
}
```

The fields describe:

| Field | Meaning |
|---|---|
| `x` | Horizontal position |
| `y` | Vertical position |
| `width` | Width of the anomaly cell |
| `height` | Height of the anomaly cell |
| `label` | Cell classification |
| `value` | Anomaly score |

This allows downstream software to determine which area of the inspected product differs from the learned normal state.

---

# 🐍 `anomaly.py`

The repository includes:

```text
anomaly.py
```

The script parses the visual-anomaly output generated by the Edge Impulse Linux Runner.

Instead of displaying raw JSON, it converts anomaly locations into a simple text matrix.

Conceptually:

```text
Runner JSON
    │
    ▼
Parse cells
    │
    ▼
Read x / y coordinates
    │
    ▼
Build matrix
    │
    ▼
X = anomaly
. = normal
```

Example:

```text
. . . . .
. . . . .
. X X . .
. X X . .
. . . . .
```

This provides an immediate terminal representation of the location of a detected defect.

---

# 🧰 Hardware

## Texas Instruments SK-TDA4VM

The reference implementation uses the:

**Texas Instruments SK-TDA4VM**

This development kit is designed for edge AI vision applications and is based on the **TDA4VM Jacinto processor**.

Relevant specifications include:

- dual Arm Cortex-A72 CPU
- C7x DSP
- dedicated deep-learning accelerator
- up to **8 TOPS** of AI performance
- vision-processing accelerators
- Linux support
- camera interfaces
- Ethernet
- USB
- GPU
- dedicated hardware for vision workloads

Official hardware page:

**[Texas Instruments SK-TDA4VM](https://www.ti.com/tool/SK-TDA4VM)**

Processor:

**[Texas Instruments TDA4VM](https://www.ti.com/product/TDA4VM)**

---

## 📷 USB camera

The project uses a conventional USB webcam.

The original build was tested with cameras such as:

```text
Logitech C270
Logitech C920
Logitech C922
```

Other Linux-compatible UVC cameras may also work.

A suitable camera should provide:

- stable focus
- consistent exposure
- repeatable framing
- adequate resolution
- low image noise

For anomaly detection, camera consistency is important because differences in lighting, focus, or perspective can themselves appear anomalous.

---

# 🏭 Example inspection target

The reference project uses **electrical components / circuit breakers** as the inspected objects.

Approximately 100–120 images of correctly assembled products were used to demonstrate the workflow.

```text
correct breaker
correct breaker
correct breaker
correct breaker
correct breaker
       │
       ▼
    Training
       │
       ▼
   Normal model
```

Then a modified or incorrectly assembled example can be presented to the camera:

```text
expected product
      vs.
unexpected visual difference
```

The same workflow can be adapted to many other objects by replacing the training dataset.

Examples:

- PCB assemblies
- connectors
- machined parts
- packaging
- labels
- bottles
- mechanical assemblies
- castings
- molded parts
- electronic modules
- consumer products

---

# 📊 Dataset

The repository contains:

```text
dataset/
```

with sample material associated with the project.

The important principle for training FOMO-AD is that the training set should primarily represent the **correct product state**.

Good training images should cover normal variations such as:

```text
small position changes
minor lighting variation
normal manufacturing tolerances
small camera differences
acceptable surface variation
```

while excluding actual faults.

---

## 📷 Image quality matters

Visual anomaly detection depends heavily on dataset consistency.

Potential problems include:

- blurry images
- inconsistent camera positions
- large lighting changes
- strong reflections
- noisy images
- varying backgrounds
- partially visible products
- different scales
- significant rotations

A model may learn these variations as part of the normal distribution or mistakenly classify them as anomalies.

For production systems, the imaging setup should be mechanically controlled whenever possible.

---

# 🧪 Edge Impulse project

The public Edge Impulse project is available at:

**[Visual Anomaly — Edge Impulse Studio](https://studio.edgeimpulse.com/public/374008/latest)**

The reference workflow uses:

```text
Image Data
    │
    ▼
96 × 96
    │
    ▼
Squash resize
    │
    ▼
Image processing
    │
    ▼
FOMO-AD
```

---

## 1. Upload normal images

Upload approximately:

```text
100+
```

images of correctly assembled products.

Use:

```text
No Anomaly
```

as the normal-state label where required by the Edge Impulse workflow.

The training dataset should contain as few actual anomalies as possible.

---

## 2. Create the impulse

Configure image input as:

```text
Width:  96
Height: 96
Resize: Squash
```

Add:

```text
Image
```

as the processing block.

Then select:

```text
Visual Anomaly Detection / FOMO-AD
```

as the learning block.

---

## 3. Generate features

Edge Impulse extracts visual features from the training images.

These features represent the visual structure of correctly assembled products.

The feature explorer can help identify:

- unusual training images
- inconsistent examples
- outliers
- poor dataset coverage

---

## 4. Train FOMO-AD

FOMO-AD includes a configurable:

```text
Capacity
```

parameter.

Higher capacity increases the number of Gaussian components used to model the normal feature distribution.

Conceptually:

```text
Lower capacity
      │
      ▼
simpler normal distribution

Higher capacity
      │
      ▼
more detailed adaptation
to the training distribution
```

Too little capacity may underfit normal variation.

Too much capacity may make the model unnecessarily specific to the training data.

---

# 🎚️ Anomaly threshold

FOMO-AD uses an anomaly threshold to determine when a cell should be classified as anomalous.

```text
anomaly score
      │
      ▼
compare with threshold
      │
  ┌───┴────┐
  ▼        ▼
below     above
  │        │
normal   anomaly
```

Changing the threshold modifies sensitivity.

A lower threshold may increase detection sensitivity but also increase false positives.

A higher threshold may reduce false positives but miss subtle defects.

The threshold should therefore be validated using representative production examples.

---

# 🧪 Model testing

After training, open:

```text
Model Testing
```

in Edge Impulse.

Use:

```text
Classify All
```

to evaluate test images.

For FOMO-AD, the visual interface displays a grid over the image.

Cells are represented using anomaly scores.

Regions exceeding the configured threshold indicate detected anomalies.

---

## 📊 Calculating an F1 score

Anomaly-only training does not inherently provide the same accuracy metric as a conventional supervised classification dataset.

To evaluate the system more formally, a separate test set can contain labeled examples such as:

```text
No Anomaly
Anomaly
```

This can then be used to calculate metrics such as:

```text
precision
recall
F1 score
```

without contaminating the normal-only training data.

---

# ⚙️ Texas Instruments software setup

The original project used the Texas Instruments Linux SDK for the SK-TDA4VM.

Official download:

**[PROCESSOR-SDK-LINUX-SK-TDA4VM](https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM)**

The historical project tutorial used:

```text
08.06.00.11
```

because that image worked with the USB camera and Edge Impulse Linux Runner used during development.

Texas Instruments now publishes newer SDK releases, so current installations should also consult the current TI and Edge Impulse documentation.

---

# 💾 Flash the system image

Download the appropriate:

```text
.wic.xz
```

image from Texas Instruments.

Flash it to a microSD card using a tool such as:

- Raspberry Pi Imager
- balenaEtcher
- `dd`

Insert the microSD card into the SK-TDA4VM and boot the board.

---

# 🌐 Network connection

The reference setup uses Ethernet.

```text
SK-TDA4VM
    │
    └── Ethernet
          │
          ▼
        Router
```

Determine the IP address assigned by the router.

The historical TI image used:

```text
User: root
Password: empty
```

for SSH access.

Credentials and defaults can differ on current Processor SDK releases.

---

# 📷 Verify the camera

Connect the USB webcam before launching inference.

The Edge Impulse Linux tools can expose a camera preview stream.

In the original setup this could be viewed at:

```text
http://<BOARD_IP>:4912
```

For example:

```text
http://192.168.1.67:4912
```

Use the preview to check:

- focus
- framing
- product position
- illumination
- reflections

before collecting data or running inference.

---

# 📦 Install Edge Impulse Linux tools

The original setup updates Node.js with:

```bash
npm install -g n
n lts
n latest
n prune
```

Then installs Edge Impulse for Linux:

```bash
npm install -g --unsafe-perm edge-impulse-linux
```

Verify the tools are available before continuing.

---

# 🚀 Deploy the model

On the SK-TDA4VM:

```bash
edge-impulse-linux-runner
```

Log in with your Edge Impulse credentials.

Select the Visual Anomaly project when prompted.

The Linux Runner downloads the model and starts inference using the attached camera.

---

## 🔄 Refreshing the model

If the Edge Impulse model or threshold has been changed, reset the runner's downloaded model:

```bash
edge-impulse-linux-runner --reset
```

Then launch it again:

```bash
edge-impulse-linux-runner
```

---

# 🐍 Install the parser

Clone the repository:

```bash
git clone https://github.com/ronibandini/visualAnomaly.git
cd visualAnomaly
```

The main parser is:

```text
anomaly.py
```

The original deployment copied it to:

```text
/opt/edge_ai_apps
```

Run:

```bash
python3 anomaly.py
```

The script processes FOMO-AD results and prints the visual anomaly map to the terminal.

---

# 🔄 Complete workflow

```text
┌──────────────────┐
│ Normal products  │
│ 100+ photographs │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Edge Impulse   │
│                  │
│ Image processing │
│ FOMO-AD          │
└────────┬─────────┘
         │
         ▼
   Train / test
         │
         ▼
┌──────────────────┐
│ Edge Impulse     │
│ Linux Runner     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  SK-TDA4VM       │
│  + USB camera    │
└────────┬─────────┘
         │
         ▼
  anomaly scores
         │
         ▼
    anomaly.py
         │
         ▼
 terminal matrix
```

---

# 📁 Repository structure

```text
visualAnomaly/
├── dataset/
├── README.md
└── anomaly.py
```

### `anomaly.py`

Python parser for Edge Impulse visual-anomaly inference output.

It converts anomaly coordinates into a simplified terminal visualization.

### `dataset/`

Sample project data associated with the visual anomaly experiment.

### `README.md`

Original project notes and links.

---

# ⚡ Edge inference

Inference is performed on the local hardware.

The production path is:

```text
camera
  │
  ▼
TDA4VM
  │
  ▼
Edge Impulse model
  │
  ▼
anomaly score
```

The camera frames do not need to be uploaded to a remote inference server.

Advantages include:

- lower latency
- continued operation without Internet access
- reduced network traffic
- easier integration with production equipment
- local control of camera data

---

# 🏭 Industrial use cases

The architecture can be adapted to quality-control tasks such as:

### Electronics

```text
missing components
incorrect connectors
damaged PCB sections
wrong component placement
assembly errors
```

### Mechanical parts

```text
missing screws
surface damage
deformation
incorrect machining
assembly differences
```

### Packaging

```text
missing labels
damaged boxes
incorrect closures
missing contents
wrong printing
```

### Food and consumer goods

```text
incorrect shape
surface damage
foreign material
packaging anomalies
missing elements
```

The model must be retrained with normal examples from the specific object and production environment.

---

# ⚠️ Limitations

## Noisy images

High image noise can make convolutional feature extraction less reliable.

Use:

- good illumination
- controlled camera settings
- fixed mounting
- adequate focus
- short exposure times where objects move

---

## Receptive field size

An anomaly larger than the effective receptive field of the model may not be represented optimally by a single FOMO-AD configuration.

For some applications, multiple models operating at different scales can provide additional confidence.

---

## Normal-state coverage

The model can only learn the normal variations represented in its training data.

If legitimate production variation is missing from the dataset, it may be classified as anomalous.

---

## Threshold tuning

There is no universal anomaly threshold.

The correct value depends on:

- product
- camera
- illumination
- manufacturing tolerances
- cost of false positives
- cost of false negatives

---

## Prototype vs. production system

The project demonstrates the Machine Learning core of a visual inspection system.

A production implementation may additionally require:

```text
camera trigger
industrial lighting
PLC integration
conveyor synchronization
product tracking
reject mechanism
database
traceability
statistics
operator UI
alerts
multiple cameras
redundant inspection
```

---

# 🔬 Ideas for extending the project

1. **📊 Store anomaly scores over time** — save coordinates, scores, product IDs and timestamps to a database for quality trends and process analysis.

2. **🦾 Automatic reject mechanism** — integrate the validated anomaly result with a PLC, servo or pneumatic mechanism to divert defective parts from a production line.

3. **📷 Multi-camera inspection** — combine several synchronized views to detect defects that cannot be reliably observed from a single camera angle.

---

# 📰 External references

## 🗞️ Edge Impulse

### Building an Automated Manufacturing Inspection System with FOMO-AD

Edge Impulse published a dedicated feature about this project on June 26, 2024.

The article covers:

- FOMO-AD
- circuit-breaker inspection
- the SK-TDA4VM
- USB camera input
- approximately 120 normal training images
- local edge inference
- anomaly localization
- industrial inspection applications

**[Building an Automated Manufacturing Inspection System with FOMO-AD — Edge Impulse](https://www.edgeimpulse.com/blog/automated-manufacturing-inspection-with-fomo-ad/)**

---

## 🧠 Edge Impulse Expert Network

### Visual Anomaly Detection with FOMO-AD — Texas Instruments TDA4VM

The complete technical tutorial is part of the Edge Impulse Expert Network.

It documents:

- how FOMO-AD works
- Gaussian Mixture Models
- dataset creation
- 96×96 image configuration
- model training
- anomaly thresholds
- model testing
- TI Processor SDK installation
- Linux Runner deployment
- `anomaly.py`
- terminal anomaly matrix
- known limitations

**[Visual Anomaly Detection with FOMO-AD — Edge Impulse Documentation](https://docs.edgeimpulse.com/projects/expert-network/fomo-ad-ti-tda4vm)**

---

## 🧪 Public Edge Impulse model

The model can be inspected in Edge Impulse Studio:

**[Visual Anomaly — Edge Impulse Studio](https://studio.edgeimpulse.com/public/374008/latest)**

---

# ✍️ Medium

## Detección de anomalías con Machine Learning

Spanish-language article explaining:

- visual anomaly detection
- dataset asymmetry
- Gaussian Mixture Models
- Edge Impulse
- edge inference
- anomaly localization
- Python parsing
- industrial quality-control applications

**[Read on Medium](https://bandini.medium.com/detecci%C3%B3n-de-anomal%C3%ADas-con-machine-learning-ca39c7f5d868)**

---

# 📢 Edge Impulse social reference

Edge Impulse also featured the project through its official LinkedIn account:

**[Building an Automated Manufacturing Inspection System with FOMO-AD — Edge Impulse on LinkedIn](https://www.linkedin.com/posts/edgeimpulse_building-an-automated-manufacturing-inspection-activity-7211770973778296832-ixZC)**

---

# 🎥 Demo

The repository includes a YouTube demonstration of the running visual anomaly system:

**[Visual Anomaly Demo — YouTube](https://www.youtube.com/watch?v=UckRoZBy8vk)**

---

# 📕 Contracultura Maker

More projects, technical experiments and context around unconventional hardware, artificial intelligence, Machine Learning and electronic prototyping are collected in:

**[Contracultura Maker — book](https://bandini.medium.com/libro-de-contracultura-maker-94d1bb0d951c)**

---

# 📚 Useful references

- **[Edge Impulse](https://edgeimpulse.com/)**
- **[FOMO-AD project tutorial](https://docs.edgeimpulse.com/projects/expert-network/fomo-ad-ti-tda4vm)**
- **[Visual Anomaly public model](https://studio.edgeimpulse.com/public/374008/latest)**
- **[Texas Instruments SK-TDA4VM](https://www.ti.com/tool/SK-TDA4VM)**
- **[Texas Instruments TDA4VM](https://www.ti.com/product/TDA4VM)**
- **[TI Processor SDK Linux for SK-TDA4VM](https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM)**
- **[Gaussian Mixture Models — Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/05.12-gaussian-mixtures.html)**
- **[Visual Anomaly Detection with FOMO-AD — Edge AI and Vision Alliance](https://www.edge-ai-vision.com/2023/06/visual-anomaly-detection-with-fomo-ad-a-presentation-from-edge-impulse/)**

---

# 🔗 You may also be interested in...

Other projects by **Roni Bandini** involving anomaly detection, industrial inspection and Edge Impulse.

## 👁️⚡ Visual Anomaly — Grove Vision AI V2

**A low-cost standalone visual anomaly detector using the Seeed Studio Grove Vision AI Module V2 and Edge Impulse FOMO-AD.**

This project takes the same anomaly-detection concept to a much smaller and less expensive vision module.

**[github.com/ronibandini/visualAnomalyGroveV2](https://github.com/ronibandini/visualAnomalyGroveV2)**

---

## 🟦📊 RUBIK Pi 3 Anomaly Detection

**Visual anomaly detection with Edge Impulse on the RUBIK Pi 3, connected to n8n for data aggregation, charts and email reports.**

It extends the original visualAnomaly model into a reporting and workflow-automation architecture.

**[github.com/ronibandini/rubikpi3-anomaly-detection](https://github.com/ronibandini/rubikpi3-anomaly-detection)**

---

## ⚡🧠 EdenOff

**Offline TinyML experiment using voltage, temperature and recent voltage behavior to detect conditions associated with power outages.**

Another anomaly-oriented Machine Learning project focused on detecting deviations from normal operating conditions.

**[github.com/ronibandini/EdenOff](https://github.com/ronibandini/EdenOff)**

---

# 👤 Author

**Roni Bandini**

Maker, AI developer, electronic artist and writer.

- 🐙 GitHub: [@ronibandini](https://github.com/ronibandini)
- 💼 LinkedIn: [Roni Bandini](https://www.linkedin.com/in/ronibandini/)
- 📸 Instagram: [@ronibandini](https://www.instagram.com/ronibandini/)
- 🐦 X: [@RoniBandini](https://x.com/RoniBandini)
- ✍️ Medium: [bandini.medium.com](https://bandini.medium.com/)
- 🛠️ Hackster: [Roni Bandini](https://www.hackster.io/roni-bandini)
- 🔧 Hackaday.io: [Roni Bandini](https://hackaday.io/ronibandini)

Buenos Aires, Argentina.
