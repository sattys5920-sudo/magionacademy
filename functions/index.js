// 용의 알 지키기 서버: 관리자 화면을 켜 두지 않아도 서버가 계산해요.
// 관리자 화면이 defense/run 을 쓰면 시작하고, 9분 가까이 돌다가 스스로 다음 실행을 불러서 이어 가요.
const { onValueWritten } = require('firebase-functions/v2/database');
const admin = require('firebase-admin');
const { runHost } = require('./dfhost');
const { runAuto } = require('./autohost');

admin.initializeApp({ databaseURL: 'https://magionacademy-default-rtdb.asia-southeast1.firebasedatabase.app' });

exports.dfrun = onValueWritten({
  ref: '/defense/run', instance: 'magionacademy-default-rtdb', region: 'asia-southeast1',
  timeoutSeconds: 540, memory: '256MiB', maxInstances: 2, cpu: 1,
}, async ev => {
  const R = ev.data.after.val(); if (!R || !R.n) return;
  await runHost(admin.database(), R);
});

// 자동 이벤트 (유령 열차 · 별 보는 밤): 학생 화면이 정해진 시각에 autoreq/<키> 를 한 번 쓰면 서버가 열고 진행해요 (autohost.js)
exports.autorun = onValueWritten({
  ref: '/autoreq/{key}', instance: 'magionacademy-default-rtdb', region: 'asia-southeast1',
  timeoutSeconds: 540, memory: '256MiB', maxInstances: 2, cpu: 1,
}, async ev => {
  if (ev.data.before.exists() || !ev.data.after.exists()) return;   // 처음 쓰일 때만
  const r = await runAuto(admin.database(), ev.params.key); console.log('autorun', ev.params.key, r);
});
