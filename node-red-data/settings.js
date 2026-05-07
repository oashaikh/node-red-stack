/**
 * Minimal Node-RED settings. Tracked in git — runtime caches are .gitignored.
 * Customise here rather than via the UI so config stays in source control.
 */
module.exports = {
  flowFile: "flows.json",
  flowFilePretty: true,
  credentialSecret: process.env.NODE_RED_CREDENTIAL_SECRET || "",
  uiPort: process.env.PORT || 1880,
  diagnostics: { enabled: true, ui: true },
  logging: {
    console: {
      level: process.env.NODE_RED_LOG_LEVEL || "info",
      metrics: false,
      audit: false,
    },
  },
  exportGlobalContextKeys: false,
  externalModules: {
    autoInstall: true,
    palette: { allowInstall: true, allowUpload: true },
    modules: { allowInstall: true },
  },
  editorTheme: {
    page: { title: "Node-RED Stack" },
    header: { title: "Node-RED Stack" },
    palette: { editable: true },
    projects: { enabled: false },
    codeEditor: { lib: "monaco", options: { theme: "vs" } },
  },
  functionExternalModules: true,
  functionTimeout: 0,
  functionGlobalContext: {},
  debugMaxLength: 1000,
  mqttReconnectTime: 15000,
};
