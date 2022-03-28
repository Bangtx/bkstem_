const START = { path: '/', name: 'Start' }
const CLASSROOM = { path: '/classroom/:classroomId', name: 'Classroom' }
const Login = { path: '/login', name: 'Login' }
const ROLLCALL = { path: '/roll_call', name: 'RollCall' }

const DISABLE_NAVIGATION = [Login.path]

export { START, Login, CLASSROOM, ROLLCALL }
