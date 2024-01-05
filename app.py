from flask import Flask, render_template_string, request, send_file
from PIL import Image
import os

app = Flask(__name__)

template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Arranger</title>
</head>
<body>
    <h1>Image Arranger</h1>

    {% if success %}
        <p>排版完成，结果保存在: <a href="{{ result_path }}" download>点击下载</a></p>
    {% endif %}

    <form method="post" enctype="multipart/form-data">
        <label for="file">选择图片：</label>
        <input type="file" name="file" accept="image/*" required>
        <button type="submit">上传并排版</button>
    </form>

    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 处理上传的文件
        if "file" not in request.files:
            return render_template_string(template_string, error="No file part")
        
        file = request.files["file"]
        
        if file.filename == "":
            return render_template_string(template_string, error="No selected file")
        
        # 保存上传的文件
        upload_path = "uploads/" + file.filename
        file.save(upload_path)

        # 处理图片排版
        output_path = "static/output/result.jpg"
        arrange_image(upload_path, output_path)

        return render_template_string(template_string, success=True, result_path=output_path)

    return render_template_string(template_string, success=False)

if __name__ == "__main__":
    # 创建uploads目录用于存储上传的文件
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
