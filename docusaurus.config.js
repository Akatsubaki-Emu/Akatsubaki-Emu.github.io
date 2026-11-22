import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Akatsubaki Emu Docs',
  tagline: 'Installation, architecture and development documentation',
  favicon: 'img/favicon.svg',
  url: 'https://akatsubaki-emu.github.io',
  baseUrl: '/',
  organizationName: 'Akatsubaki-Emu',
  projectName: 'Akatsubaki-Emu.github.io',
  onBrokenLinks: 'throw',
  markdown: {hooks: {onBrokenMarkdownLinks: 'warn'}},
  trailingSlash: false,
  i18n: {defaultLocale: 'en', locales: ['en']},
  presets: [['classic', {
    docs: {routeBasePath: 'docs', sidebarPath: './sidebars.js', sidebarCollapsible: true, exclude: ['PAGES_SYNC.md']},
    blog: false,
    theme: {customCss: './src/css/custom.css'}
  }]],
  plugins: [['docusaurus-lunr-search', {languages: ['en'], maxHits: 10, indexBatchSize: 100, excludeRoutes: ['404']}]],
  staticDirectories: ['static', 'alt', 'altsource', 'downloads'],
  themeConfig: {
    colorMode: {defaultMode: 'dark', respectPrefersColorScheme: true},
    navbar: {title: 'Akatsubaki Emu', items: [
      {type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Documentation'},
      {href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu', label: 'Source', position: 'right'},
      {href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases', label: 'Releases', position: 'right'},
      {href: '/AltSource.json', label: 'AltStore source', position: 'right'}
    ]},
    footer: {style: 'dark', links: [
      {title: 'Documentation', items: [{label: 'Introduction', to: '/docs/'}, {label: 'Install', to: '/docs/installation'}]},
      {title: 'Project', items: [{label: 'Source code', href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu'}, {label: 'Releases', href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases'}]},
      {title: 'Distribution', items: [{label: 'AltStore source', href: 'https://akatsubaki-emu.github.io/AltSource.json'}, {label: "Xthrx's Repo", href: 'https://akatsubaki-emu.github.io/altsource/'}]}
    ], copyright: 'Akatsubaki Emu · GPL-3.0'},
    prism: {theme: prismThemes.github, darkTheme: prismThemes.dracula}
  }
};
export default config;
