import Navbar from "../components/Navbar.js";
import store from "./store.js";

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
const DashboardPage = () => import("../pages/DashboardPage.js");
const AdminDashboard = () => import("../pages/AdminDashboard.js");
const CustomerDashboard = () => import("../pages/CustomerDashboard.js");
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

// Define routes
const routes = [
  { path: "/", component: Home },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },

  // Admin Dashboard Route
  { path: "/admin-dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" } },
  { path: "/customer-dashboard", component: CustomerDashboard, meta: { requiresAuth: true, role: "customer" } },
  { path: "/professional-dashboard", component: ProfessionalDashboard, meta: { requiresAuth: true, role: "professional" } },

  // Unified Dashboard (redirects to role-specific dashboard)
  { path: "/dashboard", component: DashboardPage, meta: { requiresAuth: true } },

  // Admin Routes
  { path: "/admin-users", component: AdminUsers, meta: { requiresAuth: true, role: "admin" } },
  { path: "/admin-services", component: AdminServices, meta: { requiresAuth: true, role: "admin" } },
  { path: "/add-service", component: AddService, meta: { requiresAuth: true, role: "admin" } },

  // Customer Routes
  { path: "/book-service", component: BookService, meta: { requiresAuth: true, role: "customer" } },
  { path: "/customer-requests", component: ViewRequests, meta: { requiresAuth: true, role: "customer" } },

  // Professional Routes
  { path: "/professional-jobs", component: ViewJobs, meta: { requiresAuth: true, role: "professional" } },
  { path: "/update-job-status", component: UpdateStatus, meta: { requiresAuth: true, role: "professional" } }
];

// Create Vue Router
const router = new VueRouter({
  mode: "history",
  routes
});

// 🔐 Navigation Guard for Authentication & Role-Based Access
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.userRole;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");  // Redirect to login if not authenticated
  } else if (to.meta.role && to.meta.role !== userRole) {
    next("/dashboard");  // Redirect unauthorized users to their dashboard
  } else {
    next();  // Proceed to route
  }
});

export default router;
