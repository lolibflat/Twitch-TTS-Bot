import customtkinter as ctk
import threading
import pyttsx3
from twitchio.ext import commands

class MyBot(commands.Bot):
    def __init__(self, token, client_id, nick, volume, rate):
        super().__init__(token=token,
                         client_id=client_id,
                         nick=nick,
                         prefix='!',
                         initial_channels=[nick])
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', volume)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_PT-BR_MARIA_11.0')

    async def event_message(self, message):
        message_text = message.content
        self.engine.say(message_text)
        self.engine.runAndWait()

class TTSBotApp:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = root
        self.root.geometry('420x520')
        self.root.title("TTS Bot Configuration")
        # Frame for Twitch authentication
        self.twitch_frame = ctk.CTkFrame(root)
        self.twitch_frame.pack(pady=20, padx=60)

        # Token input
        self.token_label = ctk.CTkLabel(self.twitch_frame, text="Twitch Token:")
        self.token_label.pack(pady=(10, 0), padx=15)
        self.token_entry = ctk.CTkEntry(self.twitch_frame, width=300, justify='center', show='*')
        self.token_entry.pack(pady=5, padx=15)

        # Client ID input
        self.client_id_label = ctk.CTkLabel(self.twitch_frame, text="Client ID:")
        self.client_id_label.pack(pady=(10, 0), padx=15)
        self.client_id_entry = ctk.CTkEntry(self.twitch_frame, width=300, justify='center', show='*')
        self.client_id_entry.pack(pady=5, padx=15)

        # Nickname input
        self.nick_label = ctk.CTkLabel(self.twitch_frame, text="Twitch username:")
        self.nick_label.pack(pady=(10, 0), padx=15)
        self.nick_entry = ctk.CTkEntry(self.twitch_frame, width=300, justify='center')
        self.nick_entry.pack(pady=(5, 15), padx=15)

        # Frame for volume, rate, and start/stop button
        self.control_frame = ctk.CTkFrame(root)
        self.control_frame.pack(pady=20, padx=15)

        # Volume input
        self.volume_label = ctk.CTkLabel(self.control_frame, text="Volume (0.0 to 1.0):")
        self.volume_label.pack(pady=(10, 0), padx=15)
        self.volume_entry = ctk.CTkSlider(self.control_frame, from_=0.0, to=1.0)
        self.volume_entry.pack(pady=5, padx=15)

        # Rate input
        self.rate_label = ctk.CTkLabel(self.control_frame, text="Rate (words per minute):")
        self.rate_label.pack(pady=(10, 0), padx=15)
        self.rate_entry = ctk.CTkSlider(self.control_frame, from_=0.0, to=300.0)
        self.rate_entry.pack(pady=5, padx=15)

        # Start/Stop button
        self.toggle_button = ctk.CTkButton(self.control_frame, text="Start Bot", command=self.toggle_bot)
        self.toggle_button.pack(pady=20, padx=15)

        self.bot = None
        self.bot_thread = None
        self.is_bot_running = False

    def toggle_bot(self):
        if self.is_bot_running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        token = self.token_entry.get()
        client_id = self.client_id_entry.get()
        nick = self.nick_entry.get()
        volume = float(self.volume_entry.get())
        rate = int(self.rate_entry.get())

        self.bot = MyBot(token, client_id, nick, volume, rate)
        self.bot_thread = threading.Thread(target=self.bot.run)
        self.bot_thread.start()

        self.toggle_button.configure(text="Stop Bot")
        self.is_bot_running = True

    def stop_bot(self):
        if self.bot:
            self.bot.close()
            self.bot = None

        if self.bot_thread:
            self.bot_thread.join()
            self.bot_thread = None

        self.toggle_button.configure(text="Start Bot")
        self.is_bot_running = False

if __name__ == "__main__":
    root = ctk.CTk()
    app = TTSBotApp(root)
    root.mainloop()
