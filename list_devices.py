import pyaudio

p = pyaudio.PyAudio()
print(f"Default Host Api Info: {p.get_default_host_api_info()}")

count = p.get_device_count()
print(f"\nFound {count} devices:")

for i in range(count):
    try:
        info = p.get_device_info_by_index(i)
        print(f"ID {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")
    except Exception as e:
        print(f"ID {i}: Error getting info: {e}")

p.terminate()
