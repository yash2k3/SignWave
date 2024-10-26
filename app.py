from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run_script', methods=['GET'])
def run_script():
    try:
        result = subprocess.run(['python3', 'detect-2.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
        return jsonify({"message": "Script executed successfully!", "output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"message": f"An error occurred: {str(e)}", "output": e.output.decode('utf-8') if e.output else "No output"})
    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
