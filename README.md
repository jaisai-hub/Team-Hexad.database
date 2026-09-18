<div align="center">

# AI-Based Oil Spill Detection, Drift Prediction and Vessel Attribution

### "An intelligent pipeline for oil spill detection, movement prediction, origin estimation and vessel analysis"

</div>

---

## Overview

This project is an AI-based end-to-end system designed to detect oil spills from Sentinel-1 SAR satellite imagery, estimate the movement and probable origin of an oil spill using ocean and atmospheric data, and analyze AIS vessel trajectories around the estimated origin.

The system combines deep learning, satellite image processing, geospatial analysis, ocean-current data, weather data, particle tracking and AIS vessel analysis into a single pipeline.

The project consists of three major components:

1. Oil spill detection and segmentation
2. Oil spill drift prediction and origin estimation
3. AIS vessel trajectory analysis and vessel ranking

---

# Project Features

## Oil Spill Detection

The first model detects oil spills from Sentinel-1 SAR satellite imagery.

### Input

The model uses two SAR channels:

* VV
* VH

Large satellite images are divided into 512 x 512 tiles.

Each input has the shape:

```text
512 x 512 x 2
```

### Image Preprocessing

VV and VH channels are normalized independently using percentile-based normalization.

```text
normalized = (value - P2) / (P98 - P2)
```

The values are clipped between 0 and 1.

### Segmentation Model

The project uses a combination of:

* ResNet-34 encoder
* U-Net decoder
* ImageNet pretrained weights
* Skip connections
* Upsampling
* Sigmoid output

The first convolution layer of ResNet-34 is modified to accept two input channels.

### Output

The model produces an oil-spill probability mask:

```text
512 x 512 x 1
```

The classes are:

```text
0 = Background / No Oil
1 = Oil Spill
```

The detected oil region is then converted into a geographic polygon.

The system calculates:

* Oil spill boundary
* Spill area
* Spill centroid
* Latitude
* Longitude
* GeoJSON polygon

---

# Oil Spill Drift Prediction

The second component predicts how the detected oil spill may move through the ocean.

The model receives the following information from the detection stage:

* Oil spill polygon
* Spill centroid
* Satellite capture time
* Spill area

Environmental information is obtained from:

* Copernicus Marine
* ERA5

The environmental inputs include:

* Ocean currents
* Wind
* Wave height
* Wave direction
* Wave period
* Stokes drift

---

# Lagrangian Particle Tracking

The system initializes approximately 500 to 1,000 particles inside the detected spill polygon.

The total particle velocity is represented as:

```text
V_total = V_current + alpha * V_wind + V_stokes + V_diffusion
```

The initial windage coefficient is:

```text
alpha = 0.02
```

The suggested windage range is:

```text
0.01 - 0.03
```

Particle movement is calculated using fourth-order Runge-Kutta integration.

Suggested simulation time steps are:

```text
15 minutes
30 minutes
```

---

# Oil Spill Origin Estimation

Backward particle tracking is used to estimate the probable origin of the detected oil spill.

The system can investigate:

```text
6 hours
12 hours
24 hours
48 hours
72 hours
```

The output includes:

* Probable origin polygon
* Origin centroid
* Origin latitude and longitude
* Origin time window
* Backward particle paths
* Uncertainty radius
* Confidence information

---

# Future Oil Spill Prediction

Forward particle tracking is used to predict the future movement of the oil spill.

Forecast periods include:

```text
+6 hours
+12 hours
+24 hours
+48 hours
+72 hours
```

The system generates predicted movement paths and future spill regions.

---

# Uncertainty Analysis

Oil-spill movement depends on environmental conditions and model parameters.

To represent uncertainty, the system can use ensemble or Monte Carlo simulations.

Different windage values can be tested:

```text
1%
2%
3%
```

Small perturbations can also be applied to environmental inputs and particle conditions.

The results can be represented using a probability heatmap.

---

# Coastal Risk Analysis

Predicted oil-spill regions can be compared with sensitive marine areas.

The system can analyze possible intersections with:

* Coastlines
* Ports
* Marine protected areas
* Coral reef zones
* Fishing zones

Potential intersections can be used to generate coastal-risk alerts.

---

# AIS Vessel Analysis

The third component analyzes vessel movements around the estimated spill origin.

AIS data can be obtained from:

* MarineCadastre
* AccessAIS

Important AIS fields include:

