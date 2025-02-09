"use client";

import { useState, useEffect } from 'react';

interface Game {
    appid: number;
    name: string;
    playtime_forever: number;
    img_icon_url: string;
    playtime_hours: number;
}

export default function GameProfile() {
    const [selectedGame, setSelectedGame] = useState<Game | null>(null);
    const [games, setGames] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('game');
    const [achievements, setAchievements] = useState<any>(null);
    const [loadingAchievements, setLoadingAchievements] = useState(false);

    const playerInfo = {
        name: "Complexia",
        steamId: "76561198061149842",
        username: "complexia"
    };

    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await fetch('/server/steam/player/76561198061149842/games');
                const data = await response.json();
                setGames(data);
            } catch (error) {
                console.error('Error fetching games:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchGames();
    }, []);

    const fetchAchievements = async (appId: number) => {
        setLoadingAchievements(true);
        try {
            const response = await fetch(`/server/steam/player/${playerInfo.steamId}/achievements/${appId}`);
            const data = await response.json();
            setAchievements(data);
        } catch (error) {
            console.error('Error fetching achievements:', error);
        } finally {
            setLoadingAchievements(false);
        }
    };

    const handleTabChange = (tab: string) => {
        setActiveTab(tab);
        if (tab === 'achievements' && selectedGame) {
            fetchAchievements(selectedGame.appid);
        }
    };

    const handleGameClick = (game: Game) => {
        if (selectedGame?.appid === game.appid) {
            setSelectedGame(null);
        } else {
            setSelectedGame(game);
        }
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <div className="loading loading-spinner loading-lg"></div>
            </div>
        );
    }

    if (!games) {
        return <div>Error loading games</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <div className="flex flex-col md:flex-row gap-4">
                {/* Player Info Column */}
                <div className="card bg-base-200 shadow-xl p-6 md:w-1/4">
                    <h2 className="card-title text-2xl mb-4">Player Profile</h2>
                    <div className="space-y-2">
                        <p><span className="font-bold">Name:</span> {playerInfo.name}</p>
                        <p><span className="font-bold">Steam ID:</span> {playerInfo.steamId}</p>
                        <p><span className="font-bold">Username:</span> {playerInfo.username}</p>
                    </div>
                </div>

                {/* Games List Column */}
                <div className="card bg-base-200 shadow-xl p-6 md:w-1/3">
                    <h2 className="card-title text-2xl mb-4">Games Library</h2>
                    <div className="space-y-2">
                        {games.response.games.map((game: Game) => (
                            <div
                                key={game.appid}
                                className="card bg-base-100 hover:bg-base-300 cursor-pointer transition-colors"
                                onClick={() => handleGameClick(game)}
                            >
                                <div className="card-body p-4">
                                    <h3 className="card-title text-lg">{game.name}</h3>
                                    <p className="text-sm">Playtime: {game.playtime_hours.toFixed(1)} hours</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Game Details Column */}
                {selectedGame && (
                    <div className="card bg-base-200 shadow-xl p-6 md:w-1/3">
                        <div className="tabs tabs-boxed mb-4">
                            <a 
                                className={`tab ${activeTab === 'game' ? 'tab-active' : ''}`}
                                onClick={() => handleTabChange('game')}
                            >
                                Game
                            </a>
                            <a 
                                className={`tab ${activeTab === 'achievements' ? 'tab-active' : ''}`}
                                onClick={() => handleTabChange('achievements')}
                            >
                                Achievements
                            </a>
                        </div>

                        {activeTab === 'game' && (
                            <div className="space-y-4">
                                <img 
                                    src={selectedGame.img_icon_url} 
                                    alt={selectedGame.name}
                                    className="w-16 h-16 rounded"
                                />
                                <h3 className="text-xl font-bold">{selectedGame.name}</h3>
                                <div className="space-y-2">
                                    <p><span className="font-bold">App ID:</span> {selectedGame.appid}</p>
                                    <p><span className="font-bold">Total Playtime:</span> {selectedGame.playtime_hours.toFixed(1)} hours</p>
                                </div>
                            </div>
                        )}

                        {activeTab === 'achievements' && (
                            <div className="space-y-4">
                                {loadingAchievements ? (
                                    <div className="flex justify-center">
                                        <div className="loading loading-spinner loading-md"></div>
                                    </div>
                                ) : achievements?.playerstats?.achievements ? (
                                    <div className="space-y-2">
                                        {achievements.playerstats.achievements.map((achievement: any) => (
                                            <div 
                                                key={achievement.apiname}
                                                className={`p-3 rounded ${achievement.achieved ? 'bg-success/20' : 'bg-base-100'}`}
                                            >
                                                <h4 className="font-bold">{achievement.name}</h4>
                                                {achievement.description && (
                                                    <p className="text-sm">{achievement.description}</p>
                                                )}
                                                <p className="text-xs mt-1">
                                                    {achievement.achieved ? 
                                                        `Unlocked: ${new Date(achievement.unlocktime * 1000).toLocaleDateString()}` : 
                                                        'Not achieved'}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p>No achievements data available</p>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

