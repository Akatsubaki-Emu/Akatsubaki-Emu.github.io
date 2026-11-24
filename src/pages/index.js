import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const pathways = [
  {number: '01', eyebrow: 'GET STARTED', title: 'Install and set up', description: 'Follow the current installation path, understand signing, and prepare the app on iOS.', to: '/docs/installation', link: 'Installation guide'},
  {number: '02', eyebrow: 'HOW IT WORKS', title: 'Explore Kenran Butō', description: 'See how interpretation, translation and native execution fit together in the hybrid runtime.', to: '/docs/hybrid-runtime-architecture', link: 'Runtime architecture'},
  {number: '03', eyebrow: 'BEFORE YOU START', title: 'Check compatibility', description: 'Separate verified behavior from prototypes, experiments and work still in progress.', to: '/docs/compatibility', link: 'Compatibility status'}
];
const principles = [
  {symbol: 'K', title: 'Hybrid by design', text: 'Kenran Butō combines translated hot paths with interpreter fallbacks instead of relying on one execution strategy.'},
  {symbol: 'iOS', title: 'Built around iOS', text: 'The project focuses on the realities of Apple platforms: app sandboxing, signing, memory and device capabilities.'},
  {symbol: '↗', title: 'Open development', text: 'Architecture notes, build guidance and project decisions are documented so progress can be inspected and improved.'}
];
export default function Home() {
  return (
    <Layout title="Akatsubaki Emu" description="The official home of Akatsubaki Emu: an experimental iOS emulation project powered by the Kenran Butō hybrid runtime.">
      <main className="home">
        <section className="home-hero">
          <div className="container home-hero__inner">
            <div className="home-hero__copy">
              <div className="eyebrow"><span className="eyebrow__dot" /> OPEN-SOURCE EMULATION PROJECT</div>
              <h1>Run more than<br /><span>you thought possible.</span></h1>
              <p className="home-hero__lead">Akatsubaki Emu is an experimental emulation project for Apple platforms, built around <strong>Kenran Butō</strong> — a hybrid execution architecture that brings translation and interpretation together.</p>
              <div className="home-hero__actions">
                <Link className="button button--primary button--lg" to="/docs/">Explore the docs <span aria-hidden="true">↗</span></Link>
                <Link className="home-text-link" to="https://github.com/Akatsubaki-Emu/Akatsubaki-Emu">Explore the source <span aria-hidden="true">→</span></Link>
              </div>
              <div className="home-hero__meta"><span><i className="meta-mark meta-mark--rose" /> In active development</span><span><i className="meta-mark" /> iOS-first research</span></div>
            </div>
            <div className="runtime-art" aria-label="Illustration of the Kenran Butō hybrid runtime">
              <div className="runtime-art__halo runtime-art__halo--one" /><div className="runtime-art__halo runtime-art__halo--two" />
              <div className="runtime-art__orbit runtime-art__orbit--one" /><div className="runtime-art__orbit runtime-art__orbit--two" />
              <div className="runtime-art__node runtime-art__node--top"><span>01</span> TRANSLATE</div>
              <div className="runtime-art__node runtime-art__node--left"><span>02</span> INTERPRET</div>
              <div className="runtime-art__node runtime-art__node--right"><span>03</span> EXECUTE</div>
              <div className="runtime-art__core"><div className="runtime-art__core-mark">K</div><strong>KENRAN BUTŌ</strong><small>HYBRID RUNTIME</small></div>
              <div className="runtime-art__caption">ONE RUNTIME · MULTIPLE EXECUTION PATHS</div>
            </div>
          </div><div className="home-hero__edge" />
        </section>
        <section className="home-notice"><div className="container home-notice__inner">
          <span className="home-notice__icon" aria-hidden="true">i</span>
          <p><strong>Still under development.</strong> Guest execution and platform support are evolving. A successful build or install does not yet mean every guest OS or application will run. Check the compatibility guide for the current evidence.</p>
          <Link to="/docs/compatibility">What works today <span aria-hidden="true">→</span></Link>
        </div></section>
        <section className="home-section container">
          <div className="section-heading"><div><div className="eyebrow">FIND YOUR WAY</div><h2>Start with what matters.</h2></div>
            <p>Whether you are installing, exploring the internals or contributing, these are the best places to begin.</p></div>
          <div className="pathway-grid">{pathways.map((item) => <article className="pathway-card" key={item.number}>
            <div className="pathway-card__top"><span>{item.eyebrow}</span><span>{item.number}</span></div><h3>{item.title}</h3><p>{item.description}</p><Link to={item.to}>{item.link} <span aria-hidden="true">↗</span></Link>
          </article>)}</div>
        </section>
        <section className="principles-section"><div className="container">
          <div className="section-heading section-heading--light"><div><div className="eyebrow">THE PROJECT</div><h2>Engineered for the edge cases.</h2></div>
            <p>Emulation on iOS is a systems problem. The project makes those constraints part of the architecture, not an afterthought.</p></div>
          <div className="principles-grid">{principles.map((item) => <article className="principle" key={item.title}>
            <div className="principle__symbol">{item.symbol}</div><h3>{item.title}</h3><p>{item.text}</p>
          </article>)}</div>
          <div className="principles-footer"><span>OPEN SOURCE <b>·</b> BUILT IN THE OPEN</span><Link to="/docs/">Read the project overview <span aria-hidden="true">→</span></Link></div>
        </div></section>
        <section className="home-bottom container"><div><div className="eyebrow">GO DEEPER</div><h2>Good engineering starts with good documentation.</h2><p>Browse the guides, review the technical notes, or help improve the project.</p></div>
          <div className="home-bottom__links"><Link className="button button--primary" to="/docs/">Browse documentation</Link><Link className="button button--secondary" to="/docs/contributing">Contribute to the project</Link></div>
        </section>
      </main>
    </Layout>
  );
}
