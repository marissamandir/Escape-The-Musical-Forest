from pydub import AudioSegment
from pydub.playback import play

# Load your audio file
sound = AudioSegment.from_file("Rainstorms.wav")

# Apply muffling by reducing the volume
muffled_sound = sound - 30  # Muffled version

# Create an echo by delaying the sound
echo_delay = 1000  # Delay in milliseconds
echo = muffled_sound - 30  # Muffled echo
echo = echo.fade_in(100).fade_out(100)  # Optional fade in/out for smoothness

# Overlay the echo on the muffled sound
final_sound = muffled_sound.overlay(echo)

# Export the modified audio
final_sound.export("Rainstorms-2.wav", format="wav")

# Optionally play the final sound


