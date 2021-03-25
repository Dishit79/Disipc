import asyncio
import aiohttp



class IpcClient:
    def __init__(self, key, port:int = 8080, host='localhost'):

        self.url= f'ws://{host}:{port}/'
        self.key = key
        self.session = None
        self.websocket = None


    async def init_connection(self):
        self.session = aiohttp.ClientSession()
        self.websocket = await self.session.ws_connect(self.url, autoping=False, autoclose=False)

        return self.websocket

    async def request(self, endpoint:str = None, **kwargs):

        if not self.session:
            await self.init_connection()

        payload = {
            "endpoint": endpoint,
            "data": kwargs,
            "headers": {"Authorization": self.key},
        }

        await self.websocket.send_json(payload)
        recv = await self.websocket.receive()

        if recv.type == aiohttp.WSMsgType.CLOSED:
            await self.session.close()
            await self.init_connection()
            return await self.request(endpoint, **kwargs)


        return(recv.json())
