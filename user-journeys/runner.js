console.log('User journey runner is started.')

import fs from 'fs';
import puppeteer from 'puppeteer';
import { createRunner, parse, PuppeteerRunnerExtension } from '@puppeteer/replay';

const journeyFolder = './journeys';

const replays = fs.readdirSync(journeyFolder);

if(replays.length === 0) {
  console.log({
    message:"No user journey found in the /journeys folder.",
    severity: "WARNING",
  });
  process.exit(1);
} else {
  console.log(`Found ${replays.length} user journeys in folder "journeys"`);
}

let taskIndex = 0;

// If this container is running as a Cloud Run job execution
if(process.env.CLOUD_RUN_JOB) {
  taskIndex = parseInt(process.env.CLOUD_RUN_TASK_INDEX, 10);
}

if(taskIndex > replays.length) {
  console.error({
    message: `The job has been configured with too many tasks and not enough user journeys. 
    We recommend using the same number of tasks as user journeys.
    Number of journeys found: ${replays.length}.
    Index of the current task: ${taskIndexs}.
    This process will now exit.`,
    severity: "WARNING",
  });
  process.exit(1);
}

// Create an extension that prints at every step of the replay
class Extension extends PuppeteerRunnerExtension {
  async beforeEachStep(step, flow) {
    await super.beforeEachStep(step, flow);
    console.log('Step: ', `${step.type} ${step.url || ''}`);
  }

  async afterAllSteps(flow) {
    await super.afterAllSteps(flow);
    console.log('All steps done');
  }
}

// Start a browser and new page, needed to initialize the extension.
// TODO: remove these lines if https://github.com/puppeteer/replay/issues/201 is fixed
const browser = await puppeteer.launch({
  headless: true,
});
const page = await browser.newPage();

const recordingText = fs.readFileSync(`./journeys/${replays[taskIndex]}`, 'utf8');
const recording = parse(JSON.parse(recordingText));

console.log(`User journey ${taskIndex} running: ${replays[taskIndex]}`);
const runner = await createRunner(recording, new Extension(browser, page, 7000));
const result = await runner.run();

if(result) {
  console.log(`User journey ${taskIndex} completed successfully: ${replays[taskIndex]}`);
  console.log('User journey runner has finished, exiting successfully')
  process.exit();
} else {
  console.log(`User journey ${taskIndex} completed with errors: ${replays[taskIndex]}`);
  console.log('User journey runner has finished, exiting with error')
  process.exit(1);
}
