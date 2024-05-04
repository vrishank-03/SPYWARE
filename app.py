from flask import Flask, render_template, request
import threading
import spy_img

app = Flask(__name__, template_folder="C:\\Users\\digital.library\\Desktop\\Data_privacy_MP")

# Define route to start the script
@app.route('/start-script', methods=['POST'])
def start_script():
    # Start the script in a new thread
    threading.Thread(target=spy_img.start).start()
    return '', 204  # Return a success response with status code 204 (No Content)

# Define route to stop the script
@app.route('/stop-script', methods=['POST'])
def stop_script():
    # Stop the script
    spy_img.stop()
    return '', 204  # Return a success response with status code 204 (No Content)

# Define route for the index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
