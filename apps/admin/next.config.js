const { withFederatedModules } = require('@module-federation/nextjs-mf');

module.exports = withFederatedModules({
name: 'admin',
filename: 'static/chunks/remoteEntry.js',
exposes: {},
remotes: {
 web: 'web@http://localhost:3000/static/chunks/remoteEntry.js',
 dashboard: 'dashboard@http://localhost:3001/static/chunks/remoteEntry.js'
},
shared: {
 react: { singleton: true, eager: true },
 'react-dom': { singleton: true, eager: true }
},
webpack: (config) => {
 config.output.publicPath = 'auto';
 return config;
}
});
