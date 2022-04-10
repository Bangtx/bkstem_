const START = { path: '/', name: 'Start' }
const CLASSROOM = { path: '/classroom/:classroomId', name: 'Classroom' }
const Login = { path: '/login', name: 'Login' }
const Admin = { path: '/admin', name: 'Admin' }

const DISABLE_NAVIGATION = [Login.path]

export { START, Login, CLASSROOM, Admin }
