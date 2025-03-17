# bot.py

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Function to fetch weather data (example using OpenWeatherMap API)
def get_weather(city="Sukkur"):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Get your API key from openweathermap.org
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Weather in {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    return "Could not fetch weather data."

# Handler for /start command with an interactive button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Say Hello!", callback_data="hello")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to the Interactive Telegram Bot! Click the button below to say hello!",
        reply_markup=reply_markup
    )

# Handler for button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Hello! Thanks for interacting with me!")

# Handler for /task command (simulates task automation)
async def task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Task automated! Current timestamp: {current_time}")

# Handler for /weather command (real-time API integration)
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    weather_data = get_weather()
    await update.message.reply_text(weather_data)

def main() -> None:
    # Initialize the bot application
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", task))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    print("Bot is starting...")
    app.run_polling(allow_updates=True)

if __name__ == "__main__":
    main()