export default {
    template: `
    <div>
        <h2>Assigned Jobs</h2>
        <ul>
            <li v-for="job in jobs" :key="job.id">
                {{ job.service }} - Customer: {{ job.customer }}
                <button @click="markCompleted(job.id)">Mark as Completed</button>
            </li>
        </ul>
    </div>
    `,
    data() {
        return {
            jobs: [
                { id: 1, service: "AC Repair", customer: "John Doe" },
                { id: 2, service: "Cleaning", customer: "Jane Smith" }
            ]
        };
    },
    methods: {
        markCompleted(jobId) {
            alert(`Job ${jobId} marked as completed.`);
        }
    }
};
