import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const guides = [
  {title: 'Installation', text: 'Install the iOS app and complete the initial setup.', to: '/docs/installation'},
  {title: 'Using Akatsubaki Emu', text: 'Learn about the library, guest files and current launch flow.', to: '/docs/user-guide'},
  {title: 'Compatibility', text: 'Check which parts of the runtime are implemented or still experimental.', to: '/docs/compatibility'},
  {title: 'Kenran Butō', text: 'Read about the hybrid execution architecture.', to: '/docs/hybrid-runtime-architecture'},
  {title: 'JIT setup', text: 'Understand the available JIT activation paths and their limitations.', to: '/docs/jit-activation'},
  {title: 'Troubleshooting', text: 'Find help with installation, signing, file access and runtime issues.', to: '/docs/troubleshooting'}
];

export default function Home() {
  return (
    <Layout title="Home" description="Documentation and project information for Akatsubaki Emu.">
      <main className="home">
        <div className="home-main">
          <div className="home-kicker">Akatsubaki Emu · Project documentation</div>
          <h1>Akatsubaki Emu</h1>
          <p className="home-lead">An experimental emulator for Apple platforms, built around Kenran Butō — a hybrid runtime combining ahead-of-time translation with interpreter fallbacks.</p>
          <div className="home-actions">
            <Link className="button button--primary button--lg" to="/docs/">Read the documentation</Link>
            <Link className="button button--secondary button--lg" to="/docs/installation">Installation guide</Link>
          </div>
          <div className="home-status"><strong>Development status:</strong> the project is still in active development. A successful build or IPA installation does not prove that a guest operating system or application can run. Check the compatibility guide for the current implementation status.</div>
          <h2>About the project</h2>
          <p>Akatsubaki Emu is focused on making guest software run within the constraints of iOS and iPadOS. Its work includes guest loading, memory management, instruction translation, interpreter execution and the host-device interfaces needed by the runtime.</p>
          <h2>Documentation</h2>
          <div className="home-guides">
            {guides.map((guide) => (
              <section className="home-guide" key={guide.title}>
                <Link to={guide.to}>{guide.title}</Link>
                <p>{guide.text}</p>
              </section>
            ))}
          </div>
          <h2>Project links</h2>
          <ul>
            <li><Link to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">Source code</Link></li>
            <li><Link to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases">Releases</Link></li>
            <li><Link to="https://akatsubaki-emu.github.io/AltSource.json">AltStore source</Link></li>
            <li><Link to="/docs/contributing">Contributing</Link></li>
          </ul>
        </div>
      </main>
    </Layout>
  );
}
