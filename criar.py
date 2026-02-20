import sqlite3, bcrypt

conn = sqlite3.connect("ocorrencias.db")
cursor = conn.cursor()

senha_hash = bcrypt.hashpw("1234".encode(), bcrypt.gensalt())
cursor.execute("INSERT INTO usuarios (usuario, senha, nivel) VALUES (?,?,?)",
               ("admin", senha_hash, "admin"))

conn.commit()
conn.close()
print("ADMIN criado!")