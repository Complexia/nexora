use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token};
use anchor_spl::metadata::{
    create_metadata_accounts_v3,
    CreateMetadataAccountsV3,
    Metadata,
};

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod player_games {
    use super::*;

    pub fn initialize_collection(ctx: Context<InitializeCollection>) -> Result<()> {
        // Initialize collection for PlayerGames
        Ok(())
    }

    pub fn mint_game_nft(
        ctx: Context<MintGameNFT>,
        game_name: String,
        game_id: String,
        playtime: u64,
    ) -> Result<()> {
        // Mint NFT for a game
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
pub struct MintGameNFT<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
} 