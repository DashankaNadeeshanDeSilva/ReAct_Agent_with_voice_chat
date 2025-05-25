/// <reference types="vite/client" />

// env.d.ts
interface ImportMetaEnv {
    readonly VITE_API_GATEWAY_URL?: string;
    // add other env variables here as needed
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
  }