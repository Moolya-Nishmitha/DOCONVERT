import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
)

from werkzeug.utils import secure_filename
from converters.word_to_pdf import convert_word_to_pdf
from converters.pdf_to_word import convert_pdf_to_word

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

ALLOWED_EXTENSIONS = {"docx", "pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


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

    if "document" not in request.files:
        return "No file uploaded."

    uploaded_file = request.files["document"]

    if uploaded_file.filename == "":
        return "No file selected."

    if not allowed_file(uploaded_file.filename):
        return "Only PDF and DOCX files are allowed."

    conversion = request.form.get("conversion")

    original_filename = secure_filename(uploaded_file.filename)

    unique_filename = (
        f"{uuid.uuid4().hex}_{original_filename}"
    )

    upload_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename,
    )

    uploaded_file.save(upload_path)

    extension = os.path.splitext(original_filename)[1].lower()

    try:

        if extension == ".docx" and conversion == "pdf":

            output_path = convert_word_to_pdf(
                upload_path,
                app.config["OUTPUT_FOLDER"],
            )

        elif extension == ".pdf" and conversion == "word":

            output_path = convert_pdf_to_word(
                upload_path,
                app.config["OUTPUT_FOLDER"],
            )

        else:
            return "Invalid conversion selected."

        # delete uploaded file immediately
        if os.path.exists(upload_path):
            os.remove(upload_path)

        output_filename = os.path.basename(output_path)

        return render_template(
            "result.html",
            original_file=original_filename,
            converted_file=output_filename,
        )

    except Exception as e:
        return f"Conversion failed:<br><br>{e}"


@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(
        app.config["OUTPUT_FOLDER"],
        filename,
    )

    response = send_from_directory(
        app.config["OUTPUT_FOLDER"],
        filename,
        as_attachment=True,
    )

    @response.call_on_close
    def cleanup():

        if os.path.exists(path):
            os.remove(path)

    return response


if __name__ == "__main__":
    app.run(debug=True)