from fastapi import FastAPI
import httpx
import os

app = FastAPI()

# Environment variable names (NOT the actual values)
CLIENT_ID = os.getenv("1467576967489392796")
CLIENT_SECRET = os.getenv("bX3tdQ8rYvv2uE-TblO14fBYgwQAozhp")
GUILD_ID = os.getenv("1467576711402225717")

# Change this to your real Vercel URL
REDIRECT_URI = "https://your-project-name.vercel.app/api/callback"


@app.get("/api/login")
async def login():
    url = (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
    )
    return {"url": url}


@app.get("/api/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:

        # Exchange code for token
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        token_res = await client.post(
            "https://discord.com/api/oauth2/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        access_token = token_res.json()["access_token"]

        # Get guild list
        guilds_res = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        guilds = guilds_res.json()

        # Check if user is in your server
        if not any(str(g["id"]) == str(GUILD_ID) for g in guilds):
            return {"error": "Access denied. Not in server."}

        return {"status": "success", "message": "Welcome to the portal!"}
