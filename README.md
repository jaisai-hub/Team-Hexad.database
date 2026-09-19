# 🌊 AI-Based Oil Spill Detection, Drift Prediction & Vessel Attribution

<div align="center">

[![AI/ML](https://img.shields.io/badge/AI%2FML-PyTorch-blue?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Computer Vision](https://img.shields.io/badge/Computer-Vision-green?style=for-the-badge)](https://opencv.org/)
[![Geospatial](https://img.shields.io/badge/Geospatial-SAR%20%7C%20GIS-orange?style=for-the-badge)](https://www.sentinel.esa.int/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![SIH 2026](https://img.shields.io/badge/SIH-2026-red?style=for-the-badge)](https://www.sih.gov.in/)

**AI-powered maritime intelligence for oil-spill detection, drift prediction, origin estimation, and vessel trajectory analysis.**

🛰️ Detect • 🌊 Trace • 🔮 Predict • 🚢 Analyze

</div>

---

## 🎯 Project Overview

Marine oil spills are difficult to monitor because they can spread rapidly across large ocean regions and may not be easily visible from conventional optical satellite imagery.

This project develops an **end-to-end AI and geospatial intelligence system** that combines:

- 🛰️ **Sentinel-1 SAR satellite imagery**
- 🌊 **Ocean and atmospheric environmental data**
- 🚢 **AIS vessel trajectory data**
- 🤖 **Deep learning**
- 🗺️ **Geospatial analysis**
- 🎲 **Probabilistic uncertainty modeling**

The system consists of **three interconnected models**.

```text
                 🛰️ Sentinel-1 SAR
                        │
                        ▼
        ┌────────────────────────────┐
        │          MODEL 1           │
        │ Oil Spill Detection &      │
        │       Segmentation         │
        └──────────────┬─────────────┘
                       │
                       ▼
             Spill Mask / Polygon
             Area + Centroid
                       │
                       ▼
        ┌────────────────────────────┐
        │          MODEL 2           │
        │ Drift & Origin Prediction  │
        └──────────────┬─────────────┘
                       │
                       ▼
          Origin + Drift Trajectory
          Future Spill Prediction
                       │
                       ▼
        ┌────────────────────────────┐
        │          MODEL 3           │
        │    AIS Vessel Analysis     │
        └──────────────┬─────────────┘
                       │
                       ▼
             Vessel Trajectories
             + Analytical Ranking
                       │
                       ▼
              🌍 MARITIME
              INTELLIGENCE
