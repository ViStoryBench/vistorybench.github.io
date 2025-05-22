// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

// https://astro.build/config
export default defineConfig({
  // 使用 vite 配置直接处理 tailwind
  vite: {
    css: {
      postcss: {
        plugins: [
          // 直接内联配置 Tailwind
          tailwindcss({
            content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
            darkMode: 'class',
            safelist: [
              // Globals and Header related
              'bg-white',
              'dark:bg-slate-900',
              'text-gray-800',
              'dark:text-slate-200',
              'border-gray-200',
              'dark:border-slate-700',
              'bg-gray-100',
              'text-gray-700',
              'dark:text-slate-300',
              'hover:text-sky-600',
              'dark:hover:text-sky-400',
              'bg-sky-500',
              'text-white',
              'dark:bg-sky-500',
              'dark:text-white',
              
              // Story Detail Page classes
              'p-4', 'p-6',
              'mb-2', 'mb-4', 'mb-6',
              'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl',
              'font-semibold',
              'rounded-lg', 'rounded-xl', 'rounded-2xl',
              'bg-gray-50',
              'dark:bg-slate-800',
              'dark:bg-opacity-50',
              'border',
              'border-transparent',
              'shadow-lg',
              'hover:bg-gray-100',
              'dark:hover:bg-slate-700',
              'grid', 'grid-cols-1', 'md:grid-cols-2', 'lg:grid-cols-3', 'gap-4', 'gap-x-4',
              'flex', 'items-center', 'justify-between', 'flex-col', 'flex-wrap',
              
              // Model visibility selector
              'bg-gray-200', 
              'dark:bg-gray-700', 
              'hover:bg-gray-300', 
              'dark:hover:bg-gray-600',
              'px-3', 'py-1', 'px-4', 'py-2', 
              
              // Model containers & focus
              'border-2',
              'border-blue-500', 
              'dark:border-sky-400',
              'ring-2',
              'ring-offset-2',
              'ring-blue-500',
              'dark:ring-sky-400',
              'dark:ring-offset-slate-900',
              'opacity-50',
              'opacity-100',
              
              // Character reference images
              'w-20', 'h-20', 'w-24', 'h-24', 'object-cover',
            ],
            theme: {
              extend: {},
            },
            plugins: [],
          }),
          autoprefixer(),
        ],
      },
    },
  },
  base: '/bmk_leaderboard/', 
});