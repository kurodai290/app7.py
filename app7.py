"""
今際の国のアリス 風ゲーム：『暴走電車』
GitHub公開用ソースコード
"""

import random
import time
import sys

class BorderlandTrain:
    def __init__(self, num_players=5, num_cars=4):
        self.num_players = num_players
        self.num_cars = num_cars
        # 生存フラグ(is_alive)を管理
        self.players = {
            f"Player_{i+1}": {"car": 0, "is_heart": False, "is_alive": True} 
            for i in range(num_players)
        }
        
        # ハート（ターゲット）を決定
        heart_id = f"Player_{random.randint(1, num_players)}"
        self.players[heart_id]["is_heart"] = True
        self.user_id = "Player_1"

    def play_turn(self, turn):
        print(f"\n====================\n   TURN {turn} / 5\n====================")
        
        # 1. ユーザーの移動
        if self.players[self.user_id]["is_alive"]:
            print(f"現在地: {self.players[self.user_id]['car']}号車")
            while True:
                try:
                    move = input(f"移動先を選んでください (0-{self.num_cars-1}): ")
                    move = int(move)
                    if 0 <= move < self.num_cars:
                        self.players[self.user_id]["car"] = move
                        break
                    else:
                        print(f"エラー: 0から{self.num_cars-1}の間で入力してください。")
                except ValueError:
                    print("エラー: 数字を入力してください。")

        # 2. NPC（生存者）の移動
        for p_id, info in self.players.items():
            if p_id != self.user_id and info["is_alive"]:
                info["car"] = random.randint(0, self.num_cars - 1)

        print("\n移動中...")
        time.sleep(1)

        # 3. 車両状況の集計
        car_occupants = {i: [] for i in range(self.num_cars)}
        for p_id, info in self.players.items():
            if info["is_alive"]:
                car_occupants[info["car"]].append(p_id)

        # 4. 生存判定
        for car, occupants in car_occupants.items():
            has_heart = any(self.players[p]["is_heart"] for p in occupants)
            print(f"[{car}号車]: {' / '.join(occupants)}")
            
            if has_heart:
                for p in occupants:
                    if not self.players[p]["is_heart"]:
                        print(f" ⚠️  {p} は【ハート】に遭遇し、排除されました。")
                        self.players[p]["is_alive"] = False

    def start(self):
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  今際の国のアリス：暴走電車 (Crazy Train)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        is_user_heart = self.players[self.user_id]["is_heart"]
        if is_user_heart:
            print("【ROLE】あなたは【ハート】です。")
            print("潜伏しながら他のプレイヤーと同じ車両に入り、全員を排除してください。")
        else:
            print("【ROLE】あなたは【一般参加者】です。")
            print("5ターンの間、ハートのいる車両を避け、生き残ってください。")
        
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
                    print("\nGAME CLEAR: 全員を排除しました！あなたの勝利です。")
                else:
                    print("\nGAME OVER: 全員が排除されました。")
                return
                
            time.sleep(0.5)
        
        print("\nGAME CLEAR: 5ターン生き残りました。無事に生還です！")

if __name__ == "__main__":
    try:
        game = BorderlandTrain()
        game.start()
    except KeyboardInterrupt:
        print("\n中断されました。")
    finally:
        # 直接実行した時に画面がすぐに閉じないようにする
        input("\nEnterキーを押して終了します...")
