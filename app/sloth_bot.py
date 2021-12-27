import asyncio
import discord
import os
import random
import requests
import json
from auth import TOKEN
import datetime
from app import crypto
from app import weather

DEFAULT_RESPONSE = "HEYY YOUU GUUUYYYYSSSS!"
GOONIES_QUOTES = ["Jerk Alert!", "Goonies never say die!", DEFAULT_RESPONSE, "RUTH! RUTH! BABY! RUTH!", "CHHHOOOCCCOOLLAATTEE"]
CRYPTO_CHANNEL_ID = 917071848708141087
GENERAL_CHANNEL_ID = 917071541974487040
DEFAULT_MESSAGE_TIME = datetime.time(8, 0)

class SlothClient(discord.Client):

    def _get_quote(self):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return (quote)

    def _parse_message(self, message):
      print("Parsing message")

      if "island boy" in message.content:
        return "I'M AN ISSLLAANNDDD BBOOIIII"

      elif "get weather" in message.content:
        message = message.replace(",", "").replace(".", '').strip().split()
        message = message[message.index("weather"):]
        city = message[0]
        state = message[1]
        return weather.get_weather_forecast(city=city, state=state)
      elif "show coin" in message.content:
        # assume the coin is the last work in the message
        coin = message.content.split(" ")[-1]
        coin_data = crypto.get_coin_price(coin)
        if not coin_data or type(coin_data) is Exception:
            return "Oops! Something went wrong. Make sure the last word in the line is the symbol of the coin you want. Like BTC"
        else:
            return coin_data
      elif "menu" in message.content:
          return "Here are some things you can tell me:\n" \
                 "* @sloth show coin <crypto name>\n" \
                 "* @sloth get weather <city> <state abbreviation>\n" \
                 "* @sloth and I'll return something random\n"
      elif "digest" in message.content:
          return self._morning_message()
      else:
          return GOONIES_QUOTES[random.randint(0, len(GOONIES_QUOTES))]


      return DEFAULT_RESPONSE


    async def on_ready(self):
      print('Logged on as {0}!'.format(self.user))


    async def on_message(self, message):
      print(f'Message from {message.author}: {message.content}')
      if self.user.mentioned_in(message):
        print(f"Sloth was mentioned")
        response = self._parse_message(message)
        await message.channel.send(response)


    def _morning_message(self):
        message = "Good Morning\n"
        message += crypto.get_crypto_digest()
        weather_message = weather.get_weather_forecast()
        message += weather_message
        quote = self._get_quote()
        message += quote
        return message


    async def morning_message_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(CRYPTO_CHANNEL_ID)

        while not client.is_closed():
            try:
                now = datetime.datetime.now().astimezone(tz=datetime.timezone("US/Pacific"))
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                next_time = datetime.combine(tomorrow, DEFAULT_MESSAGE_TIME)
                time_to_sleep = next_time - now
                message = self._morning_message()
                await channel.send(message)
                await asyncio.sleep(time_to_sleep)
            except Exception as e:
                print(str(e))
                await asyncio.sleep(5)

if __name__ == "__main__":
  client = SlothClient()
  # print(client._get_quote())

  # client.loop.create_task(client.morning_message_task())
  client.run(TOKEN)
