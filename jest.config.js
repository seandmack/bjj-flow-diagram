/**
 * Jest Configuration for BJJ Flow Diagram UI Tests
 */

module.exports = {
  // Test environment
  testEnvironment: 'node',

  // Test file patterns
  testMatch: [
    '**/tests/**/*.test.js'
  ],

  // Coverage configuration
  collectCoverageFrom: [
    'tests/**/*.js',
    '!tests/**/*.test.js'
  ],

  // Coverage thresholds (optional - can be adjusted)
  coverageThresholds: {
    global: {
      statements: 70,
      branches: 70,
      functions: 70,
      lines: 70
    }
  },

  // Timeout for tests (30 seconds)
  testTimeout: 30000,

  // Verbose output
  verbose: true,

  // Maximum number of concurrent workers
  maxWorkers: '50%',

  // Clear mocks between tests
  clearMocks: true,

  // Indicates whether the coverage information should be collected
  collectCoverage: false, // Set to true when running npm run test:coverage

  // Coverage directory
  coverageDirectory: 'coverage',

  // Coverage reporters
  coverageReporters: [
    'text',
    'lcov',
    'html'
  ],

  // Setup files
  // setupFilesAfterEnv: ['<rootDir>/tests/setup.js'], // Uncomment if you create a setup file

  // Module paths
  moduleDirectories: [
    'node_modules'
  ],

  // Transform files (if using TypeScript in future)
  // transform: {},

  // Global setup/teardown
  // globalSetup: undefined,
  // globalTeardown: undefined,
};
