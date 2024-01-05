from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

def arrange_image(input_path, output_path):
    original_image = Image.open(input_path)
    a4_width = 2480
    a4_height = 3508
    width_ratio = a4_width / original_image.width
    height_ratio = a4_height / original_image.height
    ratio = min(width_ratio, height_ratio)
    new_width = int(original_image.width * ratio)
    new_height = int(original_image.height * ratio)
    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
    a4_paper = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))
    x_position = (a4_width - new_width) // 2
    y_position = (a4_height - new_height) // 2
    a4_paper.paste(resized_image, (x_position, y_position))
    a4_paper.save(output_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 处理上传的文件
        if "file" not in request.files:
            return render_template("index.html", error="No file part")
        
        file = request.files["file"]
        
        if file.filename == "":
            return render_template("index.html", error="No selected file")
        
        # 保存上传的文件
        upload_path = "uploads/" + file.filename
        file.save(upload_path)

        # 处理图片排版
        output_path = "static/output/result.jpg"
        arrange_image(upload_path, output_path)

        return render_template("index.html", success=True, result_path=output_path)

    return render_template("index.html", success=False)

if __name__ == "__main__":
    # 创建uploads目录用于存储上传的文件
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
