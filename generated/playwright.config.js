import {devices} from '@playwright/test';

const config = {
    testDir: './tests',
    timeout: 60 * 5 * 1000,
    globalTimeout: 60 * 15 * 1000,
    expect: {
        timeout: 5000
    },
    fullyParallel: true,
    forbidOnly: false,
    retries: 0,
    workers: 1,
    reporter: [['json', {"outputFile": "report.json"}],["list"]],
    use: {
        baseURL: 'https://www.google.com',
        trace: 'on',
        headless: true,
        browserName: 'edge',
        video: 'on',
        ignoreHTTPSErrors: true
    }
};

module.exports = config;