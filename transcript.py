from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status":"ok"})

@app.route("/transcript")
def get_transcript():
    video_id = request.args.get("video_id")

    if not video_id:
        return jsonify({"error": "video_id is required"}), 400

    try:
        # This matches your original pattern exactly
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])

        # Convert snippet objects → dict so Flask can jsonify
        output = []
        
        for snippet in fetched_transcript:
            output.append({
                "text": snippet.text,
                # "start": snippet.start,
                # "duration": snippet.duration
            })

        return jsonify(output)

    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video"}), 404

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
