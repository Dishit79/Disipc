# DisIpc

`pip install git+https://github.com/Dishit79/DisIpc.git#egg=disipc`

## Bot
```py
import discord
from discord.ext import commands
from disipc import server

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
ipc = server.IpcServer(client, key='key')

@client.event
async def on_ready():
    print("Bot is ready.")

@ipc.routes()
async def get_channels(data):
    guild = client.get_guild(data.guild_id)
    return len(guild.text_channels)

ipc.start()
client.run("TOKEN")
```

## Client
```py
from quart import Quart
from disipc import client

app = Quart(__name__)
ipc = client.IpcClient(key="key")

@app.route("/id=<id>")
async def index(id):
    data = await ipc.request('get_channels', guild_id=int(id))
    return str(data)

if __name__ == "__main__":
    app.run()

```
