import time
import speech_recognition as sr
from manual_add import raw_lyrics
import regex as re

class LyricLine:
    def __init__(self, text):
        self.status = 'unplayed'
        self.text = text

class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics
        self.clean_lyrics()

    def delete_previous_lines(self, index):
        if index > 0:
            print(f"Deleting {index} previous lines...")
            self.lyrics = self.lyrics[index:]

    def update_lyric_status(self, sung_text):
        if not sung_text:
            return

        sung_text_lower = sung_text.lower()

        # If a line is currently playing
        for i, curr_ly in enumerate(self.lyrics):
            if curr_ly.status == 'currently_playing':
                if sung_text_lower in curr_ly.text.lower():
                    return  # Still singing the same line
                else:
                    # Try to find the next line being sung
                    for j in range(i + 1, len(self.lyrics)):
                        if sung_text_lower in self.lyrics[j].text.lower():
                            curr_ly.status = 'played'
                            self.lyrics[j].status = 'currently_playing'
                            self.delete_previous_lines(j)
                            return
                return

        # If no line is currently playing, try to find the line being sung
        for i, lyric in enumerate(self.lyrics):
            if lyric.status == 'unplayed' and sung_text_lower in lyric.text.lower():
                for j in range(i):
                    self.lyrics[j].status = 'played'
                lyric.status = 'currently_playing'
                self.delete_previous_lines(i)
                return

    def get_current_lyric(self):
        for lyric in self.lyrics:
            if lyric.status == 'currently_playing':
                print(lyric.text)
                return
        print("no line matched yet")

    def listen_and_update(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        print("Start singing! (Say something when you're ready)")
        while True:
            # Stop if all lines are played
            if all(lyric.status == 'played' for lyric in self.lyrics):
                print("\n🎉 Song finished!")
                break

            sung_text = ''
            with microphone as source:
                print("\nListening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = recognizer.listen(source, timeout=3)
                    sung_text = recognizer.recognize_google(audio)
                    print("Heard:", sung_text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    continue
                except sr.WaitTimeoutError:
                    print("Listening timed out")
                    continue

            self.update_lyric_status(sung_text)
            print("------ Current Lyric ------")
            self.get_current_lyric()

    def clean_lyrics(self):
        cleaned_lyrics = re.sub(r'\[.*?\]', '', lyrics)
        print(cleaned_lyrics)

# Sample lyrics (without timestamp)
lyrics = [
    LyricLine("This is the first line of the song"),
    LyricLine("This is the second line of the song"),
    LyricLine("This is the third line of the song"),
    LyricLine("This is the fourth line of the song")
]



# Start the song
song = Song(lyrics)
song.listen_and_update()