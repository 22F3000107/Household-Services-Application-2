// export default {
//   template: `
//     <nav class="navbar navbar-expand-lg navbar-light bg-light">
//       <div class="container-fluid">
//         <a class="navbar-brand" href="/">Household Services</a>
//         <button
//           class="navbar-toggler"
//           type="button"
//           data-bs-toggle="collapse"
//           data-bs-target="#navbarNav"
//           aria-controls="navbarNav"
//           aria-expanded="false"
//           aria-label="Toggle navigation"
//         >
//           <span class="navbar-toggler-icon"></span>
//         </button>
//         <div class="collapse navbar-collapse" id="navbarNav">
//           <ul class="navbar-nav me-auto">
//             <li class="nav-item">
//               <router-link class="nav-link" to="/">Home</router-link>
//             </li>
//             <li v-if="!isLoggedIn" class="nav-item">
//               <router-link class="nav-link" to="/login">Login</router-link>
//             </li>
//             <li v-if="!isLoggedIn" class="nav-item">
//               <router-link class="nav-link" to="/register">Register</router-link>
//             </li>
//             <li v-if="isAdmin" class="nav-item">
//               <router-link class="nav-link" to="/admin-dashboard">Admin Dashboard</router-link>
//             </li>
//             <li v-if="isCustomer" class="nav-item">
//               <router-link class="nav-link" to="/customer-dashboard">Customer Dashboard</router-link>
//             </li>
//             <li v-if="isProfessional" class="nav-item">
//               <router-link class="nav-link" to="/professional-dashboard">Professional Dashboard</router-link>
//             </li>
//           </ul>
//           <button v-if="isLoggedIn" @click="logout" class="btn btn-danger">Logout</button>
//         </div>
//       </div>
//     </nav>
//   `,
//   computed: {
//     isLoggedIn() {
//       return !!localStorage.getItem("token");
//     },
//     userRole() {
//       return localStorage.getItem("role");
//     },
//     isAdmin() {
//       return this.userRole === "admin";
//     },
//     isCustomer() {
//       return this.userRole === "customer";
//     },
//     isProfessional() {
//       return this.userRole === "professional";
//     }
//   },
//   methods: {
//     logout() {
//       localStorage.removeItem("token");
//       localStorage.removeItem("role");
//       alert("Logged out successfully!");
//       this.$router.push("/login"); // Redirect to login
//     }
//   }
// };

export default {
  template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold text-primary" href="/">Household Services</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li v-if="!isLoggedIn" class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
            <li v-if="isAdmin" class="nav-item">
              <router-link class="nav-link" to="/admin-dashboard">Admin Dashboard</router-link>
            </li>
            <li v-if="isCustomer" class="nav-item">
              <router-link class="nav-link" to="/customer-dashboard">Customer Dashboard</router-link>
            </li>
            <li v-if="isProfessional" class="nav-item">
              <router-link class="nav-link" to="/professional-dashboard">Professional Dashboard</router-link>
            </li>
          </ul>
          
          <div class="d-flex">
            <button v-if="isLoggedIn" @click="logout" class="btn btn-danger px-4">Logout</button>
          </div>
        </div>
      </div>
    </nav>
  `,
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("token");
    },
    userRole() {
      return localStorage.getItem("role");
    },
    isAdmin() {
      return this.userRole === "admin";
    },
    isCustomer() {
      return this.userRole === "customer";
    },
    isProfessional() {
      return this.userRole === "professional";
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      alert("Logged out successfully!");
      this.$router.push("/login"); // Redirect to login
    }
  }
};
