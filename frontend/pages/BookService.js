export default {
    template: `
    <div>
        <h2>Book a Service</h2>
        <select v-model="selectedService">
            <option v-for="service in services" :key="service.id" :value="service.id">
                {{ service.name }}
            </option>
        </select>
        <button @click="bookService">Book</button>
    </div>
    `,
    data() {
        return {
            selectedService: "",
            services: [
                { id: 1, name: "AC Repair" },
                { id: 2, name: "Cleaning" }
            ]
        };
    },
    methods: {
        bookService() {
            if (!this.selectedService) {
                alert("Please select a service.");
            } else {
                alert(`Service ${this.selectedService} booked successfully.`);
            }
        }
    }
};
