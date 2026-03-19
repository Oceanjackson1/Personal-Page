import zh from './zh.json';
import en from './en.json';

const translations = { zh, en } as const;
export type Lang = keyof typeof translations;
export const defaultLang: Lang = 'zh';
export const languages = { zh: '中', en: 'EN' } as const;

export function t(lang: Lang = defaultLang) {
  return translations[lang];
}

export function getLangFromStorage(): Lang {
  if (typeof window === 'undefined') return defaultLang;
  return (localStorage.getItem('lang') as Lang) || defaultLang;
}
