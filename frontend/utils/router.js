// import { createRouter, createWebHistory } from 'vue-router';
// import LoginPage from '../pages/LoginPage.js';
// import RegisterPage from '../pages/RegisterPage.js';

// const Home = {
//   template: `
//     <div>
//         <h1>Welcome to the Household Services Application V2</h1>
//         <p>This is the homepage.</p>
//     </div>
//   `,
// };

// // Define routes
// const routes = [
//   { path: '/', component: Home }, // Index route
//   { path: '/login', component: LoginPage },
//   { path: '/register', component: RegisterPage },
// ];

// // Create the router
// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// });

// console.log("Router initialized with routes:", routes);

// export default router; // Export the router

const Home = {
  template: `
    <div>
        <h1>Welcome to the Household Services Application V2</h1>
        <p>This is the homepage.</p>
    </div>
  `,
};

// Dynamically import Vue components for Login and Register pages
const LoginPage = () => import("../pages/LoginPage.js");
const RegisterPage = () => import("../pages/RegisterPage.js");

// Define routes
const routes = [
  { path: "/", component: Home }, 
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
];

// Create the router
const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes,
});

console.log("Router initialized with routes:", routes);

export default router;


