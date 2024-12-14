# 🎨 Virtual Painter: Hand Gesture-Based Art Tool

Bring your artistic visions to life with the power of AI and hand gestures! The **Virtual Painter** is an innovative application that transforms your webcam into a canvas where you can draw, erase, and color using just your hands.  

![Virtual Painter Demo](https://example.com/demo-image) *(Add a screenshot or demo GIF)*  

## 🌟 Features
- **Gesture Control**: Use hand movements to draw, select colors, erase, and more. No mouse or keyboard needed!
- **Dynamic Color Palette**: Switch between pre-defined colors or pick a custom color using a color picker.
- **Undo/Redo Support**: Correct your strokes easily with undo/redo functionality.
- **Clear All Option**: Start fresh anytime by clearing the entire canvas.
- **Real-Time Performance**: Enjoy smooth and responsive drawing with FPS tracking.
- **Save Your Work**: Capture your masterpiece with a screenshot feature.

## 🛠️ Tech Stack
- **Python**: Core programming language.
- **OpenCV**: For computer vision and real-time video processing.
- **MediaPipe**: Hand tracking for gesture recognition.
- **Tkinter**: Color picker for custom color selection.
- **NumPy**: Efficient matrix operations for canvas manipulation.

## 📂 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sriramsowmithri9807/virtual-painter.git
   cd virtual-painter
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.x installed. Then, install the required libraries:
   ```bash
   pip install opencv-python mediapipe numpy
   ```

3. **Add Resources**:
   Download or create the `Eraser.png` and `Clear all.png` images, and place them in the appropriate path specified in the script.

4. **Run the Application**:
   ```bash
   python virtual_painter.py
   ```

## 🖐️ How It Works
1. **Hand Gesture Tracking**:
   - **Two Fingers (Index + Middle)**: Activates selection mode to pick colors or tools.
   - **One Finger (Index)**: Activates drawing/erasing mode.
   
2. **Interactive Tools**:
   - Choose colors from the palette or the color picker.
   - Use the eraser tool to remove unwanted strokes.
   - Clear the canvas using the "Clear All" button.

3. **Keyboard Shortcuts**:
   - Press `Z`: Undo last action.
   - Press `Y`: Redo the last undone action.
   - Press `S`: Save current canvas state.

## 📸 Screenshots
*(Include images of the app in action, highlighting gesture control and drawing features.)*

## 🚀 Future Enhancements
- Add support for multiple brush styles.
- Enable saving the canvas as an image file.
- Introduce multi-touch gestures for advanced controls.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.  

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🌐 Connect
Feel free to reach out for suggestions or collaboration:
- **GitHub**: [sriramsowmithri9807](https://github.com/sriramsowmithri9807)
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle) *(Add your actual handle)*

---

Let me know if you want to tweak anything!
