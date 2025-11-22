// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';
import { readdir, readFile, writeFile, cp, mkdir, rm, stat } from 'node:fs/promises';
import { extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PROJECT_ROOT_DIR = fileURLToPath(new URL('.', import.meta.url));
const DATASET_SOURCE_DIR = join(PROJECT_ROOT_DIR, 'src', 'data');
const DATASET_ASSET_OUTPUT = 'dataset_assets';
const DATASET_FOLDERS_TO_COPY = [
  'dataset_lite_avif',
  'dataset_full_avif',
  'dataset_lite',
  'dataset_full',
];

// https://astro.build/config
export default defineConfig({
  base: './',
  build: {
    inlineStylesheets: 'always',
  },
  integrations: [
    copyDatasetAssetsIntegration(),
    stripHtmlCommentsIntegration(),
  ],
  // 使用 vite 配置直接处理 tailwind
  vite: {
    build: {
      minify: 'terser',
      terserOptions: {
        format: {
          comments: false,
        },
      },
      cssMinify: true,
    },
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
});

function copyDatasetAssetsIntegration() {
  return {
    name: 'copy-dataset-assets',
    hooks: {
      /**
       * @param {{ dir: string | URL }} param0
       */
      'astro:build:done': async ({ dir }) => {
        const distDir = typeof dir === 'string' ? dir : fileURLToPath(dir);
        const destRoot = join(distDir, DATASET_ASSET_OUTPUT);
        await mkdir(destRoot, { recursive: true });

        await Promise.all(DATASET_FOLDERS_TO_COPY.map(async (datasetFolder) => {
          const sourceDir = join(DATASET_SOURCE_DIR, datasetFolder);
          let sourceStats;
          try {
            sourceStats = await stat(sourceDir);
            if (!sourceStats.isDirectory()) {
              return;
            }
          } catch (error) {
            if (error && typeof error === 'object' && 'code' in error && error.code === 'ENOENT') {
              return;
            }
            throw error;
          }

          const targetDir = join(destRoot, datasetFolder);
          let shouldCopy = true;
          try {
            const targetStats = await stat(targetDir);
            if (targetStats.isDirectory() && targetStats.mtimeMs >= sourceStats.mtimeMs) {
              shouldCopy = false;
            }
          } catch (targetError) {
            if (!(targetError && typeof targetError === 'object' && 'code' in targetError && targetError.code === 'ENOENT')) {
              throw targetError;
            }
          }

          if (shouldCopy) {
            await rm(targetDir, { recursive: true, force: true });
            await cp(sourceDir, targetDir, { recursive: true });
          }
        }));
      },
    },
  };
}

function stripHtmlCommentsIntegration() {
  // Avoid traversing extremely large static asset folders that only contain binary files.
  const SKIP_DIRECTORIES = new Set([
    'outputs_lite_avif',
    'outputs_full_avif',
    'outputs_lite',
    'outputs_full',
    'dataset_lite_avif',
    'dataset_full_avif',
    'dataset_lite',
    'dataset_full',
    'dataset_assets',
  ]);
  const MAX_DEPTH = 4;

  /**
   * @param {string} dir
   * @param {number} [depth=0]
   * @returns {Promise<string[]>}
   */
  async function collectHtmlFiles(dir, depth = 0) {
    if (depth > MAX_DEPTH) {
      return [];
    }

    const entries = await readdir(dir, { withFileTypes: true });
    const htmlFiles = [];

    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (SKIP_DIRECTORIES.has(entry.name)) {
          continue;
        }
        htmlFiles.push(...await collectHtmlFiles(join(dir, entry.name), depth + 1));
        continue;
      }

      if (extname(entry.name) === '.html') {
        htmlFiles.push(join(dir, entry.name));
      }
    }

    return htmlFiles;
  }

  return {
    name: 'strip-html-comments',
    hooks: {
      /**
       * @param {{ dir: string | URL }} param0
       */
      'astro:build:done': async ({ dir }) => {
        const rootDir = typeof dir === 'string' ? dir : fileURLToPath(dir);
        const htmlFiles = await collectHtmlFiles(rootDir);
        await Promise.all(htmlFiles.map(async (/** @type {string} */ htmlFilePath) => {
          const original = await readFile(htmlFilePath, 'utf8');
          const stripped = original.replace(/<!--[\s\S]*?-->/g, '');
          if (stripped !== original) {
            await writeFile(htmlFilePath, stripped, 'utf8');
          }
        }));
      },
    },
  };
}
