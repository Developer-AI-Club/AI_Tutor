from aspeak import SpeechToSpeakerService, ResultReason

speech = SpeechToSpeakerService()
def say(text = "Nothing to say"):
    try:
        result = speech.text_to_speech(text,voice="en-US-JennyNeural", rate="+0%", pitch="+30%", style="cheerful")
        if result.reason != ResultReason.SynthesizingAudioCompleted:
            print("Failed to synthesize speech.")
    except:
        print("Error occurred while synthesizing speech.")

if __name__ == "__main__":
    say("Hello what can I do")
