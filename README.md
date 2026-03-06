# 🌿 LeafGuard AI  
### AI-Powered Crop Nutrient Deficiency Detection

LeafGuard AI is a **farmer-friendly web application** that detects **plant nutrient deficiencies from leaf images using deep learning** and provides **fertilizer recommendations and agronomic explanations**.

The system combines **Computer Vision, Deep Learning, and Generative AI** to assist farmers in identifying nutrient issues early and improving crop yield.

---

# 🚀 Features

- Upload crop leaf images for analysis
- Detect nutrient deficiencies using a trained **TensorFlow CNN model**
- Provide **fertilizer recommendations**
- Generate **AI-powered agronomic explanations** using **Groq Llama API**
- Display **prediction confidence**
- Secure **user login & authentication system**
- Maintain **analysis history for each user**
- Clean **farmer-friendly user interface**

---

# 🧠 How It Works

1. User uploads a **leaf image**
2. Image is processed using **TensorFlow CNN model**
3. The model predicts nutrient deficiency
4. The system calculates **confidence score**
5. A fertilizer recommendation is generated
6. **Groq LLM generates detailed agronomic explanation**
7. Results are stored in the **user's history**

---

# 🧪 Nutrient Deficiencies Detected

| Deficiency | Recommendation |
|-------------|---------------|
| Nitrogen Deficiency | Apply Urea fertilizer |
| Phosphorus Deficiency | Apply DAP fertilizer |
| Potassium Deficiency | Apply MOP fertilizer |
| Zinc Deficiency | Apply Zinc Sulphate |
| Multiple Deficiencies | Apply balanced NPK fertilizer |
| Healthy Leaf | No fertilizer required |

---

# 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite

### AI / ML
- TensorFlow / Keras
- Convolutional Neural Networks (CNN)

### Generative AI
- Groq API
- Llama 3.1 Model

### Frontend
- HTML
- CSS
- JavaScript

### Other Tools
- Markdown
- Jinja2 Templates
- Werkzeug

---

# 📂 Project Structure
```bash
LeafGuard-AI
│
├── app.py
├── auth.py
├── models.py
├── database.py
├── requirements.txt
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── upload.html
│ ├── result.html
│ └── history.html
│
├── static/
│ ├── style.css
│ └── uploaded images
│
└── nutrient_deficiency_model1.h5


```

# ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/leafguard-ai.git
```

### 2️⃣ Navigate to project folder
```bash
cd leafguard-ai
```


### 3️⃣ Create virtual environment
```bash
python -m venv venv
```

##### Activate it (Windows):
```bash
venv\Scripts\activate
```


### 4️⃣ Install dependencies
```bash
pip install -r requirements.txt
```


### 5️⃣ Add your API key

Create a .env file in the project root:
```bash
GROQ_API_KEY=your_api_key_here
```
### 6️⃣ Run the application
```bash
python app.py
```

##### Open in browser:
```bash
http://127.0.0.1:5000
```


# 📊 Example Workflow

Login or Register

Upload crop leaf image

AI detects nutrient deficiency

Fertilizer recommendation is generated

Detailed AI report is displayed

Result is saved in history

# 🌾 Impact

LeafGuard AI helps farmers:

Detect nutrient deficiencies early

Apply correct fertilizers

Reduce crop loss

Improve crop yield

Make better agricultural decisions


# 🔮 Future Improvements

Multi-language support for farmers

Mobile application

Crop-specific AI models

Soil health integration

Satellite crop monitoring

# 👨‍💻 Author

Sahil Bhardwaj

BTech CSE | AI & ML Enthusiast
