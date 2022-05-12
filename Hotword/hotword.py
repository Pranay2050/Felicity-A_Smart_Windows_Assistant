import struct
import pyaudio
import pvporcupine

porcupine = None
pa = None
audio_stream = None


def get_porcupine():
    return pvporcupine.create(keyword_paths=['felicity.ppn'], sensitivities = [1.0])

def check_hotword(porcupine):
    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Hotword Detected")
            return True
            
