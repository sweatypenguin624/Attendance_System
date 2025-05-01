# 📸 Attendance System

**Attendance_System** is a facial recognition-based attendance application built using Python and Gradio. It allows for efficient and automated attendance tracking by recognizing student faces from images.

---

## 🚀 Features

- 🧑‍🎓 **Student Image Registration**: Easily add student images to the system.
- 📷 **Facial Recognition**: Automatically identifies students using their facial features.
- 📝 **Attendance Logging**: Records attendance data and generates reports.
- 📧 **Email Notifications**: Sends attendance reports via email.
- 🌐 **Web Interface**: User-friendly interface powered by Gradio.

---

## 🛠️ Tech Stack

| Component        | Technology         |
|------------------|--------------------|
| Programming Language | Python 3.x       |
| Web Interface    | Gradio              |
| Facial Recognition | OpenCV, face_recognition |
| Email Service    | smtplib             |
| Data Handling    | pandas              |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sweatypenguin624/Attendance_System.git
   cd Attendance_System
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up student images**
   - Create a folder named `images` in the root directory.
   - Add student images in the format `studentname.jpg`.

---

## 🧪 Usage

1. **Run the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to the URL provided by Gradio (usually `http://localhost:7860`).

3. **Mark Attendance**
   - Upload or capture images through the interface to mark attendance.

4. **Generate Reports**
   - Attendance data is saved and can be accessed or emailed as needed.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For questions or support:

- GitHub: [@sweatypenguin624](https://github.com/sweatypenguin624)

---

> Automating attendance tracking with facial recognition technology.
