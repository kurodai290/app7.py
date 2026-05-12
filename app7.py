import random
import time

class BorderlandTrain:
    def __init__(self, num_players=5, num_cars=4):
        self.num_players = num_players
        self.num_cars = num_cars
        # 生存フラグ(is_alive)を追加
        self.players = {
            f"Player_{i+1}": {"car": 0, "is_heart": False, "is_alive": True} 
            for i in range(num_players)
        }
        
        # ターゲット（ハート）を一人決める
        heart_id = f"Player_{random.randint(1, num_players)}"
        self.players[heart_id]["is_heart"] = True
        self.user_id = "Player_1"

    def play_turn(self, turn):
        print(f"\n--- Turn {turn} ---")
        
        # 1. プレイヤー（ユーザー）の移動
        if self.players[self.user_id]["is_alive"]:
            print(f"現在地: {self.players[self.user_id]['car']}号車")
            try:
                move = int(input(f"どこへ移動しますか？ (0-{self.num_cars-1}): "))
                if 0 <= move < self.num_cars:
                    self.players[self.user_id]["car"] = move
                else:
                    print("存在しない車両です。その場に留まります。")
            except ValueError:
                print("無効な入力です。その場に留まります。")

        # 2. NPCの移動（生存している者のみ）
        for p_id, info in self.players.items():
            if p_id != self.user_id and info["is_alive"]:
                info["car"] = random.randint(0, self.num_cars - 1)

        # 3. 車両ごとの状況確認（生存者のみカウント）
        car_occupants = {i: [] for i in range(self.num_cars)}
        for p_id, info in self.players.items():
            if info["is_alive"]:
                car_occupants[info["car"]].append(p_id)

        # 4. 生存判定
        for car, occupants in car_occupants.items():
            # その車両にハートがいるかチェック
            has_heart = any(self.players[p]["is_heart"] for p in occupants)
            print(f"[{car}号車]: {', '.join(occupants)}")
            
            if has_heart:
                # ハートと同じ車両にいる「一般プレイヤー」を排除
                for p in occupants:
                    if not self.players[p]["is_heart"]:
                        print(f"⚠️ {p} は排除されました...")
                        self.players[p]["is_alive"] = False

    def start(self):
        print("【今際の国のアリス：暴走電車】開始")
        is_user_heart = self.players[self.user_id]["is_heart"]
        
        if is_user_heart:
            print("あなたは【ハート】です。正体を隠して他全員を排除してください。")
        else:
            print("あなたは【一般】です。ハートと同じ車両を避け、生き残ってください。")
        
        for t in range(1, 6):
            self.play_turn(t)
            
            # ユーザーの生存チェック
            if not self.players[self.user_id]["is_alive"]:
                print("\nGAME OVER: あなたは排除されました。")
                return

            # ハート以外の生存者チェック
            survivors = [p for p, info in self.players.items() 
                        if not info["is_heart"] and info["is_alive"]]
            
            if not survivors:
                if is_user_heart:
                    print("\nGAME CLEAR: 全員を排除しました！")
                else:
                    print("\nGAME OVER: 全員排除されました。")
                return
                
            time.sleep(1)
        
        print("\nGAME CLEAR: 制限時間終了まで生き残りました！")

game = BorderlandTrain()
game.start()
