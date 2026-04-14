# 🎯 Dead & Injured: Distributed Systems MVP

**A fully decoupled, event-driven desktop application built with Python.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVP-success.svg)
![UI](https://img.shields.io/badge/UI-Tkinter%20%7C%20ttkbootstrap-orange.svg)

## 📌 Project Overview
"Dead & Injured" is a turn-based, code-breaking application designed as a foundational exercise in **System Architecture**. 

Rather than writing a monolithic script, this project implements a strict **Model-View-Presenter (MVP)** pattern to entirely decouple the graphical user interface from the underlying mathematical engine. 

**Core Engineering Goals Achieved:**
* **State Management:** Managing cyclical turns and persistent match data without manual loop tracking.
* **Event-Driven UX:** Handling OS-level keyboard events (like reverse-jump focus) for a seamless, "Fintech-style" input experience.
* **Algorithmic Filtering:** Engineering an automated opponent that dynamically deduces secret PINs using mathematical permutation filtering.

## 🏗️ System Architecture & Features

This application strictly adheres to the MVP pattern, ensuring the graphical interface is entirely agnostic of the game's core mathematical rules.

### Core Engineering Features:

* **Algorithmic AI Opponent:** A custom `ComputerPlayer` class that generates 4-digit permutations and mathematically filters out impossible PINs based on real-time feedback to dynamically close in on the answer.
  
  ![Computer AI Filtering Logic](assets/computer_thinking_screenshot.png)
  *(Placeholder: Add a screenshot of the computer thinking spinner or the terminal showing its possible pin list shrinking)*

* **Asynchronous UI Threading:** Utilizes Tkinter's event loop (`.after()` callbacks) to schedule AI logic and render custom GIF loading animations without blocking or freezing the main OS thread.
  
  ![Asynchronous UI Spinner](assets/ui_spinner_screenshot.png)
  *(Placeholder: Add a quick screenshot or GIF of the UI staying responsive during a turn)*

* **Custom Event-Driven Inputs:** Bypasses standard text entries for a highly interactive, "Fintech-style" UX. Intercepts `<KeyRelease>` and `<KeyPress-BackSpace>` events at the OS level for automatic cursor routing and reverse-jumping.
  
  ![Fintech Style Input Boxes](assets/fintech_input_screenshot.png)
  *(Placeholder: Add a screenshot of the 4-box PIN/Guess entry screen)*

* **Dual-Mode State Orchestration:** The Presenter dynamically reconfigures the internal state machine for either Local Multiplayer (`H_Vs_H`) or Single Player against the AI (`H_Vs_C`) on the fly.
  
  ![Mode Selection Screen](assets/mode_selection_screenshot.png)
  *(Placeholder: Add a screenshot of the Home Screen dropdown menu)*

* **Persistent Data & Schema Migration:** Reads and writes match histories to `D_n_I_leaderboard.json` using an O(1) dictionary lookup structure (`winner:loser`), parsing the data to dynamically populate a visual Treeview leaderboard.
  
  ![Global Leaderboard Table](assets/leaderboard_screenshot.png)
  *(Placeholder: Add a screenshot of your beautiful Treeview Leaderboard)*

* **Memory-Safe Soft Resets:** A centralized `reset_sequence()` completely wipes the core data models and clears UI frames, allowing users to restart matches infinitely without destroying the application window or causing state bleed.
  
  ![Game Over and Reset Screen](assets/game_over_screenshot.png)
  *(Placeholder: Add a screenshot of the Game Over screen showing the 'Play Again' button)*

## 🚀 Getting Started

This application requires **Python 3.10+**. 

### 1. Clone & Install Dependencies
The GUI utilizes `ttkbootstrap` for modern rendering.

```bash
git clone [https://github.com/yourusername/DeadandInjured-GUI-Application.git](https://github.com/yourusername/DeadandInjured-GUI-Application.git)
cd DeadandInjured-GUI-Application
pip install ttkbootstrap pillow
```

### 2. Launch the Application
You can run the full Graphical User Interface, or test the underlying logic engine directly via the Command Line Interface.

**To run the Desktop GUI:**
```bash
python main.py
```

**To run the headless CLI version:**
```bash
python DeadAndInjuredCLI_App.py
```

## 🗺️ Future Roadmap: The Backend Pivot (Phase 2)

This desktop application represents **Phase 1 (The Local MVP)** of the Dead & Injured system. The codebase was intentionally designed with strict Model-View boundaries to ensure a seamless transition to a distributed **Client-Server architecture**. 

The immediate next steps for this project involve migrating the core logic to the cloud:
* **API Extraction:** Removing the local `game_presenter.py` routing and migrating the rules engine (`backend_models`) to a dedicated **Flask server**.
* **RESTful Communication:** Refactoring the Tkinter View to act as a pure frontend client, sending HTTP requests (e.g., `POST /api/guess`) instead of local method calls.
* **Database Scaling:** Replacing the local `D_n_I_leaderboard.json` persistence with a robust relational database (e.g., PostgreSQL or SQLite via SQLAlchemy) to support a true, global online leaderboard.
* **Security:** Implementing session management and secure endpoints to ensure player scores and the computer's secret PINs cannot be manipulated client-side.
