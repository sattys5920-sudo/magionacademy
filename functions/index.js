// 용의 알 지키기 서버: 관리자 화면을 켜 두지 않아도 서버가 계산해요.
// 관리자 화면이 defense/run 을 쓰면 시작하고, 9분 가까이 돌다가 스스로 다음 실행을 불러서 이어 가요.
const { onValueWritten } = require('firebase-functions/v2/database');
const admin = require('firebase-admin');
const { runHost } = require('./dfhost');

admin.initializeApp({ databaseURL: 'https://magionacademy-default-rtdb.asia-southeast1.firebasedatabase.app' });

exports.dfrun = onValueWritten({
  ref: '/defense/run', instance: 'magionacademy-default-rtdb', region: 'asia-southeast1',
  timeoutSeconds: 540, memory: '256MiB', maxInstances: 2, cpu: 1,
}, async ev => {
  const R = ev.data.after.val(); if (!R || !R.n) return;
  await runHost(admin.database(), R);
});
