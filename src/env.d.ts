/// <reference types="astro/client" />

declare global {
  interface Window {
    amplitude?: {
      track: (eventName: string, properties?: Record<string, unknown>) => void;
      [key: string]: unknown;
    };
    __amplitudeInitialized?: boolean;
  }
}

export {};
