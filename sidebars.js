/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'introduction',
    {type: 'category', label: 'Getting started', collapsible: true, collapsed: false, items: ['installation', 'user-guide', 'faq']},
    {type: 'category', label: 'Platform guides', collapsible: true, collapsed: true, items: ['compatibility', 'ios-entitlements', 'jit-activation', 'tvos']},
    {type: 'category', label: 'Kenran Butō and architecture', collapsible: true, collapsed: false, items: ['hybrid-runtime-architecture', 'host-device-bridge', 'windows-arm64-static-translation', 'droiddeck-port-plan', 'droiddeck-port-status']},
    {type: 'category', label: 'Build, release and maintenance', collapsible: true, collapsed: true, items: ['qemu-build-workflow', 'releases', 'git-sync']},
    {type: 'category', label: 'Project reference', collapsible: true, collapsed: true, items: ['project-metrics']},
    {type: 'category', label: 'Troubleshooting', collapsible: true, collapsed: true, items: ['troubleshooting']},
    {type: 'category', label: 'Contributing and legal', collapsible: true, collapsed: true, items: ['contributing', 'third-party-notices']}
  ]
};
module.exports = sidebars;
