/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'introduction',
    {type: 'category', label: 'Get started', collapsible: true, collapsed: false,
      link: {type: 'generated-index', title: 'Get started', description: 'Install the app, learn the current workflows and find quick answers.'},
      items: ['installation', 'user-guide', 'faq']},
    {type: 'category', label: 'Platform guides', collapsible: true, collapsed: true,
      link: {type: 'generated-index', title: 'Platform guides', description: 'Platform-specific compatibility, memory and JIT guidance.'},
      items: ['compatibility', 'ios-entitlements', 'jit-activation', 'tvos']},
    {type: 'category', label: 'Kenran Butō', collapsible: true, collapsed: false,
      link: {type: 'generated-index', title: 'Kenran Butō architecture', description: 'Explore the hybrid runtime, packaging tools, guest/host boundary and translation plans.'},
      items: ['hybrid-runtime-architecture', 'kenran-buto-aot-abi',
        {type: 'category', label: 'Butō Box', collapsible: true, collapsed: false,
          link: {type: 'doc', id: 'buto-box'},
          items: ['buto-box', 'buto-box-workflow', 'buto-box-bundle-layout', 'buto-box-signing', 'buto-box-compatibility']},
        'host-device-bridge', 'windows-arm64-static-translation', 'droiddeck-port-plan', 'droiddeck-port-status']},
    {type: 'category', label: 'Build and release', collapsible: true, collapsed: true,
      link: {type: 'generated-index', title: 'Build and release', description: 'Build the iOS runtime, understand release channels and repository synchronization.'},
      items: ['qemu-build-workflow', 'releases', 'git-sync', 'pages-sync']},
    {type: 'category', label: 'Project reference', collapsible: true, collapsed: true,
      link: {type: 'generated-index', title: 'Project reference', description: 'Project metrics and implementation status references.'},
      items: ['project-metrics']},
    {type: 'category', label: 'Troubleshooting', collapsible: true, collapsed: true, items: ['troubleshooting']},
    {type: 'category', label: 'Contributing and legal', collapsible: true, collapsed: true,
      link: {type: 'generated-index', title: 'Contributing and legal', description: 'Help improve the project and review third-party licensing information.'},
      items: ['contributing', 'third-party-notices']}
  ]
};
module.exports = sidebars;