| Field        | Description                  |
| ------------ | ---------------------------- |
| MMSI         | Vessel identification number |
| BaseDateTime | AIS timestamp                |
| LAT          | Latitude                     |
| LON          | Longitude                    |
| SOG          | Speed over ground            |
| COG          | Course over ground           |
| Heading      | Vessel heading               |
| VesselName   | Vessel name                  |
| IMO          | IMO number                   |
| VesselType   | Vessel category              |
| Status       | Navigation status            |
| Length       | Vessel length                |
| Width        | Vessel width                 |
| Draft        | Vessel draft                 |
| Cargo        | Cargo information            |

---

# AIS Data Processing

The AIS processing pipeline consists of:

```text
AIS Data
   |
   v
Data Cleaning
   |
   v
Group by MMSI
   |
   v
Trajectory Reconstruction
   |
   v
Spatial Filtering
   |
   v
Temporal Filtering
   |
   v
Feature Calculation
   |
   v
Vessel Ranking
```

### Data Cleaning

The system performs:

* Duplicate removal
* UTC timestamp conversion
* Invalid latitude and longitude removal
* Impossible speed filtering
* MMSI and time-based sorting
* Region filtering
* Time-window filtering

Valid coordinate ranges are:

```text
Latitude:  -90 to 90
Longitude: -180 to 180
Speed:     >= 0
```

---

# Vessel Trajectory Reconstruction

AIS records are grouped by MMSI.

The vessel trajectory can then be reconstructed using interpolation for:

* Latitude
* Longitude
* Speed
* Course

The reconstructed trajectory is compared with the estimated oil-spill origin and backward drift path.

---

# Vessel Filtering

The system searches for vessels around the estimated origin.

A possible search area is:

```text
Origin uncertainty radius
+
30 km safety buffer
```

A possible time window is:

```text
Origin time +/- 6 hours
```

Vessels are filtered using:

* Minimum distance from origin
* Haversine distance
* Temporal overlap
* Vessel type
* Direction similarity
* Trajectory relationship

---

# Vessel Features

The vessel-ranking stage uses features including:

* Minimum distance
* Time difference
* Trajectory overlap
* Direction similarity
* Speed anomaly
* Course change
* AIS gap duration
* Vessel type
* Origin confidence

An AIS gap may affect the ranking score, but an AIS gap alone does not establish responsibility.

---

# Vessel Ranking

A transparent weighted scoring system is used.

| Feature                  | Weight |
| ------------------------ | -----: |
| Proximity                |    30% |
| Time Match               |    25% |
| Trajectory Match         |    20% |
| AIS Gap                  |    10% |
| Speed and Course Anomaly |    10% |
| Vessel Type              |     5% |

The final score ranges from:

```text
0 - 100
```

The score is intended to prioritize vessels for further analysis. It does not establish that a vessel caused an oil spill.

---

# Future Machine Learning Ranking

The vessel-ranking stage can later be extended using labeled spill-to-vessel datasets.

Potential algorithms include:

* XGBoost
* Random Forest
* LightGBM
* Learning-to-Rank

A future model could estimate a potential-polluter probability based on the available vessel and trajectory features.

---

# System Architecture

```text
Sentinel-1 SAR Image
          |
          v
   SAR Preprocessing
          |
          v
   ResNet-34 + U-Net
          |
          v
 Oil Spill Segmentation
          |
          v
GeoJSON + Area + Centroid
          |
          v
Environmental Data
Current + Wind + Waves
          |
          v
Lagrangian Particle Tracking
          |
     +----+----+
     |         |
     v         v
 Backward   Forward
 Tracking   Prediction
     |
     v
Probable Spill Origin
     |
     v
    AIS Data
     |
     v
Trajectory Reconstruction
     |
     v
 Vessel Filtering
     |
     v
Vessel Feature Extraction
     |
     v
 Weighted Vessel Ranking
     |
     v
Final Analysis
```

---

# Project Workflow

## Step 1: Satellite Image Processing

Sentinel-1 SAR imagery is loaded and VV and VH channels are extracted.

## Step 2: SAR Preprocessing

The SAR channels are normalized and divided into 512 x 512 tiles.

## Step 3: Oil Spill Segmentation

The ResNet-34 and U-Net model detects oil-spill pixels.

## Step 4: Geospatial Processing

The segmentation mask is converted into a geographic polygon.

The spill area and centroid are calculated.

## Step 5: Environmental Data Collection

Ocean currents, wind and wave data are collected for the required region and time.

## Step 6: Backward Tracking

Particle tracking is performed backward to estimate the probable spill origin.

## Step 7: Forward Prediction

Particle tracking is performed forward to predict future spill movement.

## Step 8: Uncertainty Estimation

Multiple simulations are performed using different environmental and windage parameters.

## Step 9: Coastal Risk Analysis

Predicted spill regions are compared with sensitive marine areas.

