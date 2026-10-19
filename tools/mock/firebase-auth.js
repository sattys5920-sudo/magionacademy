let cbs = [];
const user = { uid: window.__uid || 'me1', email: window.__email };
export const getAuth = () => ({});
export const onAuthStateChanged = (a, cb) => { cbs.push(cb); setTimeout(() => cb(user), 10); };
export const createUserWithEmailAndPassword = async () => {}; export const signInWithEmailAndPassword = async () => {};
