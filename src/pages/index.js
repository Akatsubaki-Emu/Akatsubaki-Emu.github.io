import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const principles = [
  {
    number: '01',
    title: 'Hybrid by design',
    description: 'Kenran Butō combines ahead-of-time translation with interpreter fallbacks, so unsupported guest instructions can return to a safer execution path.',
  },
  {
    number: '02',
    title: 'Built around Apple platforms',
    description: 'The project treats iOS constraints such as signing, app sandboxing, memory policy and host-device services as core engineering requirements.',
  },
  {
    number: '03',
    title: 'Open development',
    description: 'Architecture notes, build instructions, compatibility limits and contribution guidance are documented alongside the source.',
  },
];

const guides = [
  {title: 'Installation', description: 'Prepare, sign and install the current iOS build.', to: '/docs/installation', label: 'Get the app'},
  {title: 'User guide', description: 'Understand the current interface, imports and library workflows.', to: '/docs/user-guide', label: 'Learn the basics'},
  {title: 'Compatibility', description: 'Check what is implemented, experimental or still planned.', to: '/docs/compatibility', label: 'Check support'},
  {title: 'Frequently asked questions', description: 'Answers about guest execution, JIT, platforms and the project.', to: '/docs/faq', label: 'Read the FAQ'},
  {title: 'Kenran Butō', description: 'Explore the hybrid runtime and its execution paths.', to: '/docs/hybrid-runtime-architecture', label: 'Explore the architecture'},
  {title: 'Troubleshooting', description: 'Find help with installation, file access, JIT and builds.', to: '/docs/troubleshooting', label: 'Solve a problem'},
];

export default function Home() {
  return (
    <Layout
      title="Akatsubaki Emu"
      description="The official documentation for Akatsubaki Emu and the Kenran Butō hybrid emulation runtime."
    >
      <main className="home">
        <header className="container home-intro">
          <p className="home-intro__eyebrow">OPEN-SOURCE EMULATION PROJECT</p>
          <h1>Akatsubaki Emu</h1>
          <p className="home-intro__lead">
            An experimental emulation project for Apple platforms. Its runtime,
            <strong> Kenran Butō</strong>, brings ahead-of-time translation and
            interpreter fallbacks together to explore guest execution within iOS constraints.
          </p>
          <div className="home-intro__links">
            <Link className="button button--primary button--lg" to="/docs/installation">
              Get started
            </Link>
            <Link className="button button--secondary button--lg" to="/docs/">
              Browse documentation
            </Link>
            <Link className="home-source-link" to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">
              View source code <span aria-hidden="true">↗</span>
            </Link>
          </div>
        </header>

        <section className="container home-status" aria-label="Development status">
          <span className="home-status__mark" aria-hidden="true">i</span>
          <p>
            <strong>Still in active development.</strong> A successful build or installation
            does not establish that a guest operating system or application runs on a physical
            device. Check the compatibility guide for the latest verified status.
          </p>
          <Link to="/docs/compatibility">Compatibility <span aria-hidden="true">→</span></Link>
        </section>

        <section className="container home-section" aria-labelledby="home-principles-title">
          <div className="home-section__heading">
            <p className="home-section__eyebrow">THE PROJECT</p>
            <h2 id="home-principles-title">A practical approach to emulation.</h2>
            <p>Three ideas guide the architecture and the way the project is developed.</p>
          </div>
          <div className="home-feature-grid">
            {principles.map((item) => (
              <article className="home-feature-card" key={item.number}>
                <span className="home-feature-card__number">{item.number}</span>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="home-guides">
          <div className="container home-section">
            <div className="home-section__heading">
              <p className="home-section__eyebrow">DOCUMENTATION</p>
              <h2>Where would you like to start?</h2>
              <p>Choose a guide, or open the full wiki to browse every topic.</p>
            </div>
            <div className="home-guide-grid">
              {guides.map((guide) => (
                <Link className="home-guide-card" to={guide.to} key={guide.to}>
                  <span className="home-guide-card__title">{guide.title}</span>
                  <span className="home-guide-card__description">{guide.description}</span>
                  <span className="home-guide-card__action">{guide.label} <span aria-hidden="true">→</span></span>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="container home-project">
          <div>
            <p className="home-section__eyebrow">KEEP EXPLORING</p>
            <h2>Built in the open.</h2>
            <p>Review the code, follow releases or help improve the project.</p>
          </div>
          <div className="home-project__links">
            <Link to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">Source repository <span aria-hidden="true">↗</span></Link>
            <Link to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases">Releases <span aria-hidden="true">↗</span></Link>
            <Link to="/docs/contributing">Contributing <span aria-hidden="true">→</span></Link>
            <Link to="https://akatsubaki-emu.github.io/AltSource.json">AltStore source <span aria-hidden="true">↗</span></Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
