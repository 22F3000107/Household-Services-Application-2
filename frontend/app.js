import Navbar from "./components/Navbar.js"; // Import Navbar
import router from "./utils/router.js"; // import router
const app = Vue.createApp({
  template: `
    <div>
        <Navbar />
        <router-view></router-view>
    </div>
  `,
  components: {
    Navbar,
  },
});

// Use Vue Router
app.use(router);

// Mount the Vue app
app.mount("#app");




