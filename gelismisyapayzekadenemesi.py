import tkinter as tk
import sqlite3
import numpy as np
import transformers
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- MODEL ----------------
embedder = SentenceTransformer("Sonul Paşa")

# ---------------- HAFIZA ----------------
conn = sqlite3.connect("brain.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    embedding BLOB,
    reward INTEGER
)
""")
conn.commit()

# ---------------- YARDIMCI ----------------
def to_blob(vec):
    return vec.astype(np.float32).tobytes()

def from_blob(blob):
    return np.frombuffer(blob, dtype=np.float32)

# ---------------- HAFIZA OKUMA ----------------
def recall(query):
    q_vec = embedder.encode([query])
    cur.execute("SELECT text, embedding, reward FROM memory")
    rows = cur.fetchall()

    if not rows:
        return "Henüz hiçbir şey bilmiyorum.", None

    best_score = -1
    best_text = None

    for text, emb, reward in rows:
        vec = from_blob(emb)
        score = cosine_similarity([vec], q_vec)[0][0]
        score += reward * 0.1  # ödül etkisi

        if score > best_score:
            best_score = score
            best_text = text

    return best_text, best_score

# ---------------- ÖĞRENME ----------------
def learn(text, reward):
    vec = embedder.encode([text])[0]
    cur.execute(
        "INSERT INTO memory (text, embedding, reward) VALUES (?,?,?)",
        (text, to_blob(vec), reward)
    )
    conn.commit()

# ---------------- AI BEYNİ ----------------
def ai_response(user_text):
    memory, score = recall(user_text)

    if score is None or score < 0.4:
        return "Bu konuda yeterince bilgim yok. Bana öğretir misin?"
    return memory

# ---------------- GUI ----------------
def send():
    user_text = entry.get()
    if not user_text:
        return

    chat.insert(tk.END, f"Sen: {user_text}\n")
    response = ai_response(user_text)
    chat.insert(tk.END, f"AI: {response}\n\n")
    entry.delete(0, tk.END)

def reward_good():
    last = chat.get("end-3l", "end-2l").replace("AI: ", "").strip()
    learn(last, 1)
    chat.insert(tk.END, "✅ Öğrendim (iyi cevap)\n\n")

def reward_bad():
    last = chat.get("end-3l", "end-2l").replace("AI: ", "").strip()
    learn(last, -1)
    chat.insert(tk.END, "❌ Öğrendim (kötü cevap)\n\n")

# ---------------- PENCERE ----------------
root = tk.Tk()
root.title("MiniMind AI v2")
root.geometry("520x650")

tk.Label(root, text="🧠 MiniMind AI – Seviye 2", font=("Arial", 16, "bold")).pack()

chat = tk.Text(root, height=22)
chat.pack(pady=10)

entry = tk.Entry(root, width=55)
entry.pack(pady=5)

tk.Button(root, text="Gönder", command=send, bg="green", fg="white").pack(pady=5)

tk.Frame(root).pack()

tk.Button(root, text="👍 İyi", command=reward_good, bg="blue", fg="white", width=12).pack(side="left", padx=40)
tk.Button(root, text="👎 Kötü", command=reward_bad, bg="red", fg="white", width=12).pack(side="right", padx=40)

root.mainloop()
