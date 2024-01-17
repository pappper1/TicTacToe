from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from.game import Game

class WSGame(WebSocketEndpoint):

	actions = ['create']
	games = []


	async def create_game(self, ws: WebSocket) -> None:
		game = await Game().create(ws)
		self.games.append(game)

	async def on_connect(self, websocket: WebSocket) -> None:
		await websocket.accept()

	async def on_receive(self, websocket: WebSocket, data: bytes) -> None:
		if data['action'] in self.actions:
			if data['action'] == 'create':
				pass