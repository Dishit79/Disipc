import aiohttp.web


def routes():
    def decorater(func):
        IpcServer.cogendpoints[func.__name__] = func
    return decorater


class ServerResponse:
    def __init__(self, data: dict):
        self.endpoint = data["endpoint"]

        for key, value in data["data"].items():
            setattr(self, key, value)


class IpcServer():

    cogendpoints={}

    def __init__(self, client, key, port:int = 8080, host='localhost'):

        self.client = client
        self.loop = client.loop
        self.port = port
        self.host = host
        self.key = key
        self.endpoints = {}

    def routes(self):
        def decorater(func):
            self.endpoints[func.__name__] = func
        return decorater

    def update_endpoints(self):
        self.endpoints.update(IpcServer.cogendpoints)
        IpcServer.cogroutes = {}

    async def websocket_handler(self, request):

        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:

            request = msg.json()
            endpoint = request.get("endpoint")
            headers = request.get("headers")

            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    if not headers['Authorization'] or headers['Authorization']!= self.key:
                        return await ws.send_json({'error':'Authorization failed', 'code':'401'})
                    if not endpoint or endpoint not in self.endpoints:
                        return await ws.send_json({'error':'Endpoint not found', 'code':'400'})
                    data = (ServerResponse(request),)
                    self.update_endpoints()
                    classes = self.client.cogs.get(self.endpoints[endpoint].__qualname__.split(".")[0])
                    if classes:
                        response = await self.endpoints[endpoint](classes, *data)
                    else:
                        response = await self.endpoints[endpoint](*data)
                    await ws.send_str(str(response))

            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')

        return ws


    async def server_start(self,application):
        runner = aiohttp.web.AppRunner(application)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, self.host, self.port)
        await site.start()

    def start(self,):
        app = aiohttp.web.Application()
        app.add_routes([aiohttp.web.route('GET', '/', self.websocket_handler)])
        self.loop.run_until_complete(self.server_start(app))
