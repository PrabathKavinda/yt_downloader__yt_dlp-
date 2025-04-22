from flask import Flask, request, render_template, send_file, redirect, url_for
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        video_url = request.form["url"]
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Create a download endpoint instead of direct response
                return redirect(url_for('download_file', filename=os.path.basename(filename)))
                
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    temp_dir = tempfile.gettempdir()
    return send_file(
        os.path.join(temp_dir, filename),
        as_attachment=True,
        download_name=filename
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))