from kivy.core.audio import SoundLoader

sound = SoundLoader.load('mywav.wav')
if sound:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()