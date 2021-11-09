from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

speech_config = SpeechConfig(subscription="06ee11a748eb4523b8ae1dd8739d0023", region="eastus")

# audio_config = AudioOutputConfig(filename="output.wav")
# synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
# synthesizer.speak_text_async("A simple test to write to a file.")
# audio_config = AudioOutputConfig(use_default_speaker=True)
# result = synthesizer.speak_text_async("Getting the response as an in-memory stream.").get()
# stream = AudioDataStream(result)


# Custom voice


speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

ssml_string = open("ssml.xml", "r", encoding="utf8").read()
result = synthesizer.speak_ssml_async(ssml_string).get()

stream = AudioDataStream(result)
stream.save_to_wav_file("D:/file.wav")

# print(synthesizer.synthesis_word_boundary())

# To change the voice without using SSML, you can set the property on the SpeechConfig by using

# SpeechConfig.speech_synthesis_voice_name = "en-US-AriaNeural"
