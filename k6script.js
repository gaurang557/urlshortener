import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m',  target: 25 },
    { duration: '30s', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed:                      ['rate<0.01'],
    http_req_duration:                    ['p(95)<500'],
    'http_req_duration{name:redirect}':   ['p(95)<300'],
    'http_req_duration{name:shorten}':    ['p(95)<500'],
  },
};

const BASE_URL = 'https://urlshortener-prjs.onrender.com';
const shortCodes = ['rmY6HI', 'Bmq17g', 'hlSHWn'];

function testRedirect() {
  const shortCode = shortCodes[Math.floor(Math.random() * shortCodes.length)];
  const res = http.get(`${BASE_URL}/${shortCode}`, {
    redirects: 0,
    tags: { name: 'redirect' },
  });

  check(res, {
    'redirect status 301/302': (r) => r.status === 301 || r.status === 302,
    'redirect under 300ms':    (r) => r.timings.duration < 300,
  });
}

function testCreation() {
  const payload = JSON.stringify({
    original_url: 'https://example.com/' + Math.random(),
  });

  const res = http.post(`${BASE_URL}/api/shorten/`, payload, {
    headers: { 'Content-Type': 'application/json' },
    tags: { name: 'shorten' },
  });

  check(res, {
    'shorten status 200/201':  (r) => r.status === 200 || r.status === 201,
    'shorten under 500ms':     (r) => r.timings.duration < 500,
  });
}

export default function () {
  testRedirect();

  // 10% of VUs test creation — matches real 100:1 read/write ratio
  if (Math.random() < 0.1) {
    testCreation();
  }

  sleep(1);
}