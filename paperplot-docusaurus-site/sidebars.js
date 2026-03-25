// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro', // Technical Documentation
    'changelog', // Changelog
    {
      type: 'category',
      label: 'API',
      items: [
        'api/plotter',
        'api/mixins-generic',
        'api/mixins-analysis',
        'api/mixins-domain',
        'api/mixins-ml',
        'api/mixins-modifiers',
        'api/mixins-stats-modifiers',
        'api/mixins-stats-plots',
        'api/mixins-three-d',
        'api/utils',
      ],
    },
  ],
};

export default sidebars;