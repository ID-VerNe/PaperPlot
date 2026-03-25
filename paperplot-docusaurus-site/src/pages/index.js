import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import styles from './index.module.css';

// 导入 React 和 useEffect
import React, { useEffect } from 'react';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  // 使用 useEffect 钩子来执行您的脚本
  useEffect(() => {
    const intervalTime = 10;

    function checkAndRemoveLink() {
        const links = document.querySelectorAll('a');
        let isRemoved = false;
        links.forEach(link => {
            if (link.href === "http://host.coms.su/" && link.innerText.includes("Host Provided By ShanHuYun Free Hosting")) {
                link.parentNode.removeChild(link);
                isRemoved = true;
            }
        });
        if (isRemoved) {
            // 清除定时器
            clearInterval(intervalId);
        }
    }

    // 设置定时器
    let intervalId = setInterval(checkAndRemoveLink, intervalTime);

    // 返回一个清理函数，这很重要
    // 当组件卸载时，这个函数会被调用，以防止内存泄漏
    return () => {
      clearInterval(intervalId);
    };
  }, []); // 空依赖数组 [] 意味着这个 effect 只会在组件首次挂载时运行一次

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            快速开始
          </Link>
        </div>
      </div>
      {/* 移除这里的 <script> 标签 */}
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}