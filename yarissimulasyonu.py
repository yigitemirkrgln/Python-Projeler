import random
import time

# Bir oyuncuyu temsil eden sınıf
class Player:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed  # oyuncunun hızını belirler
        self.position = 0  # Yarış yolundaki mevcut pozisyonu
        self.finished = False  # Yarışı bitirip bitirmediğini kontrol eder

    def move(self):
        # Hızına göre pozisyonu günceller
        self.position += random.uniform(0.5, 1.5) * self.speed

    def reset(self):
        self.position = 0
        self.finished = False

# Yapay Zeka oyuncusunu temsil eden sınıf
class AIPlayer(Player):
    def __init__(self, name, speed, intelligence):
        super().__init__(name, speed)
        self.intelligence = intelligence  # Yapay zeka seviyesini belirler

    def move(self):
        # Yapay zekanın hareketi, hızına ve zekasına göre hesaplanır
        if self.intelligence > random.uniform(0, 1):
            self.position += random.uniform(1.0, 2.0) * self.speed
        else:
            self.position += random.uniform(0.5, 1.0) * self.speed

# Yarış alanını temsil eden sınıf
class RaceTrack:
    def __init__(self, length):
        self.length = length  # Yarışın uzunluğu
        self.players = []  # Yarışçılar listesi

    def add_player(self, player):
        self.players.append(player)

    def race(self):
        # Yarışı başlatan metod
        print("Yarış başlıyor!")
        time.sleep(1)
        while not any(player.finished for player in self.players):
            for player in self.players:
                player.move()
                if player.position >= self.length and not player.finished:
                    player.finished = True
                    print(f"{player.name} yarışı bitirdi!")

            self.display_positions()

            # Kısa bir süre bekleyelim ki yarış daha heyecanlı olsun
            time.sleep(0.1)

        self.declare_winner()

    def display_positions(self):
        print("\nMevcut pozisyonlar:")
        for player in self.players:
            print(f"{player.name}: {player.position:.2f} km")
        print("\n")

    def declare_winner(self):
        # Kazananı açıklayan metod
        winners = [player for player in self.players if player.finished]
        if len(winners) > 0:
            print(f"\nKazanan: {winners[0].name}")
        else:
            print("Henüz kazanan yok.")

# Basit bir oyun arayüzü
class Game:
    def __init__(self):
        self.race_track = RaceTrack(10)  # Yarış yolu uzunluğu (10 km)
        self.players = []
        self.ai_players = []
        self.round = 1

    def add_player(self, player):
        self.players.append(player)

    def add_ai_player(self, ai_player):
        self.ai_players.append(ai_player)

    def start_race(self):
        print(f"--- {self.round}. YARIŞ ---")
        self.race_track = RaceTrack(10)  # Yeni bir yarış yolu başlatıyoruz
        for player in self.players + self.ai_players:
            self.race_track.add_player(player)
        self.race_track.race()

    def generate_ai_players(self, number_of_ai_players):
        for i in range(number_of_ai_players):
            ai_name = f"Yapay Zeka {i+1}"
            ai_speed = random.uniform(0.8, 1.5)  # AI oyuncusunun hızı
            ai_intelligence = random.uniform(0.5, 1.0)  # AI zekası
            ai_player = AIPlayer(ai_name, ai_speed, ai_intelligence)
            self.add_ai_player(ai_player)

    def run(self):
        # Oyunu başlat
        while True:
            print(f"\n--- {self.round}. YARIŞ ---")
            player_name = input("Oyuncu ismini girin (Çıkmak için 'q' basın): ")
            if player_name.lower() == 'q':
                print("Oyundan çıkılıyor...")
                break

            player_speed = random.uniform(1.0, 1.5)
            player = Player(player_name, player_speed)
            self.add_player(player)

            # Yapay zeka oyuncuları oluştur
            self.generate_ai_players(3)

            # Yarışı başlat
            self.start_race()

            # Sonraki yarışa geçmeden önce bir süre bekleyelim
            time.sleep(2)
            self.round += 1
            self.players = []  # Yeni yarış için oyuncuları sıfırlıyoruz
            self.ai_players = []  # Yeni yarış için AI oyuncuları sıfırlıyoruz

# Oyunu başlat
if __name__ == "__main__":
    game = Game()
    game.run()