# Gesture Volume Control
![](https://github.com/AdilShamim8/Gesture-Volume-Control/blob/main/image/Output.gif)


What if controlling your computer’s volume was as natural as breathing? No knobs. No sliders. Just a gesture—your hand speaking to your machine.

Gesture Volume Control merges **OpenCV**, **MediaPipe**, and **pycaw** into a singular experience: effortless, elegant, and utterly human.

---

##  The Vision

You shouldn’t need to reach for anything. Let your hand be the interface. Extend your thumb and index finger—feel the world respond. Bring them closer—experience perfect silence. This is not just a project; it’s a statement:

> **Interaction should be invisible.**

That’s the future we’re building.

---

##  How It Feels

1. **You sit before your camera.**  
2. **Your hand floats** into view.  
3. **MediaPipe** identifies your thumb tip and index fingertip.  
4. **OpenCV** measures the distance.  
5. **pycaw** breathes life into that measurement—volume rises and falls.  

No menus. No clicks. Only motion.
![](https://github.com/AdilShamim8/Gesture-Volume-Control/blob/main/image/hand_landmarks_docs.png)
![](https://github.com/AdilShamim8/Gesture-Volume-Control/blob/main/image/htm.jpg)


---

##  What’s Inside

- **HandTrackingModule.py**  
  A concise, battle-tested engine that detects 21 hand landmarks in real time.

- **main.py**  
  Where your gesture becomes command. It captures frames, computes distance, and whispers to your audio device.

- **requirements.txt**  
  All you need:  
  ```txt
  opencv-python
  mediapipe
  pycaw
  numpy
  comtypes

---

##  Get Started

1. **Clone & Enter**

   ```bash
   git clone https://github.com/AdilShamim8/Gesture-Volume-Control.git
   cd Gesture-Volume-Control
   ```

2. **Install Everything**

   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Magic**

   ```bash
   python main.py
   ```

4. **Command Your Sound**

   * **Spread fingers apart** → volume climbs.
   * **Bring them together** → volume fades away.

Feel the simplicity.

---

##  Why It Matters

* **Intuitive** – Your hand is your remote.
* **Responsive** – Milliseconds between motion and action.
* **Open‐Source** – Visibility into every line of code.
* **Expandable** – Today, volume. Tomorrow, brightness. Or next track.

Buttons are relics of the past.

---

##  What’s Next

* **Gesture Customizer** – Define gestures visually.
* **Multi‐Control Hub** – One app for volume, brightness, media play/pause.
* **Cross‐Platform** – macOS and Linux support (using native audio bindings).
* **Adaptive Learning** – The system learns your preferred gestures over time.

The story only begins here.

---

##  Inspirations & Gratitude

* **Pratham Bhatnagar’s original vision**
* **MediaPipe by Google** powers our hands with precision.
* **pycaw** connects us to Windows audio with grace.
* **You**, the explorer, making every gesture count.

---

##  License

Licensed under the [MIT License](License).

We said no to complexity. We said yes to your hand.

Gesture Volume Control—where your motion speaks volume.
