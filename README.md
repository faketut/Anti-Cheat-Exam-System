# Anti-Cheating-Exam-System

## Overview

The Anti-Cheating Exam System is a Python-based application designed to prevent cheating during exams using Tkinter. This system offers robust measures to ensure a fair and secure exam environment for users.

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>

## Running The App

```bash
python main.py
```

## Features

- **Anti-Cheating Mechanism:** Implements various techniques to prevent cheating during exams.
- **User Authentication:** Secure login system to authenticate users and maintain exam integrity.
- **Question Randomization:** Randomly extracts questions from the database, enhancing exam variability.

## Usage

Threading:
- Implement background tasks for real-time monitoring while the exam is ongoing.
- Use threads to manage simultaneous processes like monitoring system resources and user activities without blocking the main application.
- Employ threading to handle multiple tasks concurrently, such as authenticating users while maintaining a smooth UI experience.
  
Tkinter:
- Create the graphical user interface (GUI) for user authentication, exam modules, and navigation.
- Design interactive screens to guide users through exam instructions and questionnaires.
- Implement secure input and display mechanisms for user authentication to maintain exam integrity.
- Utilize Tkinter widgets to organize and present exam questions and options to the user.
  
Psutil:
- Monitor system resource usage during the exam to detect any abnormal activities or processes.
- Utilize psutil to gather data on CPU, memory, and disk usage to ensure fairness and identify potential cheating behaviors.
- Set up checks to verify that the exam is running on a system with acceptable resource usage, preventing cheating via resource-heavy processes or external assistance.
- Implement a monitoring system to analyze and flag suspicious activities by leveraging psutil's system monitoring capabilities.
These components work together to create a secure exam environment by managing user authentication, providing a seamless UI experience, and actively monitoring system resources to prevent cheating behaviors.

## Project Structure

The project structure includes:

- `AntiCheating.py`: Implements anti-cheating functionalities.
- `Config.py`: Configuration constants and methods.
- `Functions.py`: Manages question extraction and related functions.
- `Main.py`: Entry point and main functionality implementation.


