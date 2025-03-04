const store = new Vuex.Store({
  state: {
      token: localStorage.getItem("token") || "",
      role: localStorage.getItem("role") || ""
  },
  mutations: {
      setAuthData(state, { token, role }) {
          state.token = token;
          state.role = role;
          localStorage.setItem("token", token);
          localStorage.setItem("role", role);
      },
      logout(state) {
          state.token = "";
          state.role = "";
          localStorage.removeItem("token");
          localStorage.removeItem("role");
      }
  },
  actions: {
      login({ commit }, { token, role }) {
          commit("setAuthData", { token, role });
      },
      logout({ commit }) {
          commit("logout");
      }
  },
  getters: {
      isAuthenticated: state => !!state.token,
      userRole: state => state.role
  }
});

export default store;

