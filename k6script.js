import http from 'k6/http';
import { check, sleep } from 'k6';

// test configuration
export const options = {
  stages: [
    { duration: '30s', target: 100 },   // ramp up
    { duration: '1m', target: 500 },    // steady load
    { duration: '30s', target: 1000 },  // spike
    { duration: '30s', target: 0 },     // ramp down
  ],
};

// Base URL
const BASE_URL = 'https://urlshortener-prjs.onrender.com';

// Sample short codes (replace with real ones)
const shortCodes = ['rmY6HI', 'Bmq17g', 'hlSHWn'];

export default function () {

  // 🔁 Test redirect endpoint (MOST IMPORTANT)
  const shortCode = shortCodes[Math.floor(Math.random() * shortCodes.length)];
  const redirectRes = http.get(`${BASE_URL}/${shortCode}`, {
    redirects: 0, // we only check redirect response
  });

  check(redirectRes, {
    'redirect status is 301/302': (r) => r.status === 301 || r.status === 302,
    'response time < 300ms': (r) => r.timings.duration < 300,
  });

  // ➕ Test URL creation endpoint
  const payload = JSON.stringify({
    original_url: 'https://example.com/' + Math.random(),
  });

  const headers = {
    'Content-Type': 'application/json',
  };

  const createRes = http.post(`${BASE_URL}/api/shorten/`, payload, { headers });

  check(createRes, {
    'shorten API status 200/201': (r) => r.status === 200 || r.status === 201,
    'creation response < 300ms': (r) => r.timings.duration < 300,
  });

  sleep(1);
}