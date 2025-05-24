import ReaderLayout from '@core/views/ReaderLayout.vue';

export default [
  {
    path: '/',
    component: ReaderLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@reader/views/HomePage.vue'),
      },
      {
        path: 'profile',
        name: 'ProfilePage',
        component: () => import('@reader/views/ProfilePage.vue'),
      },
      {
        path: 'bitrix-auth',
        name: 'OauthRedirectPage',
        component: () => import('@reader/views/OauthRedirectPage.vue'),
      },
      {
        path: 'basket',
        name: 'BasketPage',
        component: () => import('@reader/views/BasketPage.vue'),
      },
      {
        path: 'order',
        name: 'OrderPage',
        component: () => import('@reader/views/OrderPage.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: 'note',
        name: 'NotePage',
        component: () => import('@reader/views/NotePage.vue'),
      },
      {
        path: 'orders',
        name: 'OrdersPage',
        component: () => import('@reader/views/OrdersPage.vue'),
      },
    ],
  },
];
