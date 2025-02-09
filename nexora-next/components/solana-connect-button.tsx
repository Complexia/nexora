'use client';

import { useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';

export function SolanaConnectButton() {
  const { wallet } = useWallet();

  return (
    <WalletMultiButton className="wallet-adapter-button" />
  );
} 