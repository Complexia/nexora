'use client';

import { SolanaConnectButton } from './solana-connect-button';

export default function Navbar() {
  return (
    <nav className="shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div>
            <SolanaConnectButton />
          </div>
          {/* <div className="text-xl font-bold">
            AI Chat
          </div> */}
          <div className="w-[120px]"> {/* Empty div for balance */}
          </div>
        </div>
      </div>
    </nav>
  );
} 