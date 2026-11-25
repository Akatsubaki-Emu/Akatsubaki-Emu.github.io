/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Akatsubaki Emu',
  tagline: 'A practical guide to installation, Kenran Butō and experimental guest execution on Apple platforms.',
  favicon: 'img/favicon.svg',
  url: 'https://akatsubaki-emu.github.io',
  baseUrl: '/',
  organizationName: 'Akatsubaki-Emu',
  projectName: 'Akatsubaki-Emu.github.io',
  onBrokenLinks: 'throw',
  markdown: {hooks: {onBrokenMarkdownLinks: 'warn'}},
  trailingSlash: false,
  headTags: [{
    tagName: 'meta',
    attributes: {
      name: 'google-site-verification',
      content: 'dskTPELl4KFBeZASfSDUawWQuAqBPbxrcb9TFvXgOKk'
    }
  }],
  i18n: {defaultLocale: 'en', locales: ['en']},
  presets: [['classic', {
    docs: {routeBasePath: 'docs', sidebarPath: './sidebars.js', sidebarCollapsible: true},
    blog: false,
    theme: {customCss: ['./src/css/custom.css', './src/css/docs-theme.css']}
  }]],
  plugins: [['docusaurus-lunr-search', {languages: ['en'], maxHits: 10, indexBatchSize: 100, excludeRoutes: ['404']}]],
  staticDirectories: ['static'],
  themeConfig: {
    colorMode: {defaultMode: 'dark', disableSwitch: false, respectPrefersColorScheme: true},
    navbar: {
      title: 'Akatsubaki Emu',
      logo: {alt: 'Akatsubaki Emu mark', src: 'img/favicon.svg'},
      hideOnScroll: false,
      items: [
        {type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Documentation'},
        {href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu', label: 'Source', position: 'right'},
        {href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases', label: 'Releases', position: 'right'},
        {href: 'https://akatsubaki-emu.github.io/AltSource.json', label: 'AltStore source', position: 'right'},
        {href: "https://altdirect.app/?url=https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json", label: "Xthrx's repo", position: 'right'}
      ]
    },
    docs: {sidebar: {hideable: true, autoCollapseCategories: false}},
    footer: {
      style: 'dark',
      links: [
        {title: 'Get started', items: [
          {label: 'Documentation home', to: '/docs/'}, {label: 'Installation', to: '/docs/installation'},
          {label: 'User guide', to: '/docs/user-guide'}, {label: 'Troubleshooting', to: '/docs/troubleshooting'}
        ]},
        {title: 'Architecture', items: [
          {label: 'Kenran Butō', to: '/docs/hybrid-runtime-architecture'}, {label: 'Host-device bridge', to: '/docs/host-device-bridge'},
          {label: 'Compatibility', to: '/docs/compatibility'}, {label: 'QEMU runtime', to: '/docs/qemu-build-workflow'}
        ]},
        {title: 'Project', items: [
          {label: 'Source code', href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu'},
          {label: 'Releases', href: 'https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases'},
          {label: 'Contributing', to: '/docs/contributing'}, {label: 'Third-party notices', to: '/docs/third-party-notices'}
        ]},
        {title: 'Distribution', items: [
          {label: 'AltStore source', href: 'https://akatsubaki-emu.github.io/AltSource.json'},
          {label: "Xthrx's Repo", href: 'https://akatsubaki-emu.github.io/altsource/'}
        ]}
      ],
      copyright: 'Akatsubaki Emu · GPL-3.0'
    }
  }
};
module.exports = config;