## Step 10: AIS Data Collection

AIS data is collected around the estimated origin and time window.

## Step 11: Vessel Trajectory Reconstruction

AIS records are cleaned and reconstructed into vessel trajectories.

## Step 12: Vessel Ranking

Vessel features are calculated and the weighted scoring system is applied.

---

# Technologies Used

| Category              | Technologies                      |
| --------------------- | --------------------------------- |
| Programming           | Python                            |
| Deep Learning         | PyTorch                           |
| Architecture          | ResNet-34, U-Net                  |
| Satellite Data        | Sentinel-1 SAR                    |
| Image Format          | GeoTIFF                           |
| Geographic Output     | GeoJSON                           |
| Data Processing       | NumPy, Pandas                     |
| Ocean Data            | Copernicus Marine                 |
| Weather Data          | ERA5                              |
| Vessel Data           | AIS                               |
| Tracking              | Lagrangian Particle Tracking      |
| Numerical Integration | RK4                               |
| Uncertainty           | Monte Carlo / Ensemble Simulation |
| Version Control       | Git and GitHub                    |

---

# Data Sources

The project uses or is designed to use the following data sources:

* Zenodo oil-spill SAR dataset
* Sentinel-1 SAR imagery
* Copernicus Marine ocean physics data
* Copernicus Marine wave data
* ERA5 wind data
* MarineCadastre AIS data
* AccessAIS

---

# Main Outputs

The complete system can generate:

* Oil-spill segmentation masks
* Oil-spill geographic polygons
* Spill area
* Spill centroid
* GeoJSON files
* Estimated origin polygon
* Estimated origin coordinates
* Estimated origin time window
* Backward drift trajectories
* Forward drift predictions
* Probability heatmaps
* Coastal-risk alerts
* AIS vessel trajectories
* Filtered vessel list
* Vessel scores
* Vessel analysis information

---

# Project Objectives

The main objectives of this project are:

* Detect oil spills automatically from satellite imagery
* Convert detected spills into geographic information
* Predict oil-spill movement
* Estimate probable spill origin
* Quantify movement uncertainty
* Identify potentially affected coastal areas
* Analyze nearby vessel trajectories
* Provide a transparent vessel-ranking system
* Build an end-to-end AI-assisted oil-spill analysis pipeline

---

# Limitations

The system depends on the quality and availability of several data sources.

Important limitations include:

* SAR image quality
* Segmentation accuracy
* Environmental data accuracy
* Windage assumptions
* Particle-tracking parameters
* AIS data quality
* AIS coverage
* Uncertainty in the estimated spill origin

Vessel ranking is an analytical prioritization method. A high score does not prove that a vessel caused an oil spill.

---

# Future Scope

Future improvements may include:

* Advanced SAR segmentation models
* Real-time satellite data processing
* Real-time ocean and weather data
* Improved particle-tracking models
* Advanced uncertainty estimation
* Automated coastal-risk monitoring
* Larger AIS datasets
* Supervised vessel attribution models
* XGBoost-based vessel analysis
* LightGBM-based vessel analysis
* Learning-to-Rank models
* Interactive geospatial dashboards
* Real-time oil-spill monitoring

---

# Team

## Team Project

This project is developed as a collaborative team project.

| Team Member   | Role                            |
| ------------- | ------------------------------- |
| punith        | AI/ML and Project Development   |
| nandini       | AI/ML and Project Development   |
| spandana      | Data Processing and Development |
| jai sai       | Development and Integration     |
| sandeepa      | Development and Integration     |
| saniya        | Development and Integration     |

Replace the names and roles above with the actual members of your team.

---

# Team Contribution

The project combines multiple areas of development:

* AI and Machine Learning
* Deep Learning
* Computer Vision
* Satellite Image Processing
* Geospatial Processing
* Ocean Data Analysis
* Numerical Simulation
* AIS Data Processing
* Data Analysis
* Software Development

---

# Conclusion

This project combines satellite-based oil-spill detection, deep learning, environmental data analysis, particle tracking and AIS vessel analysis into a unified pipeline.

The system is designed to support:

```text
Oil Spill Detection
        |
        v
Spill Mapping
        |
        v
Drift Prediction
        |
        v
Origin Estimation
        |
        v
AIS Analysis
        |
        v
Vessel Ranking
```

The goal is to provide an integrated technical framework for analyzing oil-spill events and supporting further investigation using satellite, environmental and vessel-movement data.

---

# Team Project

This repository contains the development work, experiments, implementation and documentation for the project.

If you find the project useful, consider giving the repository a star.

<div align="center">

### AI + Satellite Data + Ocean Modeling + AIS Analysis

</div>
