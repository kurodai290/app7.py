import random
import time

class BorderlandTrain:
    def __init__(self, num_players=5, num_cars=4):
        self.num_players = num_players
        self.num_cars = num_cars
        self.players = {f"Player_{i+1}": {"car": 0, "is_heart": False} for i in range(num_players)}
        
        # ターゲット（ハート）を一人決める
        heart_id = f"Player_{random.randint(1, num_players)}"
        self.players[heart_id]["is_heart"] = True
        self.user_id = "Player_1"

    def play_turn(self, turn):
        print(f"\n--- Turn {turn} ---")
        # ユーザーの移動
        print(f"現在地: {self.players[self.user_id]['car']}号車")
        try:
            move = int(input(f"どこへ移動しますか？ (0-{self.num_cars-1}): "))
            if 0 <= move < self.num_cars:
                self.players[self.user_id]["car"] = move
        except ValueError:
            print("無効な入力です。その場に留まります。")

        # NPCの移動（ランダム）
        for p_id, info in self.players.items():
            if p_id != self.user_id:
                info["car"] = random.randint(0, self.num_cars - 1)

        # 車両ごとの状況確認
        car_occupants = {i: [] for i in range(self.num_cars)}
        for p_id, info in self.players.items():
            car_occupants[info["car"]].append(p_id)

        # 生存判定（ハートと同じ車両にいたらアウト）
        for car, occupants in car_occupants.items():
            has_heart = any(self.players[p]["is_heart"] for p in occupants)
            print(f"[{car}号車]: {', '.join(occupants)}")
            
            if has_heart and len(occupants) > 1:
                for p in occupants:
                    if not self.players[p]["is_heart"]:
                        print(f"⚠️ {p} は排除されました...")
                        # 実際にはここでリストから削除するなどの処理

    def start(self):
        print("【今際の国のアリス：暴走電車】開始")
        if self.players[self.user_id]["is_heart"]:
            print("あなたは【ハート】です。正体を隠して他全員を排除してください。")
        else:
            print("あなたは【一般】です。ハートと同じ車両を避け、生き残ってください。")
        
        for t in range(1, 6):
            self.play_turn(t)
            time.sleep(1)

game = BorderlandTrain()
game.start()
