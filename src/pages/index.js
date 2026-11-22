import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const guides = [
  {title: 'Install the app', description: 'Download, sign and install the iOS build.', to: '/docs/installation'},
  {title: 'Understand the runtime', description: 'Explore the Kenran Butō hybrid architecture.', to: '/docs/hybrid-runtime-architecture'},
  {title: 'Build QEMU for iOS', description: 'Read the runtime build pipeline and its constraints.', to: '/docs/qemu-build-workflow'},
  {title: 'Contribute', description: 'Set up development, report issues and validate changes.', to: '/docs/contributing'}
];

export default function Home() {
  return <Layout title="Home" description="Official Akatsubaki Emu documentation and project guides">
    <header className="hero hero--primary"><div className="container">
      <h1 className="hero__title">Akatsubaki Emu</h1>
      <p className="hero__subtitle">The official guide to installation, platform support, Kenran Butō, and emulator development.</p>
      <div className="buttons">
        <Link className="button button--secondary button--lg" to="/docs/">Explore the documentation</Link>
        <Link className="button button--outline button--lg" style={{color:'#fff',borderColor:'#cdaab3'}} to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">View source</Link>
      </div>
    </div></header>
    <main className="container margin-vert--xl">
      <div className="row">{guides.map((guide) => <div className="col col--6 margin-bottom--lg" key={guide.to}>
        <div className="card"><div className="card__header"><h2>{guide.title}</h2></div><div className="card__body"><p>{guide.description}</p></div><div className="card__footer"><Link to={guide.to}>Read guide →</Link></div></div>
      </div>)}</div>
      <div className="alert alert--warning margin-top--lg"><strong>Experimental software:</strong> Akatsubaki Emu is not yet a complete PC emulator. Arbitrary Windows/Linux guests and Steam games are not currently guaranteed to run. A successful build or IPA package is not proof of physical-device guest execution.</div>
      <p className="text--center margin-top--lg"><Link to="/docs/droiddeck-port-status">Review current feature readiness</Link> · <Link to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu/releases">Download releases</Link></p>
    </main>
  </Layout>;
}
