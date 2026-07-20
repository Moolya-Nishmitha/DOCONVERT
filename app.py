import os

from flask import Flask, render_template, request
from docx2pdf import convert
app = Flask(__name__)
ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files["document"]
    if uploaded_file.filename == "":
        return "No file selected."
    if not allowed_file(uploaded_file.filename):
        return "Only PDF and DOCX files are allowed."
    conversion_type = request.form["conversion"]

    filename = uploaded_file.filename
    upload_path = os.path.join("uploads", filename)

    uploaded_file.save(upload_path)

    return render_template(
    "success.html",
    filename=filename,
    conversion=conversion_type
)


if __name__ == "__main__":
    app.run(debug=True)