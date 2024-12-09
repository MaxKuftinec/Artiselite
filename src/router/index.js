/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import { useUserStore } from '@/stores/users'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // routes: setupLayouts(routes),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/inventory.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/product',
      name: 'product',
      component: () => import('@/pages/productmanager.vue')
    },
    {
      path: '/datatableexample',
      name: 'dataTableExample',
      component: () => import('@/pages/datatableexample.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/pages/search.vue')
    },
    {
      path: '/testapi',
      name: 'testApi',
      component: () => import('@/pages/testapi.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/login.vue')
    },
    {
      path: '/team',
      name: 'team',
      component: () => import('@/pages/usermanagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/inbound',
      name: 'inbound',
      component: () => import('@/pages/inbound.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/outbound',
      name: 'outbound',
      component: () => import('@/pages/outbound.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
	const userStore = useUserStore();
	const isLoggedIn = userStore.isLoggedIn; // Check if the user is logged in (adjust this as needed)  

	if (to.matched.some(record => record.meta.requiresAuth)) {
		// This route requires authentication
		if (!isLoggedIn) {
			// Not logged in, redirect to login with original target route
			next({
				path: '/login',
				query: { redirect: to.fullPath }, // Store the original target route
			});
		} else {
			// Logged in, proceed to the route
			next();
		}
	} else {
		// This route does not require auth, proceed
		next();
	}
});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
