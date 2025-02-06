import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/server/:path*',
        destination: 'http://127.0.0.1:8000/:path*',
      },
    ];
  },
};

export default nextConfig;
