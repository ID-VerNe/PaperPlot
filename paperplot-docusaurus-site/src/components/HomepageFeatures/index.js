import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '声明式链式调用',
    Img: require('@site/static/img/aesthetic_and_processing_example.png').default,
    description: (
      <>
        像写句子一样构建你的图表，例如 <code>plotter.add_line(...).set_title(...)</code>。绘图后，后续修饰器会自动作用于最后一个活动的子图，无需重复指定目标。
      </>
    ),
  },
  {
    title: '强大的布局系统',
    Img: require('@site/static/img/chart_types_example.png').default,
    description: (
      <>
        无论是简单的网格，还是使用 <code>mosaic</code> 实现的复杂布局，都能轻松定义。通过一个字典即可一次性定义包含子网格的复杂层级布局。
      </>
    ),
  },
  {
    title: '内置科研主题与调色板',
    Img: require('@site/static/img/style_gallery_marin_kitagawa.png').default,
    description: (
      <>
        提供多种专业美观的内置样式和丰富的动漫游戏主题调色板，一键切换图表风格和颜色方案，保证全局一致性。
      </>
    ),
  },
];

function Feature({Img, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={Img} className={styles.featureImg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
