import { translations } from './translations.js';

// Function to change language
function changeLanguage(lang) {
    console.log(`Changing language to: ${lang}`);
    document.documentElement.lang = lang;
    localStorage.setItem('preferredLang', lang);

    const elements = document.querySelectorAll('[data-lang-key]');
    elements.forEach(element => {
        const key = element.getAttribute('data-lang-key');
        if (translations[lang] && translations[lang][key]) {
            let text = translations[lang][key];
            if (!element.hasAttribute('data-placeholder-target')) {
                text = text.replace(/\[Model Name\]/g, getPlaceholder("modelName"));
                text = text.replace(/\[Story ID\]/g, getPlaceholder("storyId"));
            }
            element.textContent = text;
        } else {
            console.warn(`Translation key '${key}' not found for language '${lang}'.`);
        }
    });
    updateTableHeadersLang(lang);
}

// Function to get placeholder values
function getPlaceholder(type) {
    const urlParams = new URLSearchParams(window.location.search);
    switch (type) {
        case "modelName":
            return urlParams.get('model') || "[Model Name]";
        case "storyId":
            return urlParams.get('story') || "[Story ID]";
        default:
            return `[${type}]`;
    }
}

// Update table header text for responsive view labels
function updateTableHeadersLang(lang) {
    const currentTranslations = translations[lang] || translations.en;

    const applyLabels = (tableSelector, headerKeys) => {
        const table = document.querySelector(tableSelector);
        if (!table) return;

        table.querySelectorAll('tbody tr.main-row td').forEach(td => {
            const cellIndex = td.cellIndex;
            if (td.classList.contains('expand-col') || (headerKeys[cellIndex] === null && tableSelector === '#detailed-leaderboard-table') ) {
                td.removeAttribute('data-label');
                return;
            }
            
            const headerKey = headerKeys[cellIndex];
            if (headerKey && currentTranslations[headerKey]) {
                const labelText = currentTranslations[headerKey] || '';
                td.setAttribute('data-label', labelText + ': ');
            } else {
                const th = table.querySelector(`thead th:nth-child(${cellIndex + 1})`);
                if (th) {
                    const thText = (th.textContent || '').replace(/[▲▼]/g, '').trim();
                    td.setAttribute('data-label', thText ? thText + ': ' : ' ');
                } else {
                    td.removeAttribute('data-label');
                }
            }
        });
    };

    const indexHeaderKeys = ['table_model', 'table_timestamp', 'table_cref', 'table_sref', 'table_prompt', 'table_quality', 'table_overall', 'table_details'];
    applyLabels('#leaderboard table', indexHeaderKeys);

    const modelDetailHeaderKeys = ['story_id', 'table_cref', 'table_sref', 'table_prompt', 'table_quality', 'table_details'];
    applyLabels('#story-list table', modelDetailHeaderKeys); // story_id is not a lang key but direct text

    const detailedHeaderKeys = [null, 'table_model', 'table_timestamp', 'table_dataset', 'table_mode', 'table_cref', 'table_sref', 'table_prompt', 'table_quality', 'table_overall', 'table_notes'];
    applyLabels('#detailed-leaderboard-table', detailedHeaderKeys);
}

// --- Active Navigation --- 
function setActiveNav() {
    let currentPagePath = window.location.pathname;

    // For Astro, ensure comparisons account for potential trailing slashes or .html extensions if still migrating
    // Normalizing to treat / and /index.html (or /index) as the same for the root.
    if (currentPagePath.endsWith('/')) {
        currentPagePath = currentPagePath.slice(0, -1); // Remove trailing slash for consistency
    }
    if (currentPagePath === '' || currentPagePath === '/index' || currentPagePath === '/index.html') {
        currentPagePath = '/'; // Normalize root path
    }

    const navLinks = document.querySelectorAll('header nav a');
    navLinks.forEach(link => {
        link.classList.remove('text-blue-600', 'font-semibold'); // Remove active classes
        link.classList.add('text-gray-600'); // Add default class

        let linkPath = new URL(link.href).pathname;
        if (linkPath.endsWith('/')) {
            linkPath = linkPath.slice(0, -1);
        }
        if (linkPath === '' || linkPath === '/index' || linkPath === '/index.html') {
            linkPath = '/';
        }

        if (linkPath === currentPagePath) {
            link.classList.add('text-blue-600', 'font-semibold');
            link.classList.remove('text-gray-600');
        }
    });
}


// --- Initial Load & Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    const preferredLang = localStorage.getItem('preferredLang') || 'en';
    changeLanguage(preferredLang);
    setActiveNav();

    const btnEn = document.getElementById('lang-en-btn');
    const btnZh = document.getElementById('lang-zh-btn');

    if (btnEn) {
        btnEn.addEventListener('click', () => changeLanguage('en'));
    }
    if (btnZh) {
        btnZh.addEventListener('click', () => changeLanguage('zh'));
    }
});

// Expose functions to global window if they are called from Astro component inline event handlers like onclick="toggleDetails('...')"
// Astro components with <script> tags are scoped. For global functions called by HTML attributes,
// they need to be on the window object.
window.changeLanguage = changeLanguage;
// toggleDetails and sortTable will be page-specific and handled in those Astro files. 