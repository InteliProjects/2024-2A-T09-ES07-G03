module.exports = {
  transform: {
    "^.+\\.jsx?$": "babel-jest",
  },
  transformIgnorePatterns: [
    "/node_modules/(?!axios)/", // Permite que o Jest transforme o axios
  ],
  moduleNameMapper: {
    "\\.(css|scss)$": "identity-obj-proxy",
  },
  testEnvironment: "jsdom",
  moduleFileExtensions: ["js", "jsx"],
};
