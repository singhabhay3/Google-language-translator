from tkinter import *
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import speech_recognition as sr
from langdetect import detect
from textblob import TextBlob

class LanguageTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.geometry("800x600")
        master.config(bg="#f0f0f0")
        master.title("Language Translator")

        self.create_widgets()
        
    def create_widgets(self):
        # Input Area
        self.input_text = Text(self.master, bg="white", fg="black", font=("Arial", 20), wrap="word")
        self.input_text.place(x=100, y=30, width=600, height=150)
        self.input_text.bind("<Key>", self.update_cursor)

        # Output Area
        self.translated_label = Label(self.master, text="", bg="white", fg="black", font=("Arial", 20), wraplength=600)
        self.translated_label.place(x=100, y=400, width=600, height = 120)
        self.translated_label.config(anchor=NW)

        # Dropdown Menu
        lang_options = self.fetch_language_options()
        self.drop_down = StringVar()
        self.drop_down.set("Select Language")

        list_lang = OptionMenu(self.master, self.drop_down, *lang_options)
        list_lang.configure(bg="#ffcc00", fg="black", font=("Arial", 16, "bold"))
        list_lang.place(x=160, y=250, width=250, height=40)

        # Translate Button
        translate_b = Button(self.master, text="Translate", bg="#e60000", fg="white", font=("Arial", 20),
                             command=self.translate_language)
        translate_b.place(x=440, y=240, width=150, height=60)

        # Speaker Buttons
        self.speak_input_button = Button(self.master, text="Speak Input", bg="#0077cc", fg="white",
                                         font=("Arial", 16), command=self.speak_input)
        self.speak_input_button.place(x=100, y=200, width=150, height=40)

        self.speak_output_button = Button(self.master, text="Speak Output", bg="#008000", fg="white",
                                          font=("Arial", 16), command=self.speak_output)
        self.speak_output_button.place(x=560, y=550, width=150, height=40)

        # Custom Cursor
        self.cursor_canvas = Canvas(self.master, bg="white", bd=0, highlightthickness=0)
        # self.cursor_canvas.place(x=100, y=30, width=600, height=150)
        self.cursor_id = self.cursor_canvas.create_line(0, 0, 0, 20, fill="black")

    def fetch_language_options(self):
        return ["Hindi", "Punjabi", "Gujarati", "Tamil", "Telugu", "Bengali", "Marathi"]

    def get_target_language(self, selected_language):
        language_mapping = {
            "Hindi": "hi",
            "Punjabi": "pa",
            "Gujarati": "gu",
            "Tamil": "ta",
            "Telugu": "te",
            "Bengali": "bn",
            "Marathi": "mr"
        }
        return language_mapping.get(selected_language)

    def translate_language(self):
        n1 = self.input_text.get("1.0", END)
        n3 = self.drop_down.get()

        if not n1.strip():
            self.translated_label.config(text="Please enter text to translate", wraplength=600)
            return

        target_language = self.get_target_language(n3)
        if not target_language:
            self.translated_label.config(text="Invalid language selection", wraplength=600)
            return

        try:
            if target_language:
                # Translate text
                text_translate = GoogleTranslator(source='auto', target=target_language).translate(n1)
                text_translate = text_translate.lower()
                self.translated_label.config(text=text_translate.capitalize(), wraplength=600)

                # Language Detection
                detected_lang = detect(n1)
                self.input_text.insert(END, f"\n\nDetected Language: {detected_lang.upper()}")

                # Sentiment Analysis
                blob = TextBlob(n1)
                sentiment_score = blob.sentiment.polarity
                sentiment_label = "Positive" if sentiment_score > 0.1 else "Negative" if sentiment_score < -0.1 else "Neutral"
                self.input_text.insert(END, f"\nSentiment: {sentiment_label}")

            else:
                self.translated_label.config(text="Invalid language selection", wraplength=600)

        except Exception as e:
            print(f"Translation error: {e}")
            self.translated_label.config(text="Translation failed", wraplength=600)

    def speak_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            input_text = recognizer.recognize_google(audio, language='hi-IN')  # For Hindi, you can use 'hi-IN'
            self.input_text.delete("1.0", END)
            self.input_text.insert(END, input_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def speak_output(self):
        output_text = self.translated_label.cget("text")
        target_language = self.get_target_language(self.drop_down.get())
        self.text_to_speech(output_text, lang_code=target_language)

    def text_to_speech(self, text, lang_code):
        try:
            speech = gTTS(text=text, lang=lang_code, slow=False)
            speech.save("output.mp3")
            os.system("start output.mp3")
        except Exception as e:
            print(f"Text-to-speech error: {e}")

    def update_cursor(self, event):
        cursor_pos = self.input_text.index(INSERT)
        cursor_bbox = self.input_text.bbox(cursor_pos)
        if cursor_bbox:
            cursor_x, cursor_y = cursor_bbox[:2]
            self.cursor_canvas.coords(self.cursor_id, cursor_x + 100, cursor_y, cursor_x + 100, cursor_y + 20)

if __name__ == "__main__":
    root = Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()