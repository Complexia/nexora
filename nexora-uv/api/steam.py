from fastapi import APIRouter, HTTPException
import httpx
from typing import Optional, Dict, Any
import os
from urllib.parse import urlparse

router = APIRouter(prefix="/steam")

# Get Steam API key from environment variables
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    raise ValueError("Steam API key not found in environment variables")

# Base URL for Steam API
STEAM_API_BASE_URL = "https://api.steampowered.com"

async def get_player_summary(steam_id: str) -> Dict[Any, Any]:
    """Fetch player summary from Steam API"""
    url = f"{STEAM_API_BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steam_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch player data")
        return response.json()

async def get_player_stats(steam_id: str, app_id: int) -> Dict[Any, Any]:
    """Fetch player stats for a specific game"""
    url = f"{STEAM_API_BASE_URL}/ISteamUserStats/GetUserStatsForGame/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "appid": app_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            error_detail = "Failed to fetch player stats"
            raw_response = response.text
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_detail = error_data.get('message') or error_data.get('error') or error_detail
            except:
                pass
            
            print(f"\nSteam API Error (Status {response.status_code}):")
            print(f"Error message: {error_detail}")
            print(f"Raw response: {raw_response}\n")
            
            raise HTTPException(
                status_code=response.status_code, 
                detail={
                    "message": error_detail,
                    "raw_response": raw_response
                }
            )
        return response.json()

async def get_player_achievements(steam_id: str, app_id: int) -> Dict[Any, Any]:
    """Fetch player achievements for a specific game"""
    url = f"{STEAM_API_BASE_URL}/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "appid": app_id,
        "l": "en"  # Language code for achievement names/descriptions
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            error_detail = "Failed to fetch player achievements"
            raw_response = response.text
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_detail = error_data.get('message') or error_data.get('error') or error_detail
            except:
                pass
            
            raise HTTPException(
                status_code=response.status_code, 
                detail={
                    "message": error_detail,
                    "raw_response": raw_response
                }
            )
        return response.json()

async def get_player_items(steam_id: str, app_id: int) -> Dict[Any, Any]:
    """Fetch player's inventory items for a specific game"""
    url = f"{STEAM_API_BASE_URL}/IInventory/GetInventory/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "appid": app_id,
        "count": 5000  # Maximum items to retrieve
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            error_detail = "Failed to fetch player inventory"
            raw_response = response.text
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_detail = error_data.get('message') or error_data.get('error') or error_detail
            except:
                pass
            
            raise HTTPException(
                status_code=response.status_code, 
                detail={
                    "message": error_detail,
                    "raw_response": raw_response
                }
            )
        return response.json()

async def get_steam_id(identifier: str) -> str:
    """Convert various Steam identifier formats to Steam ID64"""
    if identifier.isdigit() and len(identifier) == 17:
        return identifier
    
    if identifier.startswith(('http://', 'https://')):
        parsed_url = urlparse(identifier)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            if path_parts[0] == 'profiles' and path_parts[1].isdigit():
                return path_parts[1]
            elif path_parts[0] == 'id':
                url = f"{STEAM_API_BASE_URL}/ISteamUser/ResolveVanityURL/v1/"
                params = {
                    "key": STEAM_API_KEY,
                    "vanityurl": path_parts[1]
                }
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        if data['response']['success'] == 1:
                            return data['response']['steamid']
    
    raise HTTPException(status_code=400, detail="Invalid Steam identifier format")

async def get_owned_games(steam_id: str) -> Dict[Any, Any]:
    """Fetch list of owned games from Steam API"""
    url = f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "format": "json",
        "include_appinfo": 1,  # Include game names and logo information
        "include_played_free_games": 1  # Include free games if played
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            error_detail = "Failed to fetch owned games"
            raw_response = response.text
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_detail = error_data.get('message') or error_data.get('error') or error_detail
            except:
                pass
            
            raise HTTPException(
                status_code=response.status_code, 
                detail={
                    "message": error_detail,
                    "raw_response": raw_response
                }
            )
        return response.json()

@router.get("/player/{identifier}")
async def get_player_data(identifier: str, app_id: Optional[int] = None):
    """Get player data including account details and optionally game stats"""
    try:
        steam_id = await get_steam_id(identifier)
        player_summary = await get_player_summary(steam_id)
        
        response_data = {
            "player_summary": player_summary
        }
        
        if app_id:
            try:
                game_stats = await get_player_stats(steam_id, app_id)
                response_data["game_stats"] = game_stats
            except HTTPException as e:
                response_data["game_stats"] = {"error": "Failed to fetch game stats"}
        
        return response_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{identifier}/achievements/{app_id}")
async def get_player_achievement_data(identifier: str, app_id: int):
    """Get player achievements for a specific game"""
    try:
        steam_id = await get_steam_id(identifier)
        achievements = await get_player_achievements(steam_id, app_id)
        return achievements
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{identifier}/inventory/{app_id}")
async def get_player_inventory(identifier: str, app_id: int):
    """Get player's inventory items for a specific game"""
    try:
        steam_id = await get_steam_id(identifier)
        inventory = await get_player_items(steam_id, app_id)
        return inventory
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{identifier}/games")
async def get_player_games(identifier: str):
    """Get list of games owned by the player"""
    try:
        steam_id = await get_steam_id(identifier)
        games_data = await get_owned_games(steam_id)
        
        # Process the response to add full image URLs
        if 'response' in games_data and 'games' in games_data['response']:
            for game in games_data['response']['games']:
                if 'img_icon_url' in game:
                    game['img_icon_url'] = f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                if 'img_logo_url' in game:
                    game['img_logo_url'] = f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_logo_url']}.jpg"
                
                # Convert playtime from minutes to hours and round to 2 decimal places
                if 'playtime_forever' in game:
                    game['playtime_hours'] = round(game['playtime_forever'] / 60, 2)
                if 'playtime_2weeks' in game:
                    game['playtime_2weeks_hours'] = round(game['playtime_2weeks'] / 60, 2)
                
                # Add stats page URL if available
                if game.get('has_community_visible_stats'):
                    game['stats_url'] = f"http://steamcommunity.com/profiles/{steam_id}/stats/{game['appid']}"
        
        return games_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 