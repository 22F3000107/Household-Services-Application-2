const store = new Vuex.Store({
    state: {
        token: localStorage.getItem("token") || "",
        role: localStorage.getItem("role") || "",
        bookedServices: JSON.parse(localStorage.getItem("bookedServices")) || [] // Load from localStorage
    },
    mutations: {
        setAuthData(state, { token, role }) {
            state.token = token;
            state.role = role;
            localStorage.setItem("token", token);
            localStorage.setItem("role", role);

            if (role === "admin") {
                localStorage.setItem("adminToken", token);
            }
        },
        logout(state) {
            state.token = "";
            state.role = "";
            state.bookedServices = []; // Clear booked services on logout
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            localStorage.removeItem("adminToken");
            localStorage.removeItem("bookedServices");
        },
        ADD_BOOKING(state, service) {
            state.bookedServices.push(service);
            localStorage.setItem("bookedServices", JSON.stringify(state.bookedServices)); // Save to localStorage
        }
    },
    actions: {
        login({ commit }, { token, role }) {
            commit("setAuthData", { token, role });
        },
        logout({ commit }) {
            commit("logout");
        },
        bookService({ commit }, service) {
            commit("ADD_BOOKING", service);
        }
    },
    getters: {
        isAuthenticated: state => !!state.token,
        userRole: state => state.role,
        bookedServices: state => state.bookedServices,
        authToken: state => state.token
    }
});

export default store;
