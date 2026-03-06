from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
import os
from dotenv import load_dotenv
import markdown
from groq import Groq
from database import db
from werkzeug.utils import secure_filename
from models import History

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize the Flaks app 
app = Flask(__name__)

# Configure the app 

app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

import models

from auth import auth_bp
app.register_blueprint(auth_bp)
with app.app_context():
    db.create_all()

# Load trained model
import tensorflow as tf
from keras.models import load_model
from keras.layers import Dense

# Patch Dense layer to ignore quantization_config
class CustomDense(Dense):
    def __init__(self, *args, **kwargs):
        kwargs.pop("quantization_config", None)
        super().__init__(*args, **kwargs)

model = load_model(
    "nutrient_deficiency_model1.h5",
    compile=False,
    custom_objects={"Dense": CustomDense}
)

class_names = ["ALL Present", "ALLAB", "KAB", "NAB", "PAB", "ZNAB"]

fertilizer_dict = {
    "NAB": "Apply Nitrogen fertilizer (Urea)",
    "PAB": "Apply Phosphorus fertilizer (DAP)",
    "KAB": "Apply Potassium fertilizer (MOP)",
    "ZNAB": "Apply Zinc Sulphate",
    "ALLAB": "Apply Balanced NPK fertilizer",
    "ALL Present": "No fertilizer needed"
}

friendly_names = {
    "ALL Present": "Healthy Leaf (No Deficiency)",
    "ALLAB": "Multiple Nutrient Deficiency",
    "KAB": "Potassium Deficiency",
    "NAB": "Nitrogen Deficiency",
    "PAB": "Phosphorus Deficiency",
    "ZNAB": "Zinc Deficiency"
}

fertilizer_quantity = {
    "NAB": "Apply 50 kg Urea per hectare",
    "PAB": "Apply 40 kg DAP per hectare",
    "KAB": "Apply 40 kg MOP per hectare",
    "ZNAB": "Apply 25 kg Zinc Sulphate per hectare",
    "ALLAB": "Apply balanced NPK fertilizer mix (N:P:K = 10:26:26)",
    "ALL Present": "No fertilizer required"
}

from flask import session, redirect, url_for

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("upload_page"))
    return redirect(url_for("auth.login"))


@app.route("/upload")
def upload_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    username = session.get("username")
    return render_template("upload.html", username=username)

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    records = History.query.filter_by(user_id=session["user_id"]).order_by(History.date.desc()).all()

    return render_template("history.html", records=records)


@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    

    file = request.files["file"]
    language = request.form.get("language", "English")
    os.makedirs("static", exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join("static", filename)

    file.save(file_path)

    img = load_img(file_path, target_size=(160,160))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0


    
    pred = model.predict(img_array, verbose=0)
    print(pred)


    predicted_index = np.argmax(pred)

    predicted_class_code = class_names[predicted_index]
    predicted_class = friendly_names[predicted_class_code]

    confidence = round(float(np.max(pred)) * 100, 2)
    if confidence < 50:
        confidence_message = "⚠ Low confidence prediction. Please upload a clearer leaf image."
    elif confidence < 70:
        confidence_message = "Moderate confidence prediction."
    else:
        confidence_message = "High confidence prediction."
    

    suggestion = fertilizer_dict[predicted_class_code]
    quantity = fertilizer_quantity[predicted_class_code]

    prompt = f"""
    You are an expert agricultural scientist.

    Detected nutrient deficiency: {predicted_class}
    Explain the problem and solution for farmers in {language}.
    Provide a structured professional report using this exact format:
    

    ### 1. Deficiency Overview
    (2-3 sentences)

    ### 2. Visible Symptoms
    - Point 1
    - Point 2
    - Point 3

    ### 3. Causes
    - Point 1
    - Point 2
    - Point 3

    ### 4. Impact on Crop Yield
    (2-3 sentences)

    ### 5. Recommended Treatment
    - Point 1
    - Point 2

    ### 6. Preventive Measures
    - Point 1
    - Point 2
    - Point 3

    Keep explanation clear and practical.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    raw_explanation = chat_completion.choices[0].message.content
    explanation = markdown.markdown(raw_explanation)


    history = History(
    user_id=session["user_id"],
    image=filename,
    prediction=predicted_class,
    fertilizer=suggestion,
    quantity=quantity
    )

    db.session.add(history)
    db.session.commit()


    return render_template(
    "result.html",
    prediction=predicted_class,
    suggestion=suggestion,
    confidence=confidence,
    confidence_message=confidence_message,
    explanation=explanation,
    file_name=filename,
    quantity=quantity,
    language=language
)

if __name__ == "__main__":
    app.run(debug=True)

