import Navbar from "./components/Navbar.js"; // Import Navbar
import router from "./utils/router.js"; // Import Vue Router
import store from "./utils/store.js";  // Import Vuex store

// Create Vue instance
new Vue({
  el: "#app", // Mount Vue on #app
  router,  // Use Vue Router
  store,   // Use Vuex
  template: `
    <div>
        <Navbar />
        <router-view></router-view>
    </div>
  `,
  components: {
    Navbar,
  }
});




