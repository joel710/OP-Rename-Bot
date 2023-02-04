import bot

if __name__ == "__main__":
    if hasattr(bot, 'run'):
        bot.run()
    else:
        print("Le module 'bot' ne contient pas de méthode 'run'.")
