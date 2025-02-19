export default {
    template: `
    <div>
        <h2>Login Page</h2>
        <input type="text" placeholder="email" v-model="email"/>
        <input type="password" placeholder="password" v-model="password"/>
        <button class="btn btn-primary" @click="login">Login</button>
    </div>
    `,
    data(){
        return {
            email: '',
            password: ''
        };
    },
    methods: {
        async login(){
            const res = await fetch(location.origin+'/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            });
            const data = await res.json();
            if (data.error) {
                alert(data.error);
            } else {
               localStorage.setItem('token', data.token);  // Save token for future requests
                alert('Logged in');
            }
        }
    }
};