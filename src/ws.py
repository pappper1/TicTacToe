from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from.game import Game

class WSGame(WebSocketEndpoint):

	encoding = 'json'
	actions = ['create', 'new', 'join']
	games = []
	current_games = []

	async def create_game(self, ws: WebSocket) -> None:
		game = await Game().create(ws)
		self.games.append(game)

	async def join_game(self, ws: WebSocket, number: int) -> None:
		game = self.games.pop(number-1)
		self.current_games.append(game)
		await game.join_player(ws)
		return game

	async def on_connect(self, websocket: WebSocket) -> None:
		await websocket.accept()

	async def on_receive(self, websocket: WebSocket, data: bytes) -> None:
		if data['action'] in self.actions:
			if data['action'] == 'create':
				await self.create_game(websocket)
				await websocket.send_json({'action': 'create'})

			elif data['action'] == 'new':
				await websocket.send_json({'action': 'new', 'games': len(self.games)})

			elif data['action'] == 'join':
				game = await self.join_game(websocket, int(data['game']))
				await websocket.send_json({
					'action': 'join',
					'other_player': await game.player_1.get_state(),
					'player': await game.player_2.get_state(),
				})
				ws = await game.player_1.get_ws()
				await ws.send_json({
					'action':'join',
					'other_player':await game.player_1.get_state(),
					'player':await game.player_2.get_state(),
				})

	async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
		pass