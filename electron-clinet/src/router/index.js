import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CreateView from '../views/CreateView.vue'
import JoinView from '../views/JoinView.vue'
import NodeView from '../views/NodeView.vue'
import SettingView from '../views/SettingView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
    {
        path: '/',
        name: 'login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterView
    },
    {
        path: '/:userId',
        children: [
            {
                path: 'home',
                name: 'home',
                component: HomeView
            },
            {
                path: 'create',
                name: 'create',
                component: CreateView
            },
            {
                path: 'join',
                name: 'join',
                component: JoinView
            },
            {
                path: 'node',
                name: 'node',
                component: NodeView
            },
            {
                path: 'setting',
                name: 'setting',
                component: SettingView
            },
        ]
    },

    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    // }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

// 在 LoginView 和 RegisterView 不显示导航栏
router.beforeEach((to, from, next) => {
    const hideNavRoutes = ['/login', '/register'];

    if (hideNavRoutes.includes(to.path)) {
        document.getElementById('nav').style.display = 'none';
    } else {
        document.getElementById('nav').style.display = 'block';
    }

    next();
})

export default router
