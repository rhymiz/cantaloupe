from pathlib import Path

from cantaloupe.generation.generator import CodeGenerator

from cantaloupe.loaders import load_context
from cantaloupe.models import Context


def test_generate_playwright_config_file() -> None:
    """
    Test that the code generator can translate a workflow to code
    """
    workflow_path = Path(__file__).parent.parent / "workflows"
    context_data = load_context(workflow_path)
    assert context_data is not None
    context = Context(**context_data, workflows=[], output_dir=Path(), workflow_dir=workflow_path)
    generator = CodeGenerator(context)
    data = generator.generate()
    config = filter(lambda x: x.name == "playwright.config.js", data.files)
    assert (
        next(config).content
        == """
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    timeout: 60 * 1000,
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
        browserName: 'chromium',
        video: 'on',
        screenshot: 'on',
        ignoreHTTPSErrors: true,
        actionTimeout: 15000,
        navigationTimeout: 15000,
    }
});""".lstrip()
    )
