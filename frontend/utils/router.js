import Navbar from "../components/Navbar.js";
import store from "../utils/store.js";

// Home Page
const Home = {
  template: `
    <div class="container mt-4">
      <h1>Welcome to the Household Services Application V2</h1>
      <p>This is the homepage.</p>
    </div>
  `,
};

// Lazy-load Vue components for performance
const LoginPage = () => import("../pages/LoginPage.js");
const RegisterPage = () => import("../pages/RegisterPage.js");
// const DashboardPage = () => import("../pages/DashboardPage.js");
const AdminDashboard = () => import("../pages/AdminDashboard.js").catch(err => console.error("Failed to load AdminDashboard.js", err));
const CustomerDashboard = () => import("../pages/CustomerDashboard.js").catch(err => {
  console.error("Failed to load CustomerDashboard.js", err);
});
const ProfessionalDashboard = () => import("../pages/ProfessionalDashboard.js");

// Admin Pages
const AdminUsers = () => import("../pages/AdminUsers.js");
const AdminServices = () => import("../pages/AdminServices.js");
const AddService = () => import("../pages/AddService.js");

// Customer Pages
const BookService = () => import("../pages/BookService.js");
const ViewRequests = () => import("../pages/ViewRequests.js");

// Professional Pages
const ViewJobs = () => import("../pages/ViewJobs.js");
const UpdateStatus = () => import("../pages/UpdateStatus.js");

// 404 Not Found Page
const NotFound = {
  template: `
    <div class="container mt-4">
      <h2>404 - Page Not Found</h2>
      <p>The page you are looking for does not exist.</p>
      <router-link to="/">Go Home</router-link>
    </div>
  `,
};

// Define routes
const routes = [
  { path: "/", component: Home },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },

  // // Unified Dashboard (redirects to role-specific dashboard)
  // { path: "/dashboard", component: DashboardPage, meta: { requiresAuth: true } },

  // Admin Routes
  { path: "/admin-dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" } },
  { path: "/admin-users", component: AdminUsers, meta: { requiresAuth: true, role: "admin" } },
  { path: "/admin-services", component: AdminServices, meta: { requiresAuth: true, role: "admin" } },
  { path: "/add-service", component: AddService, meta: { requiresAuth: true, role: "admin" } },

  // Customer Routes
  { path: "/customer-dashboard", component: CustomerDashboard, meta: { requiresAuth: true, role: "customer" } },
  { path: "/book-service", component: BookService, meta: { requiresAuth: true, role: "customer" } },
  { path: "/customer-requests", component: ViewRequests, meta: { requiresAuth: true, role: "customer" } },

  // Professional Routes
  { path: "/professional-dashboard", component: ProfessionalDashboard, meta: { requiresAuth: true, role: "service_professional" } },
  { path: "/professional-jobs", component: ViewJobs, meta: { requiresAuth: true, role: "service_professional" } },
  { path: "/update-job-status", component: UpdateStatus, meta: { requiresAuth: true, role: "service_professional" } },

  // Catch-all route for 404 Not Found (Fix)
  { path: "/:catchAll(.*)", component: NotFound }
];

// Create Vue Router
const router = new VueRouter({
  mode: "history",
  routes
});

// 🔐 Navigation Guard for Authentication & Role-Based Access
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.getters.isAuthenticated;
//   const userRole = store.getters.userRole;

//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next("/login");  // Redirect to login if not authenticated
//   } else if (to.meta.role && to.meta.role !== userRole) {
//     next("/dashboard");  // Redirect unauthorized users to their dashboard
//   } else {
//     next();  // Proceed to route
//   }
// });
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.userRole;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");  // Redirect to login if not authenticated
  } else if (to.meta.role) {
    if (to.meta.role !== userRole) {
      // Redirect to the correct dashboard based on user role
      if (userRole === "admin") next("/admin-dashboard");
      else if (userRole === "customer") next("/customer-dashboard");
      else if (userRole === "service_professional") next("/professional-dashboard");
      else next("/login"); // Default case
    } else {
      next();  // Proceed if the role matches
    }
  } else {
    next();  // Proceed if no role restriction
  }
});


export default router;

