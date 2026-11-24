import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout
      title="Akatsubaki Emu"
      description="Documentation and development notes for Akatsubaki Emu and the Kenran Butō hybrid emulation runtime."
    >
      <main className="home">
        <header className="container home-intro">
          <h1>Akatsubaki Emu</h1>
          <p className="home-intro__lead">
            An experimental emulation project for Apple platforms. Its runtime,
            Kenran Butō, combines ahead-of-time translation with interpreter
            fallbacks to explore guest execution within iOS constraints.
          </p>
          <div className="home-intro__links">
            <Link className="button button--primary button--lg" to="/docs/">
              Read the documentation
            </Link>
            <Link className="button button--secondary button--lg" to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">
              View source code
            </Link>
          </div>
        </header>

        <section className="home-status" aria-label="Development status">
          <p>
            <strong>Development status:</strong> the project is still in active
            development. A successful build or installation does not establish
            that a guest operating system or application runs on a physical
            device. Check the compatibility notes for the current state.
          </p>
        </section>

        <section className="container home-section">
          <h2>What is included?</h2>
          <ul className="home-feature-list">
            <li><strong>Kenran Butō:</strong> the hybrid execution architecture, including translation and interpreter paths.</li>
            <li><strong>Apple-platform runtime work:</strong> research into memory, signing, app sandboxing and host-device services.</li>
            <li><strong>Build and release tooling:</strong> project build instructions, QEMU integration notes and release information.</li>
          </ul>
        </section>

        <section className="container home-section">
          <h2>Getting started</h2>
          <p>Choose the guide that matches what you want to do.</p>
          <ul className="home-links">
            <li><Link to="/docs/installation">Installation guide</Link></li>
            <li><Link to="/docs/user-guide">Using the app</Link></li>
            <li><Link to="/docs/compatibility">Compatibility and status</Link></li>
            <li><Link to="/docs/faq">Frequently asked questions</Link></li>
            <li><Link to="/docs/hybrid-runtime-architecture">Kenran Butō architecture</Link></li>
            <li><Link to="/docs/contributing">Contributing</Link></li>
          </ul>
        </section>

        <section className="container home-section">
          <h2>About this documentation</h2>
          <p>
            These pages describe the current implementation and the work still
            required. Experimental features are identified as such; plans and
            research notes should not be read as evidence that a feature is
            already available.
          </p>
          <p>
            <Link to="/docs/compatibility">Read the compatibility notes</Link>
            {' · '}
            <Link to="/docs/troubleshooting">Troubleshooting</Link>
            {' · '}
            <Link to="/docs/third-party-notices">Third-party notices</Link>
          </p>
        </section>
      </main>
    </Layout>
  );
}
