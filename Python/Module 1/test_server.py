import server
import re

s = server.Server("ABCD")

s.set_style ("""
.start { background:green; color:white; }
""")

s.set_script("""

function runstart() {
    fetch("/start");
}

""")

s.set_body ("""
<button class="start" onclick="runstart()">Start</button>
""")


# --- Gestion des requêtes HTTP ---
def handle_request(s, path, conn):
    print("my handle request path=", path)
    if "/start" in path:
        print("START")
        # conn.send("HTTP/1.1 200 OK\r\n\r\n")
        conn.send(s.html())
        conn.close()
        
    return False

s.set_handler(handle_request)

s.run()
