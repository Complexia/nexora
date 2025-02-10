use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token};
use anchor_spl::metadata::{
    create_metadata_accounts_v3,
    CreateMetadataAccountsV3,
    Metadata,
};

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod player_achievements {
    use super::*;

    pub fn initialize_collection(ctx: Context<InitializeCollection>) -> Result<()> {
        // Initialize collection for PlayerGameAchievements
        Ok(())
    }

    pub fn mint_achievement_nft(
        ctx: Context<MintAchievementNFT>,
        game_id: String,
        achievement_name: String,
        achievement_description: String,
        unlock_time: i64,
    ) -> Result<()> {
        // Mint NFT for an achievement
        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitializeCollection<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct MintAchievementNFT<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
} 